import datetime.datetime

currentdate = datetime.datetime(day=1, month=1, year=1953)
enddate = datetime.datetime.now()
all_boxscore_urls = []
while currentdate < enddate:
    all_boxscore_urls.append('http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
                             (currentdate.month, currentdate.day, currentdate.year))
    currentdate += datetime.timedelta(days=1)

with open('boxscore_urls.txt','w') as file:
    for url in all_boxscore_urls:
        file.write(url + '\n')
    file.close()


letters = map(chr, range(97, 123))
letters.remove('x')
with open('player_urls.txt', 'w') as file:
    for letter in letters:
        file.write('http://www.basketball-reference.com/players/' + letter + '\n')
    file.close()

with open('seasonstanding_urls.txt', 'w') as file:
    for i in range(1971, 2017):
        file.write('http://www.basketball-reference.com/leagues/NBA_%s.html' % (i) + '\n')
    file.close()