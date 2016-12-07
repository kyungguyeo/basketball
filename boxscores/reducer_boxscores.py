import sys, urllib2, re

for line in sys.stdin:
    url, val = line.split('\t',1)
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    date = re.findall(r'\d+', url)
    with open('%s-%s-%s.html' % (date[0], date[1], date[2]), 'w') as file:
        file.write(html)