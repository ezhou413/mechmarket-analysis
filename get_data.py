import requests
import pandas as pd
import numpy as np

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

searchPosts = pd.DataFrame()
#beforePostId = ''

for i in np.arange(1):
    res = requests.get('https://oauth.reddit.com/r/mechmarket/search.json?q=' + searchQuery + '&sort=new', 
                 headers = headers, params = {'limit': '100'})
    
    subreddit = np.array([])
    title = np.array([])
    contents = np.array([])
    id = np.array([])
    
    for post in res.json()['data']['children']:
        subreddit = np.append(subreddit, post['data']['subreddit'])
        title = np.append(title, post['data']['title'])
        contents = np.append(contents, post['data']['selftext'])
        id = np.append(id, post['kind'] + '_' + post['data']['id'])
                
    oneRun = pd.DataFrame().assign(
        subreddit = subreddit,
        title = title,
        contents = contents,
        id = id
    )
    
    searchPosts = pd.concat([searchPosts, oneRun], axis=0)
    
    #beforePostId = '\'' + id[-1] + '\''
    

# res = requests.get('https://oauth.reddit.com/r/mechmarket/search.json?q=' + searchQuery + '&sort=new', 
#                headers = headers, params = {'limit': '100', 'before': ''})

#res = requests.get('https://www.reddit.com/r/mechmarket/search.json?q=' + searchQuery, 
#                 headers = headers, params = {'limit': '100'})

# #empty array to assign to DataFrame
# subreddit = np.array([])
# title = np.array([])
# contents = np.array([])

# #loop through the response data for subreddit, title, and contents of post
# for post in res.json()['data']['children']:
#     subreddit = np.append(subreddit, post['data']['subreddit'])
#     title = np.append(title, post['data']['title'])
#     contents = np.append(contents, post['data']['selftext'])
    
# #assign arrays to columns of the DataFrame
# searchPosts = pd.DataFrame().assign(
#     subreddit = subreddit,
#     title = title,
#     contents = contents
# )

#filter posts to only include posts from r/mechmarket
searchPosts = searchPosts[searchPosts.get('subreddit') == 'mechmarket']

#put data in a csv file
searchPosts.to_csv('data/' + rawSearchQuery + '.csv')