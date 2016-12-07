#!/usr/bin/env python

import sys, urllib2
from bs4 import BeautifulSoup

for url in sys.stdin:
    url = url.strip()
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
        url = 'http://www.basketball-reference.com' + players.find('a')['href']
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html, 'html.parser')
        game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
        for game_log in game_logs:
            print "%s\t%s" % ('http://www.basketball-reference.com' + game_log['href'],
                              ''.join(game_log['href'].split('/')[-3:]) + '.html')