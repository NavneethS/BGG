'''
Available rankings :
Overall
Thematic
Strategy
War
Customizable
Abstract
Family
Party
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd

def getpage(url):
    r = requests.get(url)
    return r.text

class GameList:
    def __init__(self, ranklist):
        if ranklist == 'strategy':
            self.baseurl = 'https://boardgamegeek.com/strategygames/browse/boardgame'
        elif ranklist == 'overall':
            self.baseurl = 'https://boardgamegeek.com/browse/boardgame'
        
    def getgames(self, threshold, page):
        self.games = []

        pagehtml = getpage(self.baseurl + '/page/' + str(page))
        parsed = BeautifulSoup(pagehtml, "html5lib")
        table = parsed.find('table', {'class':'collection_table'})

        rows = table.find_all('tr')
        for row in rows:
            if row.attrs.get('id')=='row_':
                rankcell = row.find('td', 'collection_rank')
                rank = int(rankcell.text)

                gamecell = row.find('td', 'collection_objectname')
                game = gamecell.find('a', href=True)
                title = game.text
                gameid = game['href'].split('/')[2]
                shortname = game['href'].split('/')[3]

                ratingcells = row.find_all('td', 'collection_bggrating')
                geekrating = float(ratingcells[0].text)
                avgrating = float(ratingcells[1].text)
                numvoters = int(ratingcells[2].text)
            
                self.games.append({'rank': rank,
                                'title': title,
                                'shortname': shortname,
                                'gameid': gameid,
                                'geekrating': geekrating,
                                'avgrating': avgrating,
                                'numvoters': numvoters})
                

    def load(self, filename):
        pass

    def save(self, filename):
        df = pd.DataFrame(self.games)
        df.to_csv(filename)
    
    def update(self, filename):
        pass


if __name__ == '__main__':
    gamelist = GameList('strategy')
    gamelist.getgames(threshold=7, page=1)
    print(gamelist.games)

