import argparse
import requests
import time
import pandas as pd
from xml.etree import ElementTree

def get_wishlist(username):
    """
    params - username: str
    return - wishlist: [int]
    """
    status = 0
    url = "https://www.boardgamegeek.com/xmlapi2/collection?username={}&brief=1&wishlist=1".format(username)

    while status != 200:
        r = requests.get(url)
        status = r.status_code
        time.sleep(2)
    
    root = ElementTree.fromstring(r.content)
    items = []
    for child in root:
        if child.attrib['subtype'] == 'boardgame':
            items.append(child.attrib['objectid'])
    
    print('Found {} items in wishlist'.format(len(items)))
    return items

def fetch_bgg(game):

    fields = {}

    print("Fetching data for game {}".format(game))
    url = """https://www.boardgamegeek.com/xmlapi2/thing?id={}
            &versions=1
            &videos=1
            &stats=1
            &marketplace=1
            &ratingcomments=1&pagesize=100&page=1""".format(game)
    
    r = requests.get(url)
    root = ElementTree.fromstring(r.content)[0]
    assert root.get('id') == str(game)

    fields['Name'] = root.find('name').get('value')
    fields['Min Players'] = root.find('minplayers').get('value')
    fields['Max Players'] = root.find('maxplayers').get('value')
    fields['Play Time'] = root.find('playingtime').get('value')
    
    cats = []
    mechs = []
    for link in root.findall('link'):
        if link.get('type') == 'boardgamecategory':
            cats.append(link.get('value'))
        elif link.get('type') == 'boardgamemechanic':
            mechs.append(link.get('value'))
    fields['Categories'] = cats
    fields['Mechanics'] = mechs

    ratings = root.find('statistics').find('ratings')
    fields['Num Ratings'] = ratings.find('usersrated').get('value')
    fields['Avg Rating'] = ratings.find('average').get('value')
    fields['Weight'] = ratings.find('averageweight').get('value')

    for rank in ratings.find('ranks').findall('rank'):
        if rank.get('name') == 'boardgame':
            fields['Rank'] = rank.get('value')
        if rank.get('name') == 'strategygames':
            fields['Strategy Rank'] = rank.get('value')

    return fields

def get_gamedata(game):
    """

    """      
    bgg_row = fetch_bgg(game)
    
    #TODO: get geekmarket/bgp price and reddit rank
    #reddit_row = fetch_reddit(game)
    #bgp_row = fetch_price(game):
    return bgg_row


def save_list(data):
    df = pd.DataFrame(data)
    df.to_csv('file.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'BGG username')
    parser.add_argument('username')
    args = parser.parse_args()

    wishlist = get_wishlist(args.username)
    data = []
    for game in wishlist:
        data.append(get_gamedata(game))
    save_list(data)
