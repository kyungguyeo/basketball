#!/usr/bin/env python

import sys

for url in sys.stdin:
    url = url.strip()
    print "%s\t%d" % (url, 1)