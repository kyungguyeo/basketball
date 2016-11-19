import urllib2
from bs4 import BeautifulSoup
from pyspark import SparkContext, SparkConf

def player_scrape_by_season(soup):
    """
    Scrapes a player's season-by-season per-game stats
    """
    #Grab Per-Game Numbers
    all_seasonlogs = {}
    season_per_game = soup.find(id='all_per_game').find_all("tr")
    for season in season_per_game:
        if season.has_attr('id'):
            date = iter(season).next().getText() #To get the season year
            all_seasonlogs[date] = {}
            for data in season:
                all_seasonlogs[date][data["data-stat"]] = data.getText() #get all stats of gamelog
    return all_seasonlogs


def player_game_log_scrape(soup):
    """
    Scrape the player's game logs, return a dictionary with (key, val) => (game, stats)
    """
    all_gamelogs = {}
    gamelogs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
    all_logs = []
    for logs in gamelogs:
        all_logs.append('http://www.basketball-reference.com' + logs['href']) #grab all game log links of player
    for season_logs in all_logs:
        response = urllib2.urlopen(season_logs)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html, 'html.parser')
        logs = soup.find("div", class_="table_outer_container").find("tbody").find_all("tr")
        counter = 0
        for log in logs:
            if log.has_attr('id'):
                if int(log['id'].split('.')[1]) != 0:
                    date = log.find("td",{"data-stat":"date_game"}).getText()
                    all_gamelogs[date] = {}
                    for data in log:
                        all_gamelogs[date][data["data-stat"]] = data.getText() #get all stats of gamelog
    return all_gamelogs

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
        losing_team = score.find("tr",class_="loser").findChildren()[0].getText()
        losing_score = score.find("tr",class_="loser").findChildren()[2].getText()
        winning_team = score.find("tr",class_="winner").findChildren()[0].getText()
        winning_score = score.find("tr",class_="winner").findChildren()[2].getText()
        all_game_scores[score.find_all("a")[1]['href'][11:-5]] = (winning_team, losing_team, winning_score, losing_score) #super hard-coded way to get unique id of each game
    return all_game_scores

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
        teamname = team.find(attrs={'data-stat':"team_name"}).getText()
        teamwins = team.find(attrs={'data-stat':"wins"}).getText()
        teamlosses = team.find(attrs={'data-stat':"losses"}).getText()
        all_season_standings[teamname] = (teamwins, teamlosses)
    return all_season_standings

if __name__ == "__main__":
    conf = SparkConf().setAppName("Bball_stat_crawler")
    sc = SparkContext(conf=conf)
    player_data = {}
    letters=map(chr, range(97, 123))
    #Grab Player GameLogs
    url = 'http://www.basketball-reference.com/players/a/acyqu01.html'
    test_url = 'http://www.basketball-reference.com/boxscores/index.cgi?month=11&day=2&year=1946'
    standings_url = 'http://www.basketball-reference.com/leagues/NBA_1950.html'
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    player_game_log_scrape(soup)
    player_scrape_by_season(soup)
    box_score_scrape(test_url)


    ####Spark Stuff########

    ##Parallizing player_scrape_by_season
    for letter in letters:
        response = urllib2.urlopen('http://www.basketball-reference.com/players/'+ letter)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html, 'html.parser')
        for active_players in soup.find_all('strong'):
            print 'scraping data for ' + active_players.text + '...'
            url = 'http://www.basketball-reference.com'+ active_players.find('a').attrs['href']
            player_urls.append(url)
    player_url_parlzd = sc.parallelize(player_urls)
    player_url_parlzd.map(lambda x: Player_Scrape_by_Season(x))
    player_url_parlzd.map(lambda x: Player_Game_Log_Scrape(x))

