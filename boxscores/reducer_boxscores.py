#!/usr/bin/env python

import sys, urllib2, re
from subprocess import

for line in sys.stdin:
    url, val = line.split('\t',1)
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    date = re.findall(r'\d+', url)
    with open('%s-%s-%s.html' % (date[0], date[1], date[2]), 'w') as file:
        file.write(html)
    call(['hdfs', 'dfs', '-put', '%s-%s-%s.html' % (date[0], date[1], date[2]), '/gamescores_raw'])
    call(['rm', '%s-%s-%s.html' % (date[0], date[1], date[2])])