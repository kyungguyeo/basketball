from bs4 import BeautifulSoup
from pyspark import SparkContext, SparkConf
from subprocess import call
import unicodedata, re, pandas


def player_scrape_by_season(file):
    """
    Scrapes a player's season-by-season per-game stats
    """
    html = file[0][1]
    filename = file[0][0].split('/')[-1]
    soup = BeautifulSoup(html, 'html.parser')
    all_seasonlogs = {}
    outfile = filename.strip(".html").split("/")[-1] + '_seasonlogs.csv'
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
    return final_df, outfile


def player_game_log_scrape(file):
    """
    Scrape the player's game logs, return a dictionary with (key, val) => (game, stats)
    """
    html = file[0][1]
    soup = BeautifulSoup(html, 'html.parser')
    all_game_logs = {}
    filename = file[0][0].split('/')[-1] + '.csv'
    player_name = ' '.join(soup.find('h1').getText().split(' ')[:-3])
    try:
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


def box_score_scrape(file):
    """
    Scrape every boxscore for the particular day on basketball-reference
    """
    html = file[0][1]
    filename = file[0][0].split('/')[-1]
    soup = BeautifulSoup(html, 'html.parser')
    all_game_scores = {}
    date = re.findall(r'\d+', filename)
    date = ['0' + i if len(i)<2 else i for i in date]
    outfile = ''.join(date) + '_boxscore.csv'  # MONTHDAYYEAR FORMAT
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
    return final_df, outfile


def season_standings_scrape(file):
    """
    Scrape season standings for that particular season
    """
    html = file[0][1]
    filename = file[0][0].split('/')[-1]
    soup = BeautifulSoup(html, 'html.parser')
    all_season_standings = {}
    outfile = re.findall(r'\d+', filename)[0] + 'seasonstandings.csv'
    standings_e = soup.find(id='all_divs_standings_E').find("tbody").find_all("tr", class_="full_table")
    standings_w = soup.find(id='all_divs_standings_W').find("tbody").find_all("tr", class_="full_table")
    for team in (standings_e + standings_w):
        team_name = team.find(attrs={'data-stat': "team_name"}).getText()
        team_name = ' '.join(unicodedata.normalize("NFKD", team_name).split(' ')[:-2]).strip('*')
        team_wins = team.find(attrs={'data-stat': "wins"}).getText()
        team_losses = team.find(attrs={'data-stat': "losses"}).getText()
        all_season_standings[team_name] = (team_wins, team_losses)
    final_df = pandas.DataFrame.from_dict(all_season_standings, orient='index').reset_index()
    final_df['year'] = re.findall(r'\d+', filename)[0]
    final_df.columns = ['team','wins','losses','season_year']
    return final_df, outfile

if __name__ == "__main__":
    conf = SparkConf().setAppName("Bball_stat_crawler")
    sc = SparkContext(conf=conf)

    # Grab Season Standings Data
    standings_url_par = sc.wholeTextFiles("/seasonstandings_raw")
    season_standings_data = standings_url_par.flatMap(lambda x: season_standings_scrape(x)).collect()
    for i in [i for i in range(len(season_standings_data)) if i % 2 == 0]:
        path = '/root/' + season_standings_data[i + 1]
        season_standings_data[i].to_csv(path, index=False)
    call(['hdfs', 'dfs', '-put', '/root/*.csv', '/data/seasonstandings'])
    call(['rm', '-f', '*.csv'])

    # Aggregate boxscore urls for box_score_scrape
    boxscore_url_par = sc.wholeTextFiles("/gamescores_raw/*")
    boxscore_data = boxscore_url_par.flatMap(lambda x: box_score_scrape(x)).collect()
    for i in [i for i in range(len(boxscore_data)) if i % 2 == 0]:
        path = '/root/' + boxscore_data[i + 1]
        if boxscore_data[i].empty == 0:
            boxscore_data[i].to_csv(path, index=False)
    call(['hdfs', 'dfs', '-put', '/root/*.csv', '/data/gamescores'])
    call(['rm', '-f', '*.csv'])

    # Grab Player Season Data
    player_url_par = sc.wholeTextFiles("playerseasonlogs_raw/*")
    player_season_data = player_url_par.flatMap(lambda x: player_scrape_by_season(x)).collect()
    for i in [i for i in range(len(player_season_data)) if i % 2 == 0]:
        path = '/root/' + player_season_data[i + 1]
        player_season_data[i].to_csv(path, index=False)
    call(['hdfs', 'dfs', '-put', '/root/*.csv', '/data/playerseasonlogs'])
    call(['rm', '-f', '*.csv'])

    # Grab Player Game Log Data
    player_gamelog_url_par = sc.wholeTextFiles("playergamelogs_raw/*")
    player_game_log_data = player_url_par.flatMap(lambda x: player_game_log_scrape(x)).collect()
    for i in [i for i in range(len(player_game_log_data)) if i % 2 == 0]:
        path = '/root/' + player_game_log_data[i + 1]
        player_game_log_data[i].to_csv(path, index=False)
    call(['hdfs', 'dfs', '-put', '/root/*.csv', '/data/playergamelogs'])
    call(['rm', '-f', '*.csv'])


