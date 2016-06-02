import urllib2
from bs4 import BeautifulSoup

#Using Steph Curry as an example
response = urllib2.urlopen('http://www.basketball-reference.com/players/c/curryst01.html')
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
print colnames

#Season-by-season numbers
rows = {}
for season in season_data.find_all('tr', id=lambda x: x and x.startswith('totals.')):
	rows[season.attrs['id']] = []
	for row in season_data.find(id=season.attrs['id']).find_all('td'):
		rows[season.attrs['id']].append(row.text)
