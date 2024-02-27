---
title: Spam Detection and Analysis (Part 1 - Parsing)
date: 2019-04-19 01:24:59

tags:
    - Python
    - R
    - Regression
    - Analysis
    - Parsing
    - BeautifulSoup, 
    - Spam
    - Email
    - HTML
categories:
  - Data
  - Python
keywords: Python,R,Regression,detection,analysis, parsing, BeautifulSoup, spam, email
description: Spam is still a common attack method. Most of the email services have spam filters that can help us block and filter out most of the emails with commercial, fraudulent and malicious content. The purpose of the project is to explore and analyze the email header to identify the features that can tell us which emails are malicious.
image: 5cd50420b955f.png

---



Spam is still a common attack method. Most of the email services have spam filters that can help us block and filter out most of the emails with commercial, fraudulent and malicious content. The purpose of the project is to explore and analyze the email header to identify the features that can tell us which emails are malicious.
<!-- more -->

## Get Email Header information

First thing we need to do is the get the data. Email Header contents a lots of information that usually a email client do not show that to the users. However, most of those informations reveal more information about the sender. Therefore, we need to get Email Headers and parsing them for analysis.
I use Python's ```imaplib``` library to get email headers from my Gmail account Spam folder.
> For the script to work, Gmail IMAP Access need to be enabled. To enable IMAP for Gmail, please check this [instruction](https://support.google.com/mail/answer/7126229). You also need to either turn off 2-Step Verification for your Google account or set up an app password [here](https://myaccount.google.com/u/1/security).

### Setup connection

1. Import the required libraries.

```python
import getpass
import imaplib
import email
from email.parser import HeaderParser
from email.header import decode_header
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
```

2. Login to the Gmail

```python
print('Email:')
un = input()
print('Password')
pw = getpass.getpass() # hide passowrad with getpass() function.
conn = imaplib.IMAP4_SSL(port = '993',host = 'imap.gmail.com')
conn.login(un,pw)
```

### Download Email and Parsing Email Header

1. Get email list.

```python
conn.select('[Gmail]/Spam') # Get email form spam folder.
type, emaildata = conn.search(None, 'ALL')
emaillist=emaildata[0].split() # Get email list.
parser = HeaderParser()
header_list=[]
msg_text=[]

# Read API key for ipstack.com from key.txt file.
key_f=open("key.txt","r")
key=key_f.readlines()[0]
```
2. Parsing email


Usually an email header looks like this:
<img src='https://ws4.sinaimg.cn/large/006tNc79ly1g28pgwknggj30lo0ca75r.jpg' width="600" />
What we want are:
|Name|Description|
|--|--|
|   ```Subject```| The Subject of Email  |
| ```Reply-To```| The reply address that when you click reply button in you Email client  |
| ```Return-Path```|  The reply address that when you click reply button in you Email client |
| ```IP``` |  The sender's IP address |
| ```Received Time```| When is the email received |
| ```From```| The senders's address  |
| ```Date```| The date the message was sent|
| ```Content-Type```| Indicated what contents in the email |
|  ```Message``` | The email content |
|  ```DMARC``` |  Domain-Based Message Authentication Reporting and Conformance |
|  ```DKIM``` |  Domain Keys Identified Mail |
|  ```ARC-Authentication-Results``` | Authenticated Received Chain  |
|  ```SPF``` |  Sender Policy Framework |


Now we need to parse each email in the emaillist by using for loop.
```python
for a in emaillist:
    type, emaildata2 = conn.fetch(a, '(RFC822)')
    h = parser.parsestr(emaildata2[0][1].decode('utf-8','ignore'))
```
Some emails have an html format message. The html tags are not helping us in this project. Therefore, we can use ```BeautifulSoup``` to get text from the email message.

```python
    for txt in h.walk():
        if not txt.is_multipart():
            msg_text = txt.get_payload(decode=True).decode('utf-8','ignore')
    soup = BeautifulSoup(msg_text, "lxml")
    msg_text= soup.get_text(strip=True)
```
Most information is clear and do not need clean and edit.
```python
    header = {}
    header['Subject']=decode_header(h['Subject'])[0][0]
    header['ARC-Authentication-Results']=h['ARC-Authentication-Results'].strip()
    header['Return-Path']=h['Return-Path'].strip()
    header['Return-Path Address']=re.findall(r'\b@\S*\b', str(h['Return-Path'].strip()))[0]
    header['Received']=h['Received'].strip()
    header['Received-SPF']=h['Received-SPF'].strip()
    header['Date']=pd.to_datetime(h['Date'].strip())
    if 'Reply-To' in h:
        header['Reply-To']=h['Reply-To'].strip()
        header['Reply-To Address']=re.findall(r'\b@\S*\b', str(h['Reply-To'].strip()))[0]
    else:
        header['Reply-To']=''
        header['Reply-To Address']=''
    header['Content-Type']=h['Content-Type'].strip().split(';')[0]
    header['From']=h['From'].strip()
```
However, for the data contents many irrelevant information and need to be cleaned. I use Regular expression operations to extract only useful information.
```python
    if re.findall(r'\b@\S*\b',str(h['From'].strip())):
        header['From Address']=re.findall(r'\b@\S*\b',str(h['From'].strip()))[0]
    else:
        header['From Address']=''
    #header['Sender-ip']= re.findall(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',str(header))
    header['Message']= len(msg_text)
    if re.findall(r'\bip=\S*\b',str(header)):
        header['IP']=re.findall(r'\bip=\S*\b',str(header))[0].split('=')[1]
    else:
        header['IP']=''
    if re.findall(r'\bspf=\S*\b',str(header)):
        header['SPF']=re.findall(r'\bspf=\S*\b',str(header))[0].split('=')[1]
    else:
        header['SPF']=''
    if re.findall(r'\bdmarc=\S*\b',str(header)):
        header['DMARC']=re.findall(r'\bdmarc=\S*\b',str(header))[0].split('=')[1]
    else:
        header['DMARC']=''
    if re.findall(r'\bdkim=\S*\b',str(header)):
        header['DKIM']=re.findall(r'\bdkim=\S*\b',str(header))[0].split('=')[1]
    else:
        header['DKIM']=''
```
I use the api of ipstack.com to convert IP to geographic location.
```python
    address = "http://api.ipstack.com/"+header['IP']+"?access_key="+key    
    response = requests.get(address)
    ipjason = response.text
    iplist = json.loads(ipjason)
    header['Country']= iplist.get('country_name')
    header['Regin']= iplist.get('region_name')
    header['City']= iplist.get('city')
    if iplist.get('type')== 'ipv6' :
        header['IPv6 Indicator']= 1
    elif iplist.get('type')== 'ipv4' :
        header['IPv6 Indicator']= 0
    header_list.append(header)

    # For Loop END
```

For consistent analysis, I save the DataFrame into a CSV file for further analysis.

```python
keys = header_list[0].keys()
print('File Name:')
fn = input()
with open(fn+'.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(header_list)
```
> This is the Part 1 of the series. For how to user R analysis the email, please check [Part 2](/p/spam-detection-and-analysis-part-2-analysis-with-r/)
