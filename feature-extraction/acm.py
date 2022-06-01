import os.path
from datetime import date, datetime
import tweepy as tw
import csv
from key import *
import pandas as pd
import time

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tw.API(auth)

# file paths
ERROR_FILEPATH = './output/ErrorLog(acm).csv'
AAM_PATH = './output/account_average_measures.csv'
ABF_PATH = './output/account_based_features.csv'


# Authentication part done || Notes: 'status' gives my first tweet

def getFeatures(username, sourcefile):
    alldata = api.get_user(screen_name=username)._json
    id_str, followers, following, favourites, statuses = alldata['id_str'], alldata['followers_count'], alldata[
        'friends_count'], alldata['favourites_count'], alldata['statuses_count']
    with open(sourcefile, 'r', encoding='utf-8') as searchf:
        reader = csv.DictReader(searchf)
        for row in reader:
            if row['user_name'] == username:
                return (id_str, username, followers, following, round(followers / following, 3), statuses,
                        row['Total Retweets'], favourites)


def runacm(sourcefile, destfile, errorfile):
    # sourcefile = 'measures.csv'
    # destfile = 'account based features.csv'

    total_users = len(pd.read_csv(sourcefile))
    users_done = []
    open_mode = 'w+'
    # loading pre downloaded users
    if os.path.exists(destfile):
        users_done = pd.read_csv(destfile)['User Name'].tolist()
        open_mode = 'a+'
    remaining = total_users - len(users_done)
    print("\nTotal users:", total_users)
    print("Remaining:", remaining)
    time.sleep(2)

    with open(sourcefile, 'r', encoding='utf-8') as rf:
        with open(destfile, open_mode, encoding='utf-8', newline='') as wf:
            reader = csv.DictReader(rf)
            fields = ['User ID', 'User Name', 'Followers', 'Following', 'Follower/Following Ratio', 'Total Status',
                      'Retweet Count', 'Total Favourites']
            writer = csv.DictWriter(wf, fieldnames=fields)
            if open_mode == 'w+':
                writer.writeheader()
            c = total_users-remaining
            for row in reader:
                try:
                    if row['user_name'] not in users_done:
                        data = getFeatures(row['user_name'], sourcefile)
                        writer.writerow(
                            {'User ID': data[0], 'User Name': data[1], 'Followers': data[2], 'Following': data[3],
                             'Follower/Following Ratio': data[4], 'Total Status': data[5], 'Retweet Count': data[6],
                             'Total Favourites': data[7]})
                        c += 1
                        print('|||  DONE FOR    -- {} --    |||    --COUNT: {}'.format(row['user_name'], c))
                except Exception as e:
                    err_users_list = pd.read_csv(errorfile)["Username"].tolist()
                    err_file_open_mode = 'w+'

                    if os.path.exists(errorfile):
                        err_file_open_mode = 'a+'

                    error_code = str(e).split()[0]
                    if error_code == "429" or error_code == "88":
                        print("Rate limit exeeded please wait...")
                        time.sleep(60 * 5)
                    else:
                        if str(row['user_name']) not in err_users_list:
                            with open(errorfile, err_file_open_mode, encoding='utf-8', newline='') as f:
                                writer1 = csv.DictWriter(f, ['Username', 'Error'])

                                if err_file_open_mode == "w+":
                                    writer1.writeheader()

                                writer1.writerow({'Username': str(row['user_name']), 'Error': e})
                                print("error for : ", row['user_name'])
                                print(e)

                    

if __name__ == '__main__':
    runacm(AAM_PATH, ABF_PATH, ERROR_FILEPATH)
    print('\n\n|||||| Account based information collected ||||||\n\n')
