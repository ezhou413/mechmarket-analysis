import requests
import pandas as pd
import numpy as np
import re
import plotly.express as px

#get client id, secret key, and password from files in keys/
with open('keys/client_id.txt', 'r') as f:
    CLIENT_ID = f.read()
with open('keys/secret_key.txt', 'r') as f:
    SECRET_KEY = f.read()
with open('keys/pw.txt', 'r') as f:
    pw = f.read()
    
#getting access token from reddit
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    "grant_type": "password", "username": "evanz711", "password": pw
}

headers = {'User-Agent': 'mechmarketanalysis/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', 
                    auth = auth, data = data, headers = headers)

TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

#prompt user for search query
#replace spaces with '+'
rawSearchQuery = input('Enter search query: ')
searchQuery = rawSearchQuery.replace(' ', '+')

data = pd.DataFrame()

res = requests.get('https://oauth.reddit.com/r/mechmarket/search.json?q=' + searchQuery + '&sort=new', 
                headers = headers, params = {'limit': '100', 'before': ''})

#empty array to assign to DataFrame
subreddit = np.array([])
title = np.array([])
contents = np.array([])

#loop through the response data for subreddit, title, and contents of post
for post in res.json()['data']['children']:
    subreddit = np.append(subreddit, post['data']['subreddit'])
    title = np.append(title, post['data']['title'])
    contents = np.append(contents, post['data']['selftext'])
    
#assign arrays to columns of the DataFrame
data = pd.DataFrame().assign(
    subreddit = subreddit,
    title = title,
    contents = contents
)

#filter posts to only include posts from r/mechmarket
data = data[data.get('subreddit') == 'mechmarket']

#function to extract location from title
def getLocation(title):
    try: 
        return re.findall(r'\[(.*?)\]', title)[0]
    except: 
        return ''
#function to extract have, returns a list of comma separated items
def getHave(title):
    try: 
        return re.findall(r'H\](.*?)\[', title)[0].strip().split(',')
    except: 
        return ''
#function to extract want, returns a list of comma separated items
def getWant(title):
    try: 
        return re.findall(r'W\](.*)', title)[0].strip().split(',')
    except: 
        return ''

#apply function and add new location column
data = data.assign(
    location = data.get('title').apply(getLocation),
    have = data.get('title').apply(getHave),
    want = data.get('title').apply(getWant)
)

#use string split to split country and state from location and create new columns in df
def getCountry(location):
    return location.split('-')[0]

def getState(location):
    try:
        return location.split('-')[1]
    except:
        return ''
        
data = data.assign(
    country = data.get('location').apply(getCountry),
    state = data.get('location').apply(getState)
)

'''
currently, data contains
columns: subreddit, title, contents, location, have, want, country, state

todo:
get products and prices from contents
collect data on all products appearing from the query and store somewhere
    still need to determine how to best store data
make plots using plotly for this data
figure out what stats to show
implement an unlikely price filter
    ie if the price is too high or too low, exclude it on the basis that its probably an error or an outlier

'''

#put data in a csv file
data.to_csv('data/' + rawSearchQuery + '.csv')
