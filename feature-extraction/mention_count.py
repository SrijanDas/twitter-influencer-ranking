import pandas as pd
import os
import csv

path = ".\\data\\"
files = os.listdir(path)

mention_dict = {}
usernames = []
for file_name in files:
    usernames.append(file_name[:-11])
for username in usernames:
    mention_dict[username] = 0
# mention_dict
print('This operation takes some time .... Please wait')
for username in usernames:
    for file_name in files:
        if file_name[:-11] != username:
            # print("\n\n",username, "..." ,file_name)
            print("\nLooking for:", username, "...in...", file_name)

            df = pd.read_csv(path + file_name)
            tweets = df["text"]

            text = ""
            for tweet in tweets:
                text += tweet

            mentions = []
            words = text.split()

            for i in words:
                if i[0] == "@":
                    mentions.append(i[1:])

                #             print("mentions", mentions)

            if username in mentions:
                # print("found", username, "in", file_name)
                mention_dict[username] += 1
# print(mention_dict)

with open('./output/mentions_count.csv', 'w+', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, ['User_name', 'Mention_count'])
    writer.writeheader()
    for i in range(len(usernames)):
        writer.writerow({'User_name': usernames[i], 'Mention_count': mention_dict[usernames[i]]})
print('Mention_count.csv created ........')