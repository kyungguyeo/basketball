from bs4 import BeautifulSoup
from pyspark import SparkContext, SparkConf
import datetime, urllib2, requests, unicodedata, re, pandas


def player_scrape_by_season(url):
    """
    Scrapes a player's season-by-season per-game stats
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_seasonlogs = {}
    filename = url.strip(".html").split("/")[-1] + '_seasonlogs.csv'
    season_per_game = soup.find(id='all_per_game').find_all("tr")
    for season in season_per_game:
        if season.has_attr('id'):
            date = iter(season).next().getText()  # To get the season year
            all_seasonlogs[date] = {}
            for data in season:
                all_seasonlogs[date][data["data-stat"]] = data.getText()  # get all stats of gamelog
    final_df = pandas.DataFrame.from_dict(all_seasonlogs, orient='index')
    player_name = soup.find('h1').getText()
    final_df['player_name'] = player_name
    return final_df, filename


def player_game_log_scrape(url):
    """
    Scrape the player's game logs, return a dictionary with (key, val) => (game, stats)
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_game_logs = {}
    filename = url.strip(".html").split("/")[-1] + '_gamelogs.csv'
    game_logs = soup.find("li", class_="full hasmore ").find_all("a", href=True)
    player_name = soup.find('h1').getText()
    all_logs = []
    for logs in game_logs:
        all_logs.append('http://www.basketball-reference.com' + logs['href'])  # grab all game log links of player
    for season_logs in all_logs:
        try:
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
        except:
            pass
    final_df = pandas.DataFrame.from_dict(all_game_logs, orient='index')
    final_df['player_name'] = player_name
    return final_df, filename


def box_score_scrape(url):
    """
    Scrape every boxscore for the particular day on basketball-reference
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_game_scores = {}
    filename = ''.join(re.findall(r'\d+', url)) + '.csv'  # MONTHDAYYEAR FORMAT
    date = re.findall(r'\d+', url)
    date = ['0' + i if len(i)<2 else i for i in date]
    date = '-'.join((date[2],date[0],date[1]))
    game_scores = soup.find_all("div", class_='game_summary expanded nohover')
    for score in game_scores:
        losing_team = score.find("tr", class_="loser").findChildren()[0].getText()
        losing_score = score.find("tr", class_="loser").findChildren()[2].getText()
        winning_team = score.find("tr", class_="winner").findChildren()[0].getText()
        winning_score = score.find("tr", class_="winner").findChildren()[2].getText()
        all_game_scores[score.find_all("a")[1]['href'][11:-5]] = (
        winning_team, losing_team, winning_score, losing_score)  # super hard-coded way to get unique id of each game
    final_df = pandas.DataFrame.from_dict(all_game_scores, orient='index')
    final_df['gamedate'] = date
    return final_df, filename


def season_standings_scrape(url):
    """
    Scrape season standings for that particular season
    """
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html, 'html.parser')
    all_season_standings = {}
    filename = re.findall(r'\d+', url)[0] + 'seasonstandings.csv'
    standings_e = soup.find(id='all_divs_standings_E').find("tbody").find_all("tr", class_="full_table")
    standings_w = soup.find(id='all_divs_standings_W').find("tbody").find_all("tr", class_="full_table")
    for team in (standings_e + standings_w):
        team_name = team.find(attrs={'data-stat': "team_name"}).getText()
        team_name = ' '.join(unicodedata.normalize("NFKD", team_name).split(' ')[:-2]).strip('*')
        team_wins = team.find(attrs={'data-stat': "wins"}).getText()
        team_losses = team.find(attrs={'data-stat': "losses"}).getText()
        all_season_standings[team_name] = (team_wins, team_losses)
    final_df = pandas.DataFrame.from_dict(all_season_standings, orient='index').reset_index()
    final_df['year'] = re.findall(r'\d+', url)[0]
    final_df.columns = ['team','wins','losses','season_year']
    return final_df, filename

if __name__ == "__main__":
    conf = SparkConf().setAppName("Bball_stat_crawler")
    sc = SparkContext(conf=conf)

    # Aggregate player urls for player_scrape_by_season
    letters = map(chr, range(97, 123))
    letters.remove('x')
    player_urls = []
    for letter in letters:
        response = requests.get('http://www.basketball-reference.com/players/' + letter)
        soup = BeautifulSoup(response.content, 'html.parser')
        for players in soup.find('tbody').find_all(attrs={'data-stat': 'player'}):
            url = 'http://www.basketball-reference.com' + players.find('a')['href']
            player_urls.append(url)

    player_url_par = sc.parallelize(player_urls)

    # Grab Player Season Data
    player_season_data = player_url_par.flatMap(lambda x: player_scrape_by_season(x)).collect()
    for i in [i for i in range(len(player_season_data)) if i % 2 == 0]:
        path = '/root/playerseasonlogs/' + player_season_data[i+1]
        player_season_data[i].to_csv(path, index=False)

    # Grab Player Game Log Data
    player_game_log_data = player_url_par.flatMap(lambda x: player_game_log_scrape(x)).collect()
    for i in [i for i in range(len(player_season_data)) if i % 2 == 0]:
        path = '/root/playergamelogs/' + player_game_log_data[i+1]
        player_game_log_data[i].to_csv(path, index=False)

    # Aggregate boxscore urls for box_score_scrape
    currentdate = datetime.datetime(day=2, month=11, year=1946)
    enddate = datetime.datetime.now()
    all_boxscore_urls = []
    while currentdate < enddate:
        all_boxscore_urls.append('http://www.basketball-reference.com/boxscores/index.cgi?month=%s&day=%s&year=%s' % \
                                 (currentdate.month, currentdate.day, currentdate.year))
        currentdate += datetime.timedelta(days=1)

    # Grab Boxscore Data
    boxscore_url_par = sc.parallelize(all_boxscore_urls)
    boxscore_data = boxscore_url_par.flatMap(lambda x: box_score_scrape(x)).collect()
    for i in [i for i in range(len(boxscore_data)) if i % 2 == 0]:
        path = '/root/gamescores/' + boxscore_data[i+1]
        if boxscore_data[i].empty == 0:
            boxscore_data[i].to_csv(path, index=False)

    # Aggregate standings urls for season_standings_scrape
    all_standings_urls = []
    for i in range(1971, 2016):
        all_standings_urls.append('http://www.basketball-reference.com/leagues/NBA_%s.html' % (i))

    # # Grab Season Standings Data
    standings_url_par = sc.parallelize(all_standings_urls)
    season_standings_data = standings_url_par.flatMap(lambda x: season_standings_scrape(x)).collect()
    for i in [i for i in range(len(season_standings_data)) if i % 2 == 0]:
        path = '/root/seasonstandings/' + season_standings_data[i+1]
        season_standings_data[i].to_csv(path, index=False)
