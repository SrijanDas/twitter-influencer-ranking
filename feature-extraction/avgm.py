import time
from collections import Counter
import csv
import os
import traceback
from datetime import datetime

import pandas as pd


def division_pro(n, dn, mode='f'):  # n=numerator, dn=denominator, mode: f=float, i=int
    if dn == 0:
        return division_pro(n, 1, mode)
    elif mode == 'i':
        return n // dn
    else:
        return n / dn


def measureAll(sourceFile):
    with open(sourceFile, 'r', encoding='utf-8') as fr:
        reader = csv.DictReader(fr)
        tweetList, retweetList, replyList, Cfav, Cretweeted, Cquote = [], [], [], {}, {}, {}
        for i in reader:
            month = i['status created_at'].split()[0][:-3]
            Cfav[month] = Cfav.get(month, 0) + int(i['Fav_cont'])
            Cretweeted[month] = Cretweeted.get(month, 0) + int(i['retweeted_count'])
            if (i['reply_to_screen']):
                replyList.append(month)
            else:
                retweetList.append(month) if ('RT @' in i['text'][0:5]) else tweetList.append(month)
            if (i['quote'] == 'True'): Cquote[month] = Cquote.get(month, 0) + 1
        d = i['Account Created At(same for all rows)'].split()
        tquotes = sum(Cquote.values())
        Cfav, Cretweeted, Cquote = round(division_pro(sum(Cfav.values()), len(Cfav.keys())), 3), round(
            division_pro(sum(Cretweeted.values()), len(Cretweeted.keys())), 3), round(
            division_pro(sum(Cquote.values()), len(Cquote.keys())), 3)
        avgTweet, avgRetweet, avgReply = round(division_pro(sum(Counter(tweetList).values()), len(set(tweetList))),
                                               3), round(
            division_pro(sum(Counter(retweetList).values()), len(set(retweetList))), 3), round(
            division_pro(sum(Counter(replyList).values()), len(set(replyList))), 3)
        getMonth = lambda x: \
        {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11,
         'Dec': 12}[x]
        d1 = datetime(int(d[-1]), getMonth(d[1]), int(d[2]), *map(int, d[3].split(':')))
        d2 = datetime(2020, 1, 26, 00, 00, 00)  # Republic Day 26/1/2020
    return ((d2 - d1).total_seconds(), avgTweet, avgRetweet, Cfav, Cretweeted, Cquote, avgReply, len(tweetList),
            len(retweetList), len(replyList), tquotes)


def runavgm(source_folder, destFile, errorfile):
    # source_folder = 'Dummy/'  #Give Source Folder Name
    # destFile = 'measures.csv'   #DESTINATION FILE NAME full path
    total_users = len(os.listdir(source_folder))
    users_done = []
    open_mode = 'w+'
    if os.path.exists(destFile):
        users_done = pd.read_csv(destFile)['user_name'].tolist()
        open_mode = 'a+'
    remaining = total_users - len(users_done)
    print("\nTotal users:", total_users)
    print("Remaining:", remaining)
    time.sleep(2)

    if not remaining == 0:
        with open(destFile, open_mode, encoding='utf-8', newline='') as fw:
            c = len(users_done)
            ec = 0
            fields = ['user_name', 'Twitter Account Duration(till 26/1/2020)', 'Avg. Tweet Rate(per Month)',
                      'Avg. Retweet Rate(per Month)', 'Avg. Reply Rate(per Month)', 'Total Normal Tweets', 'Total Retweets',
                      'Total Replies', 'Total Quotes', 'Avg. Fav Count(per Month)', 'Avg. Retweeted Count(per Month)',
                      'Avg. Quote Count(per Month)']
            writer = csv.DictWriter(fw, fieldnames=fields)
            if open_mode == 'w+':
                writer.writeheader()
            for i in os.listdir(source_folder):
                uname = i.split('.')[0].replace('_tweets', '')
                if uname not in users_done:
                    try:
                        data = measureAll(source_folder + i)
                        writer.writerow({'user_name': uname, 'Twitter Account Duration(till 26/1/2020)': str(data[0]),
                                         'Avg. Tweet Rate(per Month)': data[1], 'Avg. Retweet Rate(per Month)': data[2],
                                         'Avg. Reply Rate(per Month)': data[6], 'Total Normal Tweets': data[7],
                                         'Total Retweets': data[8], 'Total Replies': data[9], 'Total Quotes': data[10],
                                         'Avg. Fav Count(per Month)': data[3], 'Avg. Retweeted Count(per Month)': data[4],
                                         'Avg. Quote Count(per Month)': data[5]})
                        c += 1
                        print('||||||||||---------DONE FOR--- {} ---------|||||||||| ----- Count: {}'.format(uname, c))
                    except Exception as e:
                        ec += 1
                        traceback.print_exc()
                        with open(errorfile, 'a+', encoding='utf-8', newline='') as f:
                            f.write("Count: {},  User Id: {}, Error: {}\n".format(ec, str(uname), str(e.args[0])))
                            print("error for : ", uname)
                        continue


if __name__ == '__main__':

    errorfile = './output/ErrorLog(avgm).csv'
    runavgm('./data/', './output/account_based_measures.csv',
            errorfile)
    print('\n\n||||||| Account based Average measurements collected |||||||\n\n')
