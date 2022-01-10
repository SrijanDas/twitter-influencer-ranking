import pandas as pd
import os
import csv

path = ".\\data\\Tweets\\"
files = os.listdir(path)

usernames = []

rp_ar = []
reply_array = []
nf = []

for file_name in files:
    usernames.append(file_name[:-11])
# len(usernames)


for file_name in files:
    if file_name[:-11] not in nf:
        df = pd.read_csv(path + str(file_name))
        rp_ar.extend(df['reply_to_screen'].dropna().tolist())

for username in usernames:
    reply_array.append(rp_ar.count(username))

print(len(files))
print(len(reply_array))
n= len(usernames)

with open('.\\data\\reply_count.csv', 'w+', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, ['User_name', 'RP3'])
    writer.writeheader()
    for i in range(n):
        writer.writerow({'User_name': usernames[i], 'RP3': reply_array[i]})