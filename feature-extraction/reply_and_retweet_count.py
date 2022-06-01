import pandas as pd
import os
import csv

path = ".\\data\\"
files = os.listdir(path)

# usernames = []
usernames = pd.read_csv("./userList.csv")["username"].tolist()


rp_ar = []
reply_array = []
rt_array = []
nf = []

# for file_name in files:
#     usernames.append(file_name[:-11])
# len(usernames)

print("\nCounting replies.....")
count = 0
for file_name in files:
    count += 1
    print(count, "--->", file_name)
    if file_name[:-11] not in nf:
        df = pd.read_csv(path + str(file_name))
        rp_ar.extend(df['reply_to_screen'].dropna().tolist())
        rt_array.append(sum(df['retweeted_count'].tolist()))

print("\nCounting replies.....")
count = 0
for username in usernames:
    count += 1
    print(count, "--->", username)
    reply_array.append(rp_ar.count(username))

print(len(files))
print(len(reply_array))
n = len(usernames)

with open('./output/reply_and_retweet_count.csv', 'w+', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, ['User_name', 'RP3', 'RT3'])
    writer.writeheader()
    print("\nWriting output...............................")
    for i in range(n):
        print(i, "--->", usernames[i])
        writer.writerow(
            {'User_name': usernames[i], 'RP3': reply_array[i], 'RT3': rt_array[i]})
    print("Done...........................................")
