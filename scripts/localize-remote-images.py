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


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read(), response.headers.get("Content-Type", "")


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
            data, content_type = download(origin)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as error:
            failures.append((markdown_path, url, str(error)))
            print(f"    FAILED  {url}\n            {error}")
            continue

        if not data:
            failures.append((markdown_path, url, "empty response"))
            print(f"    FAILED  {url}\n            empty response")
            continue

        name = filename_for(origin, content_type, taken)
        with open(os.path.join(post_dir, name), "wb") as handle:
            handle.write(data)

        rewrites[url] = name
        print(f"    saved   {name}  <- {origin}  ({len(data):,} bytes)")

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
        for path, url, error in all_failures:
            print(f"  {os.path.relpath(path, os.path.dirname(args.content_dir))}\n    {url}\n    {error}")
        print("\nThese hosts are likely dead. Replace or remove those images by hand.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
