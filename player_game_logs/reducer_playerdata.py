#!/usr/bin/env python

import sys, urllib2

for line in sys.stdin:
    url, filename = line.split('\t')
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    with open(filename.strip(), 'w') as file:
        file.write(html)