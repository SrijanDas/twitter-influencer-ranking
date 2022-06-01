import time

import pandas as pd
import os
import csv

INPUT_PATH = ".\\data1\\"
OUTPUT_PATH = "./output/mentions_count.csv"
SLEEP_AFTER = 1
TIMEOUT = 5
files = os.listdir(INPUT_PATH)
mention_count_exists = os.path.exists(OUTPUT_PATH)

users_done = []
mention_dict = {}
usernames = pd.read_csv("./userList.csv")["username"].tolist()

# checking if mentions output exists
if mention_count_exists:
    mentions_df = pd.read_csv(OUTPUT_PATH)
    users_done = mentions_df['User_name'].tolist()

# getting usernames
# for file_name in files:
#     usernames.append(file_name[:-11])

# initializing mention dict
# for username in usernames:
#     mention_dict[username] = 0


def write_output(username, mention_count):
    open_mode = 'w+'
    if os.path.exists(OUTPUT_PATH):
        open_mode = 'a+'
    with open(OUTPUT_PATH, open_mode, encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['User_name', 'Mention_count'])
        if open_mode == 'w+':
            writer.writeheader()
        writer.writerow(
            {'User_name': username, 'Mention_count': mention_count})
    print("Data added to 'mentions_count.csv' successfully.")


print("\nTotal files: ", len(files))
print("Done: ", len(users_done))
time.sleep(1)

for username in usernames:
    mention_count = 0
    if username in users_done:
        print("\nSkipped --> ", username)
    else:
        print(f"\nLooking for '{username}' in {len(files)} files")
        print('This operation takes some time .... Please wait')
        count1 = 0
        for file_name in files:
            if file_name[:-11] != username:
                # print("\nLooking for:", username, "...in...", file_name)

                df = pd.read_csv(INPUT_PATH + file_name)
                tweets = df["text"]

                text = ""
                for tweet in tweets:
                    text += tweet

                mentions = []
                words = text.split()

                for i in words:
                    if i[0] == "@":
                        if username == i[1:]:
                            mention_count += 1
                            break
                        # mentions.append(i[1:])

            count1 += 1
            if count1 % 100 == 0:
                print(count1, "files checked")
            # if username in mentions:
            #     # print("found", username, "in", file_name)
            #     mention_count += 1

        print("Total mentions: ", mention_count)
        write_output(username, mention_count)
