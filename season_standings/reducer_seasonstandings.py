#!/usr/bin/env python

import sys, urllib2, re
from subprocess import call

for line in sys.stdin:
    url, val = line.split('\t',1)
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    year = re.findall(r'\d+', url)
    with open('NBA_%s.html' %(year[0]), 'w') as file:
        file.write(html)
    call(['hdfs', 'dfs', '-put', 'NBA_%s.html' %(year[0]), '/seasonstandings_raw'])
    call(['rm', 'NBA_%s.html' %(year[0])])