from bs4 import BeautifulSoup
import datetime, json, urllib2
from pyspark import SparkContext, SparkConf


def player_scrape_by_season(url):
    """
    Scrapes a player's season-by-season per-game stats
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_seasonlogs = {}
    season_per_game = soup.find(id='all_per_game').find_all("tr")
    for season in season_per_game:
        if season.has_attr('id'):
            date = iter(season).next().getText()  # To get the season year
            all_seasonlogs[date] = {}
            for data in season:
                all_seasonlogs[date][data["data-stat"]] = data.getText()  # get all stats of gamelog
    filename = url.strip(".html").split("/")[-1] + '.json'
    if 'local' in sc.getConf().get('spark.master'):
        path = '/Users/johnnyyeo/Desktop/' + filename
        with open(path, 'w') as fp:
            json.dump(all_seasonlogs, fp)
    else:
        # path = hdfs://path_to_hdfs_dir + filename
        # with open(path, 'w') as fp:
        # json.dump(all_seasonlogs, fp)

def player_game_log_scrape(url):
    """
    Scrape the player's game logs, return a dictionary with (key, val) => (game, stats)
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_game_logs = {}
    game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
    all_logs = []
    for logs in game_logs:
        all_logs.append('http://www.basketball-reference.com' + logs['href'])  # grab all game log links of player
    for season_logs in all_logs:
        response = urllib2.urlopen(season_logs)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html, 'html.parser')
        logs = soup.find("div", class_="table_outer_container").find("tbody").find_all("tr")
        for log in logs:
            if log.has_attr('id'):
                if int(log['id'].split('.')[1]) != 0:
                    date = log.find("td", {"data-stat": "date_game"}).getText()
                    all_game_logs[date] = {}
                    for data in log:
                        all_game_logs[date][data["data-stat"]] = data.getText()  # get all stats of gamelog
    filename = url.strip(".html").split("/")[-1] + '.json'
    if 'local' in sc.getConf().get('spark.master'):
        path = '/Users/johnnyyeo/Desktop/' + filename
        with open(path, 'w') as fp:
            json.dump(all_game_logs, fp)
    else:
        # path = hdfs://path_to_hdfs_dir + filename
        # with open(path, 'w') as fp:
        #     json.dump(all_game_logs, fp)


def box_score_scrape(url):
    """
    Scrape every boxscore for the particular day on basketball-reference
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_game_scores = {}
    game_scores = soup.find_all("div", class_='game_summary expanded nohover')
    for score in game_scores:
        losing_team = score.find("tr", class_="loser").findChildren()[0].getText()
        losing_score = score.find("tr", class_="loser").findChildren()[2].getText()
        winning_team = score.find("tr", class_="winner").findChildren()[0].getText()
        winning_score = score.find("tr", class_="winner").findChildren()[2].getText()
        all_game_scores[score.find_all("a")[1]['href'][11:-5]] = (
        winning_team, losing_team, winning_score, losing_score)  # super hard-coded way to get unique id of each game
    filename = re.findall(r'\d+', url) + '.json' MONTHDAYYEAR FORMAT
    if 'local' in sc.getConf().get('spark.master'):
        path = '/Users/johnnyyeo/Desktop/' + filename
        with open(path, 'w') as fp:
            json.dump(all_game_scores, fp)
    else:
        # path = hdfs://path_to_hdfs_dir + filename
        # with open(path, 'w') as fp:
        #     json.dump(all_game_scores, fp)

def season_standings_scrape(url):
    """
    Scrape season standings for that particular season
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_season_standings = {}
    standings = soup.find(id='all_divs_standings_').find("tbody").find_all("tr", class_="full_table")
    for team in standings:
        team_name = team.find(attrs={'data-stat': "team_name"}).getText().strip("*")
        team_wins = team.find(attrs={'data-stat': "wins"}).getText()
        team_losses = team.find(attrs={'data-stat': "losses"}).getText()
        all_season_standings[team_name] = (team_wins, team_losses)
    filename = re.findall(r'\d+', url) + '.json'
    if 'local' in sc.getConf().get('spark.master'):
        path = '/Users/johnnyyeo/Desktop/' + filename
        with open(path, 'w') as fp:
            json.dump(all_season_standings, fp)
    else:
        # path = hdfs://path_to_hdfs_dir + filename
        # with open(path, 'w') as fp:
        #     json.dump(all_season_standings, fp)

if __name__ == "__main__":
    conf = SparkConf().setAppName("Bball_stat_crawler")
    sc = SparkContext(conf=conf)

    # Aggregate player urls for player_scrape_by_season
    letters = map(chr, range(97, 123))
    player_urls = []
    for letter in letters:
        response = urllib2.urlopen('http://www.basketball-reference.com/players/' + letter)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html, 'html.parser')
        for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
            url = 'http://www.basketball-reference.com' + players.find('a')['href']
            player_urls.append(url)

    # Aggregate boxscore urls for box_score_scrape
    currentdate = datetime.datetime(day=2, month=11, year=1946)
    enddate = datetime.datetime.now()
    all_boxscore_urls = []
    while currentdate < enddate:
        all_boxscore_urls.append('http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
                                 (currentdate.month, currentdate.day, currentdate.year))
        currentdate += datetime.timedelta(days=1)

    # Aggregate standings urls for season_standings_scrape
    all_standings_urls = []
    for i in range(1950, 2017):
        all_standings_urls.append('http://www.basketball-reference.com/leagues/NBA_%s.html' % (i))

    # Spark Stuff
    # player_url_par = sc.parallelize(player_urls)
    # player_url_par.map(lambda x: player_scrape_by_season(x))
    # player_url_par.map(lambda x: player_game_log_scrape(x))
    #
    # boxscore_url_par = sc.parallelize(all_boxscore_urls)
    # boxscore_url_par.map(lambda x: box_score_scrape(x))

    standings_url_par = sc.parallelize(all_standings_urls)
    standings_url_par.map(lambda x: season_standings_scrape(x))