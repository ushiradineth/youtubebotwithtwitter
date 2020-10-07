import google
import requests
import json
import tweepy
import time
from datetime import datetime
import pytz
import os
import schedule

seoultime = pytz.timezone('Asia/Seoul')
datetime_st = datetime.now(seoultime)
time1 = datetime_st.strftime("%H:%M KST %d/%m")
# time = datetime_st.strftime("%H:%M:%S %d-%m-%Y KST")

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

##videolink with google api not just a youtube link
videolink = ''

viewsbefore = 0
viewsdif = 0
views = 0
h = 0
m = 0

def tweet():
    try:
        global viewsbefore, h, m
        video = requests.get(videolink)
        viewslink = video.json()
        views = int(viewslink['items'][0]['statistics']['viewCount'])

        viewsdif = views - viewsbefore
        if (viewsbefore == 0):
            viewsdif = 0
        viewsbefore = views
        
        if (viewsdif > 0):
            sign = "+"
        if (viewsdif < 0):
            sign = "-"
        if(viewsdif == 0):
            sign = ""
            
        api.update_status(status=("View count : " + "{:,}".format(views)))
        
        ##if wanted to be replied to a thread (update screen_name)
        ##status_list = api.user_timeline(screen_name="")
        ##status = status_list[0]
        ##json_str = status._json
        ##tweetid = json_str["id"]
        ##api.update_status(status=("View count : " + "{:,}".format(views)) , in_reply_to_status_id=tweetid, auto_populate_reply_metadata=True)
        
        m = m + 10
        if (m == 60):
            m = 0
            h = h + 1
             
    except BaseException as e:
        print("Error on_data %s" % str(e))
        return

tweet()
schedule.every(10).minutes.do(tweet)

while True:
    schedule.run_pending()
    time.sleep(1)
