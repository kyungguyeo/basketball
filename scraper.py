import urllib2
from bs4 import BeautifulSoup

####To-do's
#Create class with methods, instead of this nasty arch
#Create method to store html pages in hdfs
#Create method to store season data to msql db
#Ideas for scraping other data from html pages

def Player_Scrape_by_Season(url):
	"""
	Scrapes a player's season-by-season stats
	"""
	response = urllib2.urlopen(url)
	html = response.read()
	response.close()
	soup = BeautifulSoup(html, 'html.parser')

	##Grab Season data
	season_data = soup.find(id='all_totals')


	#Headers
	colnames = []
	for colname in season_data.find_all('th'):
		colnames.append(colname.attrs['tip'])

	colnames[0] = 'Season' #Manual Adjustments
	colnames[1] = 'Age' #Manual Adjustments
	colnames[17] = 'Effective Field Goal Percentage' #Manual Adjustments

	#Season-by-season numbers
	rows = {}
	for season in season_data.find_all('tr', id=lambda x: x and x.startswith('totals.')):
		rows[season.attrs['id']] = []
		for row in season_data.find(id=season.attrs['id']).find_all('td'):
			rows[season.attrs['id']].append(row.text)
	return rows

if __name__ == "__main__":
	player_data = {}
	letters=map(chr, range(97, 123))
	##Grab Table Columns
	response = urllib2.urlopen('http://www.basketball-reference.com/players/a/acyqu01.html')
	html = response.read()
	response.close()
	soup = BeautifulSoup(html, 'html.parser')
	season_data = soup.find(id='all_totals')
	colnames = []
	for colname in season_data.find_all('th'):
		colnames.append(colname.attrs['tip'])
	colnames[0] = 'Season' #Manual Adjustments
	colnames[1] = 'Age' #Manual Adjustments
	colnames[17] = 'Effective Field Goal Percentage' #Manual Adjustments

	##Grab Player Data
	for letter in letters:
		response = urllib2.urlopen('http://www.basketball-reference.com/players/'+ letter)
		html = response.read()
		response.close()
		soup = BeautifulSoup(html, 'html.parser')
		for active_players in soup.find_all('strong'):
			print 'scraping data for ' + active_players.text + '...'
			url = 'http://www.basketball-reference.com'+ active_players.find('a').attrs['href']
			print 'url: ' + url
			player_data[active_players.text] = Player_Scrape_by_Season(url)