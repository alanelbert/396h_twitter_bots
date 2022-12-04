import requests
import json
import sys
import time
import os

# Simple script for downloading all the tweets in the list,
# Get your bearer token from the twitter dev dashborad: https://developer.twitter.com/ (Make an account if you dont have one)
# and replace Bearer token with it. You can change the file it reads from by running it with an argument, or replacing the list1.txt with your file


# Alan - list 1
# Samuel - list 2
# Ansh - list 3
# John - list 4
# Syed - list 5



# Set this to be your bearer token
BEARER_TOKEN = """"""

RATE_LIMIT = 16 * 60 
MAX_REQ = 850
 

queue = []

def bearer_oauth(r):
   
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "396HScraper"
    return r

def rateLimit():

    while queue != [] and time.time() - queue[0] > RATE_LIMIT:
        queue.pop(0)
    
    if len(queue) > MAX_REQ:
        time.sleep(max(RATE_LIMIT - (time.time() - queue[0]), 0))
    
    queue.append(time.time())


def apiReq(id):
    rateLimit()

    tId = id[1:]

    temp = requests.request("GET", f'https://api.twitter.com/2/users/{tId}/tweets', auth=bearer_oauth)

    if temp.status_code != 200:
        return apiReq(id)
    else: 
        return temp.json()




if __name__ == '__main__':
    
    tweets = None

    args = sys.argv + ['list1.txt']

    data = {}
    dataFileName = args[1][:-4] + ".json"

    print(dataFileName )

    

    if os.path.exists(dataFileName):
        with open(dataFileName, 'r') as f:
            data = json.load(f)



    

    with open(args[1], 'r') as f:
        tweets = f.read().split('\n')[:-1]
    
    allTweets = len(tweets)

    while tweets != [] and tweets[0] in data:
        tweets = tweets[1:]
    
    downloaded = allTweets - len(tweets)


    for id in tweets:

        response = apiReq(id)

        if 'data' not in response:
            data[id] = []
        else:
            data[id] = response['data']
        
        with open(dataFileName, 'w') as f:
            json.dump(data, f)
        
        downloaded += 1

        print(f'{downloaded/allTweets} proportion of tweets downloaded!                          ', end = '\r')
        
        

    
    
    
    


