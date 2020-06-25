import praw
import csv
import pandas as pd 

reddit = praw.Reddit(client_id='',client_secret='',
                     password='',
                     user_agent='Depression',
                     username='')
subreddit = reddit.subreddit('mentalhealth')

hot_python = subreddit.hot(limit=10000)
data=[]

for submission in hot_python:
    data.append([submission.title,submission.selftext,submission.url])
    print('Title:{} \n Content:{} \n URl:{}'.format(submission.title,submission.selftext,submission.url))

data=pd.DataFrame(data,columns=['Title','Content','URL'])
    
data.to_csv('redditdata.csv')
    
