from subprocess import call
from bs4 import BeautifulSoup
import datetime, requests, urllib2, re

if __name__ == "__main__":
#     conf = SparkConf().setAppName("Url_scraper")
#     sc = SparkContext(conf=conf)
#
#     letters = map(chr, range(97, 123))
#     letters.remove('x')
#     player_urls = []
#     player_gamelog_urls = []
#     for letter in letters:
#         response = requests.get('http://www.basketball-reference.com/players/' + letter)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
#             url = 'http://www.basketball-reference.com' + players.find('a')['href']
#             player_urls.append(url)
#             # PLAYER GAMELOGS
#             response = urllib2.urlopen('http://www.basketball-reference.com' + players.find('a')['href'])
#             html = response.read()
#             response.close()
#             soup = BeautifulSoup(html, 'html.parser')
#             game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
#             for game_log in game_logs:
#                 player_gamelog_urls.append('http://www.basketball-reference.com' + game_log['href'])
#
#     def player_gamelog_htmls(url):
#         """
#         Use wget to grab .html files, then push up to hdfs
#         """
#         call(['wget', '-O', ''.join(url.split('/')[-3:]) + '.html',
#               'http://www.basketball-reference.com' + game_log['href']])
#         call(['hdfs', 'dfs', '-put', ''.join(url.split('/')[-3:]) + '.html', '/playergamelogs_raw'])
#         call(['rm', ''.join(url.split('/')[-3:]) + '.html'])
#         return 'done!'
#
#     def player_seasonlog_htmls(url):
#         """
#         Use wget to grab .html files, then push up to hdfs
#         """
#         call(['wget', '-O', url.split('/')[-1], 'http://www.basketball-reference.com' + game_log['href']])
#         call(['hdfs', 'dfs', '-put', url.split('/')[-1], '/playergamelogs_raw'])
#         call(['rm', url.split('/')[-1]])
#         return 'done!'
#
#
#     player_url_par = sc.parallelize(player_urls)
#     player_url_par.map(lambda x: player_seasonlog_htmls(x)).take(1)
#     player_gamelog_url_par = sc.parallelize(player_gamelog_urls)
#     player_gamelog_url_par.map(lambda x: player_gamelog_htmls(x)).take(1)
#
#
#     letters = map(chr, range(97, 123))
#     letters.remove('x')
#     for letter in letters:
#         response = requests.get('http://www.basketball-reference.com/players/' + letter)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
#             call(['wget','-O', players.find('a')['href'].split('/')[-1], 'http://www.basketball-reference.com' + players.find('a')['href']])
#             call(['hdfs','dfs','-put', players.find('a')['href'].split('/')[-1],'/playerseasonlogs_raw'])
#             call(['rm', players.find('a')['href'].split('/')[-1]])
#
#             # PLAYER GAMELOGS
#             response = urllib2.urlopen('http://www.basketball-reference.com' + players.find('a')['href'])
#             html = response.read()
#             response.close()
#             soup = BeautifulSoup(html, 'html.parser')
#             game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
#             for game_log in game_logs:
#                 call(['wget', '-O', ''.join(game_log['href'].split('/')[-3:]) + '.html', \
#                       'http://www.basketball-reference.com' + game_log['href']])
#                 call(['hdfs','dfs','-put',''.join(game_log['href'].split('/')[-3:]) + '.html', '/playergamelogs_raw'])
#                 call(['rm', ''.join(game_log['href'].split('/')[-3:]) + '.html'])
#
#
#
#
# letters = map(chr, range(97, 123))
# letters.remove('x')
# player_urls = []
# player_gamelog_urls = []
# for letter in letters:
#     response = requests.get('http://www.basketball-reference.com/players/' + letter)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
#         url = 'http://www.basketball-reference.com' + players.find('a')['href']
#         player_urls.append(url)
#         # PLAYER GAMELOGS
#         response = urllib2.urlopen('http://www.basketball-reference.com' + players.find('a')['href'])
#         html = response.read()
#         response.close()
#         soup = BeautifulSoup(html, 'html.parser')
#         game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
#         for game_log in game_logs:
#             player_gamelog_urls.append('http://www.basketball-reference.com' + game_log['href'])
#
#     player_url_par = sc.parallelize(player_urls)
#
#
#
#     # Boxscore Data Stuff
#     currentdate = datetime.datetime(day=1, month=1, year=1953)
#     enddate = datetime.datetime.now()
#     all_boxscore_urls = []
#     while currentdate < enddate:
#         all_boxscore_urls.append('http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
#                                  (currentdate.month, currentdate.day, currentdate.year))
#         currentdate += datetime.timedelta(days=1)
#
#     def box_score_htmls(url):
#         """
#         Use wget to grab .html files, then push up to hdfs
#         """
#         date = re.findall(r'\d+', url)
#         response = urllib2.urlopen(url)
#         html = response.read()
#         response.close()
#         # call(['wget', '-O', '%s-%s-%s.html' % (date[0], date[1], date[2]), url])
#         # call(['hdfs', 'dfs', '-put', '%s-%s-%s.html' % (date[0], date[1], date[2]), 'hdfs://23.246.218.75:8020/gamescores_raw'])
#         # call(['rm', '%s-%s-%s.html' % (date[0], date[1], date[2])])
#         return html, date
#
#     boxscore_url_par = sc.parallelize(all_boxscore_urls)
#     boxscore_url_par.map(lambda x: box_score_htmls(x)).foreach().saveAsTextFile('file:///Users/johnnyyeo/Desktop')

    # For when doing locally, using pure python
    currentdate = datetime.datetime(day=13, month=10, year=1957)
    enddate = datetime.datetime.now()
    while currentdate < enddate:
        call(['wget','-O', '%s-%s-%s.html' % (currentdate.month, currentdate.day, \
            currentdate.year), 'http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
            (currentdate.month, currentdate.day, currentdate.year)])
        call(['hdfs','dfs','-put', '%s-%s-%s.html' % (currentdate.month, currentdate.day, currentdate.year), \
              '/gamescores_raw'])
        call(['rm', '%s-%s-%s.html' % (currentdate.month, currentdate.day, currentdate.year)])
        currentdate += datetime.timedelta(days=1)


    # Season Standings Stuff
    # ###Add in parallelized version
    #
    # for i in range(1971, 2017):
    #     call(['wget', '-O', 'NBA_%s.html' %(i), 'http://www.basketball-reference.com/leagues/NBA_%s.html' % (i)])
    #     call(['hdfs', 'dfs', '-put', 'NBA_%s.html' %(i), '/seasonstandings_raw'])
    #     call(['rm', 'NBA_%s.html' %(i)])