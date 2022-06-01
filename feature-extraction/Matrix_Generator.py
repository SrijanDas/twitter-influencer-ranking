import time

import pandas as pd
import os


class Matrix_Generator:
    user_list = []
    files = []

    def __init__(self, path):
        self.path = path
        self.files = os.listdir(path)

        for file_name in self.files:
            self.user_list.append(file_name[:-11])

    def get_reply_matrix(self):
        mat_reply = []
        reply_dict = {}
        count = 0
        for filename in self.files:
            count += 1
            username = filename[:-11]
            print(f"{count} -> --- {username} ----\n")

            df = pd.read_csv(self.path + str(filename))
            replies = df["reply_to_screen"].dropna().to_list()
            # print("Replies: ", replies)

            mat = []
            reply_dict[username] = len(replies)
            replies_of_i_to_j = {}

            for j in self.files:
                username2 = j[:-11]
                if j != filename:
                    c = replies.count(username2)
                    replies_of_i_to_j[username2] = c
                    mat.append(c)
                else:
                    replies_of_i_to_j[username2] = 0
                    mat.append(0)
                # print("replies_of " + str(username[:-11]) + " to " + str(j[:-11]) + " :  " + str(replies_of_i_to_j[j[:-11]]))

            print("Total reply of " + str(username) +
                  " : ", reply_dict[username])
            print()
            mat_reply.append(mat)

        # for i in mat_reply:
        #     print(i)

        df1 = pd.DataFrame(mat_reply, index=self.user_list,
                           columns=self.user_list)
        df1.to_csv("./output/reply_matrix.csv", index=True)
        print("reply_matrix created.\nOutput path --> ./output/reply_matrix.csv")

    def get_mention_matrix(self):
        mat_mention = []
        mention_dict = {}
        count = 0
        for filename in self.files:
            count += 1
            username = filename[:-11]
            print(f"{count} -> --- {username} ----\n")
            df = pd.read_csv(self.path + str(filename))

            mentions_of_i_to_j = {}
            mat = []
            tweets = df["text"]
            text = ""
            for tweet in tweets:
                text += tweet

            mentions = []
            words = text.split()

            for i in words:
                if i[0] == "@":
                    mentions.append(i[1:])

                #     print("mentions: ", mentions)

            mention_dict[username] = len(mentions)

            for j in self.files:
                username2 = j[:-11]
                if j != filename:
                    c = mentions.count(username2)
                    mentions_of_i_to_j[username2] = c
                    mat.append(c)
                else:
                    mentions_of_i_to_j[j[:-11]] = 0
                    mat.append(0)
                # print("mention_of " + str(username) + " to " + str(username2) + " :  " + str(
                #     mentions_of_i_to_j[username2]))

            print("Total mention of " + str(username) +
                  " : ", mention_dict[username])
            print()
            mat_mention.append(mat)

        df2 = pd.DataFrame(mat_mention, index=self.user_list,
                           columns=self.user_list)
        df2.to_csv("./output/mention_matrix.csv", index=True)
        print("mention_matrix created.\nOutput path --> ./output/mention_matrix.csv")

    def get_retweet_matrix(self):
        mat_rt = []
        rt_dict = {}
        count = 0
        for filename in self.files:
            count += 1
            username = filename[:-11]
            print(f"{count} -> --- {username} ----\n")
            df = pd.read_csv(self.path + str(filename))

            mat = []
            retweets_of_i_to_j = {}
            tweets = df["text"]
            all_retweets = []

            for tweet in tweets:
                if tweet[:2] == "RT":
                    text = ""
                    for i in tweet[4:]:
                        if i == ":":
                            break
                        else:
                            text += i
                    all_retweets.append(text)

            #     print("all_retweets: ", len(all_retweets))
            #     print(all_retweets)

            rt_dict[username] = len(all_retweets)

            for j in self.files:
                username2 = j[:-11]
                if j != filename:
                    c = all_retweets.count(username2)
                    retweets_of_i_to_j[username2] = c
                    mat.append(c)
                else:
                    retweets_of_i_to_j[username2] = 0
                    mat.append(0)
                # print("retweet_of " + str(username) + " to " + str(username2) + " :  " + str(
                #     retweets_of_i_to_j[username2]))

            print("Total retweet of " + str(username) +
                  " : ", rt_dict[username])
            print()
            mat_rt.append(mat)

        df3 = pd.DataFrame(mat_rt, index=self.user_list,
                           columns=self.user_list)
        df3.to_csv("./output/retweet_matrix.csv", index=True)
        print("retweet_matrix created.\nOutput path --> ./output/retweet_matrix.csv")


if __name__ == '__main__':
    """
    user count      : 500
    reply matrix    : 10 s
    mention matrix  : 17 s
    retweet matrix  : 09 s

    user count      : 8692
    reply matrix    : 281 s
    mention matrix  : 1193 s
    retweet matrix  : 407 s
    """

    start = time.time()
    mg = Matrix_Generator(path="./data1/")

    mg.get_reply_matrix()
    mg.get_mention_matrix()
    mg.get_retweet_matrix()

    end = time.time()
    print("Time taken: ", int(end-start), "seconds")
