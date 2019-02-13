#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import re
import ssl

import feedparser

cleanr = re.compile('&nbsp;|<.*?>')
def remove_html(raw_html):
    return re.sub(cleanr, '', raw_html)
def remove_empty_lines(raw_text):
    return "\n".join([ll.rstrip() for ll in raw_text.splitlines() if ll.strip()])
def clean_summary(summary):
    return remove_empty_lines(remove_html(summary))


pp = pprint.PrettyPrinter()
# pttrn = re.compile("Train.*(523|542)", flags=re.IGNORECASE)
pttrn = re.compile("systemwide", flags=re.IGNORECASE)

# https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# https://www.pythonforbeginners.com/feedparser/using-feedparser-in-python
url = 'https://public.govdelivery.com/topics/CACCTRAN_2/feed.rss'
feed = feedparser.parse(url)
for entry in feed.get("entries"):
    if pttrn.search(entry.get("summary")):
        print(entry.get("published_parsed"))  #time.struct_time
        summary = clean_summary(entry.get("summary"))
        print(summary)


       # TODO sometimes strings have html in them, sometimes they have \xa0
       # https://stackoverflow.com/questions/26068832/how-to-remove-this-xa0-from-a-string-in-python

# https://stackoverflow.com/questions/22211795/python-feedparser-how-can-i-check-for-new-rss-data
last_etag = feed.get("etag")
last_modified = feed.get("headers").get("Last-Modified")
feed_update = feedparser.parse(url, etag=last_etag, modified=last_modified)
if feed_update.status == 304:
    print("No change")

print(feed_update.status)