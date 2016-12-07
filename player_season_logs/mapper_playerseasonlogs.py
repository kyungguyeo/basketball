#!/usr/bin/env python

import sys, requests
from bs4 import BeautifulSoup

for url in sys.stdin:
    url = url.strip()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
        print "%s\t%s" % ('http://www.basketball-reference.com' + players.find('a')['href'], \
                          players.find('a')['href'].split('/')[-1])