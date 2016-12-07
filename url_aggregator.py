import datetime.datetime

currentdate = datetime.datetime.now()
enddate = datetime.datetime(day=15, month=12, year=1957)
all_boxscore_urls = []
while currentdate > enddate:
    all_boxscore_urls.append('http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
                             (currentdate.month, currentdate.day, currentdate.year))
    currentdate -= datetime.timedelta(days=1)

with open('urls/boxscore_urls.txt','w') as file:
    for url in all_boxscore_urls:
        file.write(url + '\n')
    file.close()


letters = map(chr, range(97, 123))
letters.remove('x')
with open('urls/player_urls.txt', 'w') as file:
    for letter in letters:
        file.write('http://www.basketball-reference.com/players/' + letter + '\n')
    file.close()

with open('urls/seasonstanding_urls.txt', 'w') as file:
    for i in range(1971, 2017):
        file.write('http://www.basketball-reference.com/leagues/NBA_%s.html' % (i) + '\n')
    file.close()