import pandas as pd
import requests
import json
import csv
import time
import datetime


def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"    
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    try:
        content=subm['selftext']
    except KeyError:
        content="NaN"
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    
    subData.append((sub_id,title,content,url,author,score,created,numComms,permalink,flair))
    subStats[sub_id] = subData

sub='mentalhealth'                  #Name of Subreddit
before="1579910400"                 # 25 Jan 2020  Unix TimeStamp....... See readme.md to get the Unix timeStamp
after="1569888000"                  # 1 Oct 2020   Unix TimeStamp
query=""                            # Keyword--> If u want data which contains a keyword like if u want Baby Yoda in data then query="Baby Yoda"
subCount=0
subStats ={}

data = getPushshiftData(query, after, before, sub)
# Will run until all posts have been gathered 
# from the 'after' date up until before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)
    
print(len(data))

def updateSubs_file():
    upload_count = 0
    location = r""    #Path to save the csv file
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location+"\"+ filename
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Content","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
            
        print(str(upload_count) + " submissions have been uploaded")
        
updateSubs_file()









































