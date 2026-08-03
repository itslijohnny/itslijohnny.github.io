#!/usr/bin/env python3
"""Download remote images referenced in post markdown and rewrite the links to
local page resources.

Hugo can only generate responsive variants for images it can resolve as page
resources. Hotlinked images are skipped by that pipeline, and they rot: several
of the hosts used in this blog's older posts block hotlinking or expire URLs.
This script pulls each remote image into the post's own directory and rewrites
the markdown to reference it by filename.

Run it somewhere with open outbound network access, then review and commit.

    python3 scripts/localize-remote-images.py --dry-run   # show planned changes
    python3 scripts/localize-remote-images.py             # download and rewrite

Only images that download successfully are rewritten; anything that fails is
left untouched and reported at the end, so the script is safe to re-run.
"""

import argparse
import binascii
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

# ![alt](url) where url is remote. Title text after the URL is preserved.
IMAGE_RE = re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<url>https?://[^)\s]+)(?P<title>\s+"[^"]*")?\)')

USER_AGENT = "Mozilla/5.0 (compatible; localize-remote-images/1.0)"
TIMEOUT = 30

# GitHub's image proxy. The path's second segment is the hex-encoded origin URL.
CAMO_HOST = "camo.githubusercontent.com"


def resolve_camo(url):
    """Return the origin URL behind a camo proxy link, or the URL unchanged.

    Saving the proxy's copy would preserve a link that GitHub rotates and
    purges; the origin is the stable artifact.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != CAMO_HOST:
        return url
    segments = [s for s in parsed.path.split("/") if s]
    for segment in reversed(segments):
        try:
            decoded = binascii.unhexlify(segment).decode("utf-8")
        except (binascii.Error, ValueError, UnicodeDecodeError):
            continue
        if decoded.startswith(("http://", "https://")):
            return decoded
    return url


def filename_for(url, content_type, taken):
    """Pick a collision-free local filename for a downloaded image."""
    path = urllib.parse.urlparse(url).path
    base = os.path.basename(urllib.parse.unquote(path)) or "image"

    stem, ext = os.path.splitext(base)
    if not ext:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".png"
        if ext == ".jpe":
            ext = ".jpg"

    stem = re.sub(r"[^A-Za-z0-9._-]", "-", stem).strip("-.") or "image"
    stem = stem[:60]

    candidate = f"{stem}{ext}"
    n = 2
    while candidate in taken:
        candidate = f"{stem}-{n}{ext}"
        n += 1
    taken.add(candidate)
    return candidate


DIAGNOSIS = {
    "dns": (
        "dns: the hostname does not resolve, so nothing was ever contacted. The\n"
        "  subdomain is usually retired rather than the image being gone. Sina's\n"
        "  ws1-ws4.sinaimg.cn are retired in favour of wx1-wx4 and tva/tvax, for\n"
        "  example, and the rest of the URL still works. Try swapping the\n"
        "  subdomain and re-running before giving up on the image."
    ),
    "blocked": (
        "blocked: a proxy or egress policy refused the request. This says nothing\n"
        "  about the host. Re-run from a network that allows it."
    ),
    "http": (
        "http: the host answered but refused or lost the image. A 403 is hotlink\n"
        "  protection; a referer retry was already tried for known hosts. Open the\n"
        "  URL in a browser, and if it loads, save it into the post folder by hand.\n"
        "  A 404 means it is gone; replace or remove the image."
    ),
    "other": (
        "other: the request failed for some other reason. Check the message above;\n"
        "  a timeout is worth simply retrying."
    ),
}


def classify(error):
    """Bucket a download failure so the summary describes what actually happened."""
    text = error.lower()
    if "tunnel connection failed" in text or "proxyerror" in text:
        return "blocked"
    if (
        "nodename nor servname" in text
        or "name or service not known" in text
        or "temporary failure in name resolution" in text
        or "getaddrinfo" in text
        or "no address associated" in text
    ):
        return "dns"
    if "http error" in text:
        return "http"
    return "other"


# Hosts that serve the image only when the request looks like it came from the
# site the image was uploaded to. Retrying with the matching referer recovers
# your own images; it does not reach anything a browser could not.
REFERERS = {
    "sinaimg.cn": "https://weibo.com/",
    "i.loli.net": "https://sm.ms/",
}


def referer_for(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    for suffix, referer in REFERERS.items():
        if host == suffix or host.endswith("." + suffix):
            return referer
    return None


def download(url, referer=None):
    headers = {"User-Agent": USER_AGENT}
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read(), response.headers.get("Content-Type", "")


def download_with_retry(url):
    """Fetch url, retrying once with a site-appropriate referer on 403.

    Returns (data, content_type, note).
    """
    try:
        data, content_type = download(url)
        return data, content_type, ""
    except urllib.error.HTTPError as error:
        referer = referer_for(url) if error.code == 403 else None
        if not referer:
            raise
        data, content_type = download(url, referer=referer)
        return data, content_type, f" (retried with referer {referer})"


def process(markdown_path, dry_run):
    with open(markdown_path, encoding="utf-8") as handle:
        text = handle.read()

    post_dir = os.path.dirname(markdown_path)
    taken = set(os.listdir(post_dir))
    rewrites = {}
    failures = []

    for match in IMAGE_RE.finditer(text):
        url = match.group("url")
        if url in rewrites:
            continue

        origin = resolve_camo(url)
        note = f" (via camo -> {origin})" if origin != url else ""

        if dry_run:
            print(f"    would fetch {url}{note}")
            rewrites[url] = None
            continue

        try:
            data, content_type, retry_note = download_with_retry(origin)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as error:
            failures.append((markdown_path, url, str(error)))
            print(f"    FAILED  {url}\n            {error}")
            rewrites[url] = None  # counted as attempted; None means "leave the link alone"
            continue

        if not data:
            failures.append((markdown_path, url, "empty response"))
            print(f"    FAILED  {url}\n            empty response")
            rewrites[url] = None
            continue

        name = filename_for(origin, content_type, taken)
        with open(os.path.join(post_dir, name), "wb") as handle:
            handle.write(data)

        rewrites[url] = name
        print(f"    saved   {name}  <- {origin}  ({len(data):,} bytes){retry_note}")

    if dry_run or not any(rewrites.values()):
        return len(rewrites), failures

    def replace(match):
        name = rewrites.get(match.group("url"))
        if not name:
            return match.group(0)
        return f'![{match.group("alt")}]({name}{match.group("title") or ""})'

    with open(markdown_path, "w", encoding="utf-8") as handle:
        handle.write(IMAGE_RE.sub(replace, text))

    return len(rewrites), failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="report what would be downloaded, change nothing")
    parser.add_argument("--content-dir", default=CONTENT_DIR, help="content directory to scan")
    args = parser.parse_args()

    markdown_files = []
    for root, _dirs, files in os.walk(args.content_dir):
        markdown_files.extend(os.path.join(root, f) for f in files if f.endswith(".md"))

    total, all_failures = 0, []
    for path in sorted(markdown_files):
        with open(path, encoding="utf-8") as handle:
            if not IMAGE_RE.search(handle.read()):
                continue
        print(f"\n{os.path.relpath(path, os.path.dirname(args.content_dir))}")
        count, failures = process(path, args.dry_run)
        total += count
        all_failures.extend(failures)

    print(f"\n{'Would localize' if args.dry_run else 'Localized'} {total - len(all_failures)} of {total} remote image(s).")

    if all_failures:
        print(f"\n{len(all_failures)} failed and were left as remote links:")
        kinds = set()
        for path, url, error in all_failures:
            kind = classify(error)
            kinds.add(kind)
            rel = os.path.relpath(path, os.path.dirname(args.content_dir))
            print(f"  {rel}\n    {url}\n    [{kind}] {error}")

        print()
        for kind in sorted(kinds):
            print(DIAGNOSIS[kind])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
