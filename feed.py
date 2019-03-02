#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ssl
from datetime import datetime
from time import mktime

import feedparser
from dateutil import tz

### TEXT CLEANING HELPERS ######################################################
html_tag = re.compile('<.*?>')
html_entitites = {
    '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
    '&lt;'   : '<', '&gt;'  : '>'
}

def clean_summary(raw_text):
    # Remove HTML tags.
    raw_text = re.sub(html_tag, '', raw_text)
    # Remove HTML entities.
    for (k, v) in html_entitites.items():
        raw_text = raw_text.replace(k, v)
    # Remove whitespace characters (space, tab, newline, return, formfeed).
    return " ".join(raw_text.split())
### TIME CONSTANTS #############################################################
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
################################################################################

# https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# https://www.pythonforbeginners.com/feedparser/using-feedparser-in-python
# https://stackoverflow.com/questions/22211795/python-feedparser-how-can-i-check-for-new-rss-data

pttrn = re.compile("systemwide|Train.*(523|542)", flags=re.IGNORECASE)
url = 'https://public.govdelivery.com/topics/CACCTRAN_2/feed.rss'

last_etag = None
last_modified = None
feed = feedparser.parse(url, etag=last_etag, modified=last_modified)

last_etag = feed.get("etag")
last_modified = feed.get("headers").get("Last-Modified")
if feed.status == 304:
    print("No change.")

for entry in feed.get("entries"):
    summary = clean_summary(entry.get("summary"))
    if pttrn.search(summary):
        # https://stackoverflow.com/questions/1697815/how-do-you-convert-a-python-time-struct-time-object-into-a-datetime-object
        # https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime-with-python
        struct = entry.get("published_parsed")
        utc = datetime.fromtimestamp(mktime(struct)).replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        print(local.strftime("%a %b %d %-I:%M %p"))
        print(summary)
  
    # TODO sometimes strings have html in them, sometimes they have \xa0
    # https://stackoverflow.com/questions/26068832/how-to-remove-this-xa0-from-a-string-in-python

# TODO locally store last_etag & last_modified
# with open('results.txt', 'w') as outfile:
#     json.dump(feed_info, outfile, indent=4, ensure_ascii=False)
