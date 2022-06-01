from os import startfile, remove, path, listdir
import tweepy as tw
import json
from csv import DictReader, DictWriter
from copy import deepcopy
from time import sleep
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


# Social Network Module
class Social_Network:
    # dicts
    __network = {}  # Internal Dictionary holding all info of the users
    __buckets = {}  # Internal Dictionary of K-Shell Bucket(ID)
    # Internal Dictionary of K-Shell Bucket(ID) for Weighted K-shell
    __sp_buckets = {}
    __d = {}  # Internal Dictionary of degrees of all users in the network
    # __sp_deg = {}               # Internal Dictionary of special weighted degrees of all users in the network
    # __sp_deg2 = {}              # Internal Dictionary of special weighted and converted degrees of all users in the network
    __user_friends = {}  # Internal Dictionary having all friends of the users
    __degree = {}  # Internal Dictionary of in-degree and out-degree of all users in the network
    __spaths = {}  # Internal Dictionary of shortest paths of all users in the network
    # lists
    __namebuck = []  # Internal List of K-Shell Bucket(Name)
    __users = []  # Internal List of all the users we are considering
    # flags
    __kflag = 0  # Internal Flag to check if K-Shell Decomposition is done or not
    # Internal Flag to check if K-Shell Decomposition(weighted) is done or not
    __sp_kflag = 0
    __amat = 0  # Internal Flag to check if Adjacency Matrix is created or not
    __uflag = 0  # Internal flag to check if friends list is SHAPED or not
    __spdegflag = 0  # Internal flag to check if special degree is obtained or not
    __pr = 0  # Internal flag to check if Page Rank algo is applied or not
    __ur1 = 0  # Internal flag to check if User Rank algo is applied or not
    # Internal flag to check if User Rank algo(ref incoming link) is applied or not
    __ur2 = 0
    # Internal flag to check if User Rank algo(ref outgoing link) is applied or not
    __ur3 = 0
    # Internal flag to check if Tunk Rank algo(ref incoming link) is applied or not
    __tr1 = 0
    # Internal flag to check if Tunk Rank algo(ref outgoing link) is applied or not
    __tr2 = 0
    __inoutdeg = 0  # Internal flag to check if in-degree, out-degree is obtained or not
    __spathsflag = 0  # Internal flag of shortest paths of all users in the network
    __bcrflag = 0  # Internal flag of bcr rank of all users in the network
    __ccrflag = 0  # Internal flag of bcr rank of all users in the network

    def __init__(self, mode=1, save=False, libf='', infof='', agef='', savepath1='',
                 savepath2=''):  # lib is the path of the friends list csv
        self.__date = ""
        try:
            if (mode == 0):  # Mode: 0 >> is for very fast scanning from a previous All_User JSON saved File as libf
                print("\n|| Selected Mode:0 for data collection\n")
                y, m, d = "2020", "1", "26"
                print(
                    "|| Alert || : For collecting age information, you can choose between two options:")
                print(
                    "|| Press 1 if you want to mention your preferred date for Account Age calculation if you have taken custom date for AVGM calculation for this Network")
                print(
                    "|| Press 2 if you have kept the default date for AVGM calculation for this network (Default that is 26/2/2022)")
                # 26/1/2020
                print("|| Enter your choice: ", end="")
                n = int(input())
                if (n == 1):
                    print(
                        "\n|| Enter your preferred date in 3 stages : year(YYYY), month(M or MM), day(D or DD)\nExample : 1983 6 15 -> 15th June, 1983")
                    print("|| Enter year(YYYY): ", end="")
                    y = str(input())
                    print("|| Enter month(M or MM): ", end="")
                    m = str(input())
                    print("|| Enter day(D or DD): ", end="")
                    d = str(input())
                    print()
                else:
                    print("|| Default date(26/1/2020) is chosen for AVGM\n")
                self.__date = "{}/{}/{}".format(d, m, y)
                c = 0
                with open(libf) as rf:
                    self.__network = json.load(rf)
                for i, j in self.__network.items():
                    self.__users.append(str(i))
                    self.__user_friends[str(i)] = j['friends']
                    c += 1
                    if (c % 50 == 0):
                        print("--Data obtained for :", c, " Users--")
                self.__uflag = 1
                print("\n|| Success || : Obtained total data from ",
                      c, " Users from Input Files\n")

            # Mode: 1 >> is for scanning steadily from all other(acm,avgm,friendsJSON) Input files given
            else:
                rejectionList = []
                print("\n|| Selected Mode:1 for data collection\n")
                with open(libf) as rf:
                    data = json.load(rf)
                    c = 0
                    for row in data.keys():
                        flag1, flag2 = False, False
                        id = self.__ltrim(str(row))
                        if (data[row] == ""):
                            rejectionList.append(id)
                            continue
                        if (id in self.__users):
                            rejectionList.append(id)
                            continue
                        # print(id, str(row))
                        # if(len(data[row].split('-'))==0): continue
                        # if(str(row).find("E")!=-1 or str(row).find("+")!=-1): continue
                        self.__network[id] = {}
                        self.__network[id]['friends'] = data[row].split('-')
                        with open(infof, 'r+', encoding='utf-8') as irf:
                            infor = DictReader(irf)
                            for infos in infor:
                                if (self.__ltrim(str(infos['User ID'])) == id):
                                    flag1 = True
                                    self.__network[id]['user Name'] = infos['User Name']
                                    self.__network[id]['followers'] = int(
                                        infos['Followers'])
                                    self.__network[id]['following'] = int(
                                        infos['Following'])
                                    self.__network[id]['ff_ratio'] = float(
                                        infos['Follower/Following Ratio'])
                                    self.__network[id]['tweet_count'] = int(
                                        infos['Total Status'])
                                    break
                        if (flag1):
                            with open(agef, 'r+', encoding='utf-8') as arf:
                                flag2 = False
                                ager = DictReader(arf)
                                for ages in ager:
                                    if (ages['user_name'] == self.__network[id]['user Name']):
                                        flag2 = True
                                        self.__network[id]['account age'] = float(
                                            ages[ager.fieldnames[1]])
                                        if (len(self.__date) == 0):
                                            self.__date = ager.fieldnames[1].split('till')[
                                                1].strip()[:-1]
                                        self.__users.append(id)
                                        break
                        if (flag1 == False or flag2 == False):
                            if (id in self.__network.keys()):
                                rejectionList.append(id)
                                self.__network.pop(id)
                            if (id in self.__users):
                                rejectionList.append(id)
                                self.__users.remove(id)
                        else:
                            c += 1
                            if (c % 100 == 0):
                                print("--Data obtained for :", c, " Users--")
                print("\n|| Alert || : The whole network is getting a shape....\n")
                self.__shaping()
                print("\n|| Success || : Obtained total data from ",
                      c, " Users from Input Files\n")
                print("|| INFO || : Date for data obtained :", self.__date)

                if (
                        save):  # if save parameter is True, it will save the whole Network in a JSON file in (savepath) path, for fast access next time
                    assert (len(savepath1) and len(savepath2)
                            ) > 0, "SavePaths not given"
                    print(
                        "\n|| Alert || : Wait a while...Userslist.csv and Rejection_List.csv files are being created....\n")
                    self.saveJson_UsersInfo(savepath1)
                    print("|| Saved || : Obtained network data is saved as output in--> ",
                          savepath1, "-path   ||\n")
                    self.saveCSV_RejectionList(rejectionList, savepath2)
        except Exception as e:
            print("\n|| Failure || : Using mode:", mode, "Error: ", e)
            self.__clear()

    def __repr__(self):
        return "[Social Network Object]"

    def getFunctionsList(self):
        print([x for x in dir(Social_Network)[26:] if
               (("__" != str(x)[-2:]) and ("_" != str(x)[0]) and callable(getattr(Social_Network, x)))])

    # Utility Functions::

    def getCsvUsers(self, filepath=" "):
        with open(filepath, 'w+', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, fieldnames=["user_name", "ID"])
            writer.writeheader()
            for u in self.__network.keys():
                writer.writerow(
                    {"user_name": self.__network[u]['user Name'], "ID": u})
        print("|| Alert || : Userslist csv file created for {} USERS in the path--> {}\n".format(len(self.__network),
                                                                                                 filepath))

    def saveCSV_RejectionList(self, rejectionList=[], filepath=" "):
        with open(filepath, 'w+', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, fieldnames=["ID"])
            writer.writeheader()
            for u in rejectionList:
                writer.writerow({"ID": u})
        print(
            "|| Alert || : Rejection-list csv file created for {} USERS in the path--> {}\n".format(len(rejectionList),
                                                                                                    filepath))

    def __ltrim(self, s: str) -> str:
        i, j = 0, len(s) - 1
        while ((not s[i].isdigit()) and (i < j)):
            i += 1
        return s[i:]

    def saveJson_UsersInfo(self,
                           filepath) -> None:  # VVIMP prints the friends dictionary(friends["1234"] = [12,34,56,78....]) of Social Graph
        if (len(self.__network) == 0):
            print("Friends list is Empty!")
        else:
            with open(filepath, 'w+') as f:
                f.write(json.dumps(self.__network, indent=4))
            # print("You can check the output JSON of the Network in--> {}  path".format(filepath))

    def __shaping(self) -> None:  # Internal Use
        # Shapes the friends list so that we can work with only the users...
        if (self.__uflag == 0):
            for i in self.__users:  # ...we are taking in our databse and it removes other users...
                temp = []  # ... from the friends list while creating the Network
                for x in self.__network[i]['friends']:
                    if (x in self.__users):
                        temp.append(x)
                self.__network[i]['friends'] = temp
            self.__uflag = 1
            for i in self.__users:
                # a very important operation
                self.__user_friends[i] = self.__network[i]['friends']

    # Shape the whole network manually by executing this function.
    def shape_network(self) -> None:
        if (self.__uflag == 0):
            self.__shaping()  # recommended when you just want to see the shaped network
        print("\n---->WARNING ::  The network is Shaped now <----")

    # Prints the list of all users considered in the Network
    def get_usersCount(self) -> None:
        print("|| Alert || : Users Count: {}\n".format(len(self.__users)))

    def getName(self, id: str) -> str:  # Returns userName of a User from userID(str)
        return self.__network[id]['user Name']

    # K_Shell Decomposition starts::

    def __clear(self):
        self.__network, self.__buckets, self.__sp_buckets, self.__d, self.__sp_deg, self.__sp_deg2, self.__user_friends = {}, {}, {}, {}, {}, {}, {}
        self.__namebuck, self.__users = [], []
        self.__kflag, self.__sp_kflag, self.__amat, self.__uflag, self.__spdegflag = 0, 0, 0, 0, 0

    def __get_degree(self, l,
                     mode="out") -> dict:  # Internal Use for getting in or out degree : mode = in for Indegree , out for Outdegree
        # stores the indgerees, outdegrees for all users
        self.__degree = {x: {"in": [], "out": []} for x in l}
        for user in l:
            # outdegree done = size of friends list
            self.__degree[user]["out"] = self.__user_friends[user]
            for i in self.__user_friends[user]:
                if (i == user or i not in l.keys()):
                    continue
                else:
                    self.__degree[i]["in"].append(
                        user)  # indegree done = user in other users friends list               # for getting all Indegree Outdegree of the network as [self.__degree{in, out}]
        d = {}  # Gets degree of the friends network and stores it in a Dictionary-->
        # -->> (dict[deg = i] = list[users who have i-th degree in the network])
        for i in self.__degree.keys():
            x = len(self.__degree[i][mode])
            if (x not in d.keys()):
                d[x] = []
            d[x].append(i)
        return d

    # If you want to see the Degree Dictionary of the Network...
    def __print_degree(self) -> None:
        print()  # ...just use this function(it will be available...
        if (self.__kflag == 0):  # ...only after the K-Shell Decomposition)
            print("|| WARNING || :: Getting degree but: ", end=' ** ')
            print("K-Shell Decomposition is not done yet!!")
        if (self.__uflag == 0):
            self.__shaping()
        self.__d = self.__get_degree(self.__user_friends, mode="out")
        for i in range(max(self.__d.keys()) + 1):
            if (i in self.__d.keys()):
                print("deg({}) ---> {}".format(i, self.__d[i]))

    def __printCSV_UKshell_Degree(self, mode="out",
                                  filepath="/") -> None:  # If you want to see the Degree Dictionary of the Network...
        print()  # ...just use this function(it will be available...
        # if(self.__kflag == 0):                                     # ...only after the K-Shell Decomposition)
        #     print("|| WARNING || :: Getting degree but: ", end = ' ** ')
        #     print("K-Shell Decomposition is not done yet!!")
        # if(self.__uflag == 0): self.__shaping()
        # dg = self.__get_degree(self.__user_friends, mode="out")
        with open(filepath, "w+", encoding="utf-8", newline="") as degreeCSV:
            writer = DictWriter(degreeCSV, fieldnames=[
                                "Degree", 'Users-Count', "Users"])
            writer.writeheader()
            for i in range(max(self.__d.keys()) + 1):
                if (i in self.__d.keys()):
                    writer.writerow(
                        {'Degree': i, 'Users-Count': len(self.__d[i]), 'Users': ":".join(self.__d[i])})
        print(
            "\n|| Success || : [Internal] You can check the output CSV of Unweighted K-Shell Output[for {}-degree] the In-Out Degree in--> {}  path".format(
                mode, filepath))

    # This is a special internal function for updaing the network...
    def __updateKs(self, y, change):
        dnew = {}  # ...after every k-shell iteration
        for i in y.keys():
            flag = True
            for j in change:
                if (i == j):
                    flag = False
                    break
                if (j in y[i]):
                    y[i].remove(j)
            if (flag):
                dnew[i] = y[i]
        return dnew

    # This is a special internal function to check if lower degrees...
    def __destroyer(self, container, x) -> bool:
        for i in container.keys():  # exist or not in the graph, while doing K-Shell
            if (i <= x):
                return True
        return False

    def __k_shell_decompose(self, mode,
                            filepaths: dict = {}) -> None:  # It is the main function for doing K-Shell Decomposition...
        # ...after making(enlisting all needed users) the friends dict...
        self.__shaping()
        if (len(self.__d) == 0):
            # ...run this.
            self.__d = self.__get_degree(self.__user_friends, mode=mode)
        l, d = deepcopy(
            {x: self.__degree[x][mode] for x in self.__degree.keys()}), deepcopy(self.__d)
        i = 0

        # some internal files
        self.__printJSON_IODegrees(filepaths['IODegree'])
        self.__printCSV_UKshell_Degree(mode, filepath=filepaths['UserDegrees'])

        while (len(d)):  #
            self.__buckets[i] = {}
            temp = []
            prune = 1  # no. of times pruned
            while (self.__destroyer(d, i)):  # <=i degree is in graph or not
                self.__buckets[i][prune] = []
                for j in range(i, -1, -1):  # i, i-1, i-2,...to 0
                    temp = d.get(j, [])
                    # if(len(temp)!=0):// condition to check if obtained bucket is empty or not
                    self.__buckets[i][prune].append(temp)

                    l = self.__updateKs(l, temp)
                    d = self.__get_degree(l, mode)
                prune += 1
            i += 1
        # self.__kflag=1
        for i in self.__buckets.keys():
            print(i, self.__buckets[i])
        print(
            "\n|| Success || : Unweighted K-Shell[Mode : {}] Decomposition Done!!!\n".format(mode.upper()))

    def printCSV_ukshellRank(self, mode="out", inputfile: str = " ", outputfile: str = " ",
                             infofiles: dict = {}) -> None:  # Prints the K-Shell Score after the K-Shell Decomposition
        self.__k_shell_decompose(mode, infofiles)
        resultDict = self.__buckets
        # print(resultDict)
        with open(outputfile, 'w+', encoding='utf-8', newline='') as f:
            fields = "User ID,user_name,Twitter Account Duration(till {}),Avg. Tweet Rate(per Month),Avg. Retweet Rate(per Month),Avg. Reply Rate(per Month),Avg. Fav Count(per Month),Avg. Retweeted Count(per Month),Avg. Quote Count(per Month),k-shell value".format(
                self.__date).split(',')
            writer = DictWriter(f, fieldnames=fields)
            writer.writeheader()
            score, c = 1, 0
            ms = set()  # Important
            for i in sorted(resultDict.keys(), reverse=False):  # Level
                dx = 0
                for j in sorted(resultDict[i].keys(), reverse=False):  # Prune
                    value = score + dx
                    # print(dx, score, value, resultDict[i].items())
                    for k in range(len(resultDict[i][j])):  # Degree
                        for p in resultDict[i][j][k]:  # List of Users
                            name = self.getName(str(p))
                            with open(inputfile, 'r+', encoding='utf-8') as rf:
                                reader = DictReader(rf)
                                for row in reader:
                                    if (name not in ms and row['user_name'] == name):
                                        ms.add(name)
                                        writer.writerow({'User ID': str(p), 'user_name': name,
                                                         'Twitter Account Duration(till {})'.format(self.__date): row[
                                                             'Twitter Account Duration(till {})'.format(self.__date)],
                                                         'Avg. Tweet Rate(per Month)': row[
                                                             'Avg. Tweet Rate(per Month)'],
                                                         'Avg. Retweet Rate(per Month)': row[
                                                             'Avg. Retweet Rate(per Month)'],
                                                         'Avg. Reply Rate(per Month)': row[
                                                             'Avg. Reply Rate(per Month)'],
                                                         'Avg. Fav Count(per Month)': row['Avg. Fav Count(per Month)'],
                                                         'Avg. Retweeted Count(per Month)': row[
                                                             'Avg. Retweeted Count(per Month)'],
                                                         'Avg. Quote Count(per Month)': row[
                                                             'Avg. Quote Count(per Month)'],
                                                         'k-shell value': str(value)})
                                        c += 1
                                        if (c % 100 == 0):
                                            print("|| Alert || : Unweighted K-Shell Score written for :",
                                                  c, " Users--")
                    dx += 1
                score += 1
                # Clearing Process::
            self.__buckets.clear()
            self.__d.clear()

            print(
                "|| Success || : Unweighted K-Shell Output[for {}-degree] created for {} USERS in the path--> {}\n".format(
                    mode.upper(), c, outputfile))

    # Weighted K-Shell Starts::

    def __check(self, user, friends) -> bool:
        s, n = 0, len(friends)
        for f in friends:
            s += self.__network[f]['account age']
        if (self.__network[user]['account age'] <= (s / n)):
            return True
        else:
            return False

    def __get_special_degree(self, container=[], mode="out", feature='ff_ratio',
                             precision=3) -> None:  # for every user we have to calculate the special degrees....
        if (self.__spdegflag):
            print(
                "Special degree is available")  # ... then we will reverse the key and values to get our special degree
        else:
            deg = {}
            self.__getIODegrees()
            uf = {x: self.__degree[x][mode] for x in self.__degree.keys()}
            for user in container:
                if (len(uf[user]) != 0):
                    friends = uf[user]
                    if (self.__check(user, friends)):
                        grad1, grad2 = 0.4, 0.6  # parents age <= avg child age
                    # if(self.__check(user, friends)): grad1, grad2 = 0.5, 0.5
                    else:
                        grad1, grad2 = 0.7, 0.3  # parents age > avg child age
                    # else: grad1,grad2=0.5,0.5
                    w = 0
                    for f in friends:
                        w += (self.__network[f][feature])
                    w = (w + self.__network[user]
                         [feature]) / (len(friends) + 1)
                    deg[user] = round(
                        (len(friends) ** grad1 + w ** grad2), precision)
                else:
                    deg[user] = 0.0

            self.__sp_deg = {}

            for k in set(deg.values()):
                self.__sp_deg[k] = []
                for i in deg.keys():
                    if (deg[i] == k):
                        self.__sp_deg[k].append(i)

    def __printCSV_Special_degree(self, mode, filepath, feature='ff_ratio', precision=3) -> None:
        self.__get_special_degree(mode, feature, precision)
        with open(filepath, 'w+', encoding='utf-8', newline='') as f:
            writer = DictWriter(f, fieldnames=["Special Degree", "Users"])
            writer.writeheader()
            for k in sorted(self.__sp_deg.keys()):
                writer.writerow(
                    {"Special Degree": k, "Users": ";".join(self.__sp_deg[k])})
            print(
                "|| Success || : You can check the output csv of Special Degree in--> {}  path".format(filepath))

    def __convert_range(self, l=0, y=(20, 300), deg=0, interval=20) -> int:
        h = y[0]
        while (h <= y[1]):
            temp = []
            for i in sorted(self.__sp_deg.keys()):
                if (i > l and i <= h):
                    temp += self.__sp_deg[i]
            if (len(temp)):
                deg += 1
                self.__sp_deg2[deg] = temp
                # print("deg: {}\t\tl: {}\t\th: {}".format(deg, l, h))
            l, h = (l + interval), (h + interval)
        return deg

    def __convert_special_degree(self, mode, container=[], convertFlag=True, feature='ff_ratio',
                                 precision=3):  # convertFlag means do you want to convert the degrees or not.
        self.__sp_deg2 = {}
        if (not convertFlag):
            precision = 0
        self.__get_special_degree(container, mode, feature, precision)
        if (not convertFlag):  # if you don't want to convert the degrees...and want to get the special degrees directly
            self.__sp_deg2 = deepcopy(self.__sp_deg)
        else:
            x1 = self.__convert_range(l=0, y=(20, 300), deg=1, interval=20)
            x2 = self.__convert_range(
                l=300, y=(350, 1000), deg=x1, interval=50)
            x1 = self.__convert_range(l=1000, y=(
                1100, int(max(self.__sp_deg.keys())) + 100), deg=x2, interval=100)

    def __printCSV_WKshell_Before_Special_degree(self, mode, filepath, feature='ff_ratio', precision=3) -> None:
        # self.__convert_special_degree(mode, feature, precision)
        with open(filepath, 'w+', encoding='utf-8', newline='') as f:
            writer = DictWriter(
                f, fieldnames=["Degree", 'Users-Count', "Users"])
            writer.writeheader()
            for k in sorted(self.__sp_deg.keys()):
                writer.writerow(
                    {"Degree": k, 'Users-Count': len(self.__sp_deg[k]), "Users": ":".join(self.__sp_deg[k])})
            print(
                "\n|| Success || : [Internal] You can check the output CSV of Weighted K-Shell Output[for {}-degree][Converted - True] for Degrees before Converted Special Degree in--> {}  path".format(
                    mode, filepath))

    def __printCSV_WKshell_Special_degree(self, mode, filepath, convertedFlag=True, feature='ff_ratio',
                                          precision=3) -> None:
        # self.__convert_special_degree(mode, feature, precision)
        with open(filepath, 'w+', encoding='utf-8', newline='') as f:
            writer = DictWriter(
                f, fieldnames=["Degree", 'Users-Count', "Users"])
            writer.writeheader()
            for k in sorted(self.__sp_deg2.keys()):
                writer.writerow(
                    {"Degree": k, 'Users-Count': len(self.__sp_deg2[k]), "Users": ":".join(self.__sp_deg2[k])})
            print(
                "\n|| Success || : [Internal] You can check the output CSV of Weighted K-Shell Output[for {}-degree][Converted - {}] Special Degree in--> {}  path".format(
                    mode, convertedFlag, filepath))

    def __k_shell_special_decompose(self, mode="out", convertFlag=True, feature='ff_ratio', precision=3,
                                    filepaths: dict = {}) -> None:  # It is the main function for doing K-Shell Decomposition...
        # self.__shaping()                                                        #...after making(enlisting all needed users) the friends dict...
        # ...run this.
        self.__convert_special_degree(
            mode, self.__users, convertFlag, feature, precision)
        l, d = deepcopy(self.__user_friends), deepcopy(self.__sp_deg2)
        i = 0

        # some internal files
        self.__printJSON_IODegrees(filepaths['IODegree'])  # IODegrees

        # for printing degrees before range convertion
        if (convertFlag):
            self.__printCSV_WKshell_Before_Special_degree(
                mode, filepaths['UserDegreesBefore'])

        self.__printCSV_WKshell_Special_degree(
            mode, filepaths['UserDegrees'], convertFlag)
        # print(d)
        c = 1
        while (len(d)):
            self.__sp_buckets[i] = {}
            # print(d)
            temp = []

            prune = 1  # no. of times pruned
            while (self.__destroyer(d, i)):
                # print(d)
                self.__sp_buckets[i][prune] = {}

                for j in range(i, -1, -1):  # i, i-1, i-2,...to 0
                    temp = d.get(j, [])
                    # if(len(temp)!=0):
                    self.__sp_buckets[i][prune][j] = temp
                    # if(len(temp)!=0):self.__sp_buckets[i][prune][j] = temp
                    # print(c," ",i," ",temp)
                    c += 1
                    l = self.__updateKs(l, temp)
                    self.__convert_special_degree(mode, list(
                        l.keys()), convertFlag, feature, precision)
                    # making a new sp_deg2 everytime
                    d = deepcopy(self.__sp_deg2)
                prune += 1
            i += 1
            print("total iteration", c, i)
        # self.__sp_kflag=1
        """for i in self.__sp_buckets.keys():
            print(i, self.__sp_buckets[i])"""
        print(
            "\n|| Success || : Weighted K-Shell[Mode : {}, Converted : {}] Decomposition Done!!!\n".format(mode.upper(),
                                                                                                           convertFlag))

    # Prints the Bucket after the K-Shell Decomposition
    def __printTXT_special_buckets(self, filepath):
        if (len(self.__sp_buckets) == 0):
            print("|| WARNING || :: No Buckets AVAILABLE, First Decompose the Network!!")
        else:
            with open(filepath, 'w+', encoding='utf-8') as f:
                f.write("Printing K-Shell Buckets--->\n\n")
                for i in sorted(self.__sp_buckets.keys()):
                    f.write('{}{}{}'.format("Level: ", i, '\n'))
                    for j in sorted(self.__sp_buckets[i].keys()):
                        f.write(
                            '{}{}{}{}{}'.format("After pruning ", j, "-th Time:>>  ", self.__sp_buckets[i][j], "\n"))
                    f.write("---\n")
            print(
                "You can check the output Textfile of K-Shell Decom. of Special Degree in--> {}  path".format(filepath))

    def printCSV_wkshellRank(self, mode="out", convertFlag=True, inputfile: str = " ", outputfile: str = " ",
                             infofiles: dict = {}) -> None:
        with open(outputfile, 'w+', encoding='utf-8', newline='') as wf:
            fields = "User ID,user_name,Twitter Account Duration(till {}),Avg. Tweet Rate(per Month),Avg. Retweet Rate(per Month),Avg. Reply Rate(per Month),Avg. Fav Count(per Month),Avg. Retweeted Count(per Month),Avg. Quote Count(per Month),k-shell value".format(
                self.__date).split(',')
            self.__k_shell_special_decompose(
                mode=mode, convertFlag=convertFlag, filepaths=infofiles)
            print("DONE")
            writer = DictWriter(wf, fieldnames=fields)
            writer.writeheader()
            score, c = 1, 0
            ms = set()  # Important
            for i in sorted(self.__sp_buckets.keys(), reverse=False):  # Level
                dx = 0.0
                for j in sorted(self.__sp_buckets[i].keys(), reverse=False):  # Prune
                    value = score + dx
                    # Degree
                    for k in sorted(self.__sp_buckets[i][j].keys(), reverse=False):
                        for p in self.__sp_buckets[i][j][k]:  # List of Users
                            name = self.getName(str(p))
                            with open(inputfile, 'r+', encoding='utf-8') as rf:
                                reader = DictReader(rf)
                                for row in reader:
                                    if (name not in ms and row['user_name'] == name):
                                        ms.add(name)
                                        writer.writerow({'User ID': str(p), 'user_name': name,
                                                         'Twitter Account Duration(till {})'.format(self.__date): row[
                                                             'Twitter Account Duration(till {})'.format(self.__date)],
                                                         'Avg. Tweet Rate(per Month)': row[
                                                             'Avg. Tweet Rate(per Month)'],
                                                         'Avg. Retweet Rate(per Month)': row[
                                                             'Avg. Retweet Rate(per Month)'],
                                                         'Avg. Reply Rate(per Month)': row[
                                                             'Avg. Reply Rate(per Month)'],
                                                         'Avg. Fav Count(per Month)': row['Avg. Fav Count(per Month)'],
                                                         'Avg. Retweeted Count(per Month)': row[
                                                             'Avg. Retweeted Count(per Month)'],
                                                         'Avg. Quote Count(per Month)': row[
                                                             'Avg. Quote Count(per Month)'],
                                                         'k-shell value': str(value)})
                                        c += 1
                                        if (c % 100 == 0):
                                            print("|| Alert || : Weighted K-Shell Score written for :",
                                                  c, " Users--")
                    dx += 0.2
                score += 1
                # Clearing Process
            self.__sp_deg.clear()
            self.__sp_buckets.clear()
            self.__sp_deg2.clear()

            print(
                "|| Success || : Weighted K-Shell Output[for {}-degree][degrees converted = {}] created for {} USERS in the path--> {}\n".format(
                    mode.upper(), convertFlag, c, outputfile))

    # TOPSIS

    # def printCSV_topsis(self, weight:list, mode="out", inputfile=" ", outputfile=" ", outf=" "):    # outf for topsis output, inpf, outf for kshell
    #     self.__k_shell_special_decompose(mode=mode)
    #     resultDict=self.__sp_buckets
    #     c=0
    #     with open(outputfile, 'w+', encoding='utf-8', newline='') as wf:
    #         fields = "User ID,user_name,Twitter Account Duration(till {}),Avg. Tweet Rate(per Month),Avg. Retweet Rate(per Month),Avg. Reply Rate(per Month),Avg. Fav Count(per Month),Avg. Retweeted Count(per Month),Avg. Quote Count(per Month),k-shell value".format(self.__date).split(',')
    #         writer = DictWriter(wf, fieldnames=fields+["K-Shell Score"])
    #         writer.writeheader()
    #         score = 0
    #         ms=set()    #Important
    #         for i in sorted(resultDict.keys()):  # Level
    #             dx = 0.0
    #             for j in sorted(resultDict[i].keys()): # Prune
    #                 value = score+dx
    #                 for k in sorted(resultDict[i][j].keys(), reverse=True): # Degree
    #                     for p in resultDict[i][j][k]: # List of Users
    #                         name = self.getName(str(p))
    #                         with open(inputfile, 'r+', encoding='utf-8') as rf:
    #                             reader = DictReader(rf)
    #                             for row in reader:
    #                                 if(name not in ms and row['user_name'] == name):
    #                                     ms.add(name)
    #                                     writer.writerow({'User ID':str(p), 'user_name':name,'Twitter Account Duration(till {})'.format(self.__date):row['Twitter Account Duration(till {})'.format(self.__date)],'Avg. Tweet Rate(per Month)':row['Avg. Tweet Rate(per Month)'],'Avg. Retweet Rate(per Month)':row['Avg. Retweet Rate(per Month)'],'Avg. Reply Rate(per Month)':row['Avg. Reply Rate(per Month)'],'Avg. Fav Count(per Month)':row['Avg. Fav Count(per Month)'],'Avg. Retweeted Count(per Month)':row['Avg. Retweeted Count(per Month)'],'Avg. Quote Count(per Month)':row['Avg. Quote Count(per Month)'], 'k-shell value':str(value)})
    #                                     c+=1
    #                                     #if(c%50==0): print("--Rows written for :", c, " Users--" )
    #                 dx+=0.2
    #             score+=1
    #     self.__sp_deg.clear()
    #     self.__sp_buckets.clear()
    #     self.__sp_deg2.clear()
    #     #wK-Shell Done, next TOPSIS
    #     topsisScore(c, weight, outputfile, outf)
    #     remove(outputfile)  #deleting helper file
    #     print("|| Success || : You can check the output CSV of TOPSIS[for {}-degree] in--> {}  -path\n".format(mode.upper(), outf))

    # Degrees for Ranking Algorithms

    def __getIODegrees(self) -> None:
        if (not self.__inoutdeg):
            self.__degree = {x: {"in": [], "out": []} for x in
                             self.__users}  # stores the indgerees, outdegrees for all users
            for user in self.__users:
                # outdegree done = size of friends list
                self.__degree[user]["out"] = self.__user_friends[user]
                for i in self.__user_friends[user]:
                    if (i == user):
                        continue
                    else:
                        # indegree done = user in other users friends list
                        self.__degree[i]["in"].append(user)
            # self.__inoutdeg=1

    def __printJSON_IODegrees(self, filepath="/"):
        if (path.isfile(filepath)):
            return  # if not already created
        if (len(self.__degree) == 0):
            self.__getIODegrees()
        with open(filepath, 'w+') as f:
            f.write(json.dumps(self.__degree, indent=4))  #
            print(
                "\n|| Success || : [Internal] -> You can check the output JSON of the In-Out Degree in--> {}  path".format(
                    filepath))

    # Page Rank Algo::

    # applies page rank algo on the network
    def __page_rank_algo(self, damp, epoch) -> None:
        self.__page_rank = {x: {"in": [], "out": 0, "node_rank": 0} for x in
                            self.__users}  # stores the indgerees, outdegrees, page ranks for all users
        revdamp = 1 - damp
        for user in self.__users:
            # outdegree done = size of friends list
            self.__page_rank[user]["out"] = len(self.__user_friends[user])
            for i in self.__user_friends[user]:
                if (i == user):
                    continue
                else:
                    # indegree done = user in other users friends list
                    self.__page_rank[i]["in"].append(user)
        diff = 1  # difference of ranks between two iterations
        e = epoch
        while (epoch > 0 and abs(diff - 0.0) != 0):
            diff = 0
            for user in self.__users:
                x = 0  # x=(noderank of ins/outs of each node)
                for i in self.__page_rank[user]["in"]:
                    x += (
                        self.__page_rank[i]["node_rank"] / self.__page_rank[i]["out"])
                prev = self.__page_rank[user]["node_rank"]
                self.__page_rank[user]["node_rank"] = (revdamp + (damp * x))
                diff += abs(prev - self.__page_rank[user]["node_rank"])
            epoch -= 1
        else:
            print("|| Success || : Page Rank Algorithm completed\n-----------|| Epoch done : ", e - epoch,
                  " , Difference: ", diff, "\n")

    # User Rank mode 1 algo::

    def __user_rank_1_algo(self) -> None:
        self.__user_rank_1 = {}
        f_values = {}
        for user in self.__users:
            data = self.__network[user]
            a, b, c = data['followers'], data['tweet_count'], len(
                data['friends'])
            if (c == 0):
                c = 1
            f_values[user] = ((a / b) / c)
        for user in self.__users:
            self.__user_rank_1[user] = 0
            for f in self.__user_friends[user]:
                self.__user_rank_1[user] += f_values[f]

    # User Rank 2, 3(ref Page Rank)::
    # applies user rank algo(ref incoming link) on the network
    def __user_rank_2_algo(self, epoch) -> None:
        self.__getIODegrees()  # in-out degree dict is available now
        def f_t(x): return self.__network[x]["followers"] / (
            self.__network[x]["tweet_count"])  # ratio = (followers count / tweets count)
        # stores the user rank ratios for all users
        user_rank_ratios = {x: f_t(x) for x in self.__users}
        # stores the user ranks(ref incoming links) for all users
        self.__user_rank_2 = {x: 0 for x in self.__users}
        diff = 1
        e = epoch
        while (epoch and diff != 0):
            diff = 0
            for user in self.__users:
                # x=((1+(ur_ratio of curr * ur of incoming link))/(no. of outs of incoming link * no. of followers of incoming link)
                x = 0
                for inc in self.__degree[user]["in"]:
                    x += (1 + (user_rank_ratios[user] * self.__user_rank_2[inc])) / (
                        1 + len(self.__degree[inc]["out"]) * self.__network[inc]["followers"])
                prev = self.__user_rank_2[user]
                self.__user_rank_2[user] = x
                diff += abs(prev - self.__user_rank_2[user])
            epoch -= 1
        else:
            print("|| Success || : User Rank Algorithm(Incoming) completed\n-----------|| Epoch done : ", e - epoch,
                  " , Difference: ", diff, "\n")
        # Clearing

    # applies user rank algo(ref outgoing link) on the network
    def __user_rank_3_algo(self, epoch) -> None:
        self.__getIODegrees()  # in-out degree dict is available now
        def f_t(x): return self.__network[x]["followers"] / (
            self.__network[x]["tweet_count"])  # ratio = (followers count / tweets count)
        # stores the user rank ratios for all users
        user_rank_ratios = {x: f_t(x) for x in self.__users}
        # stores the user ranks(ref outgoing links) for all users
        self.__user_rank_3 = {x: 0 for x in self.__users}
        diff = 1
        e = epoch
        while (epoch and diff != 0):
            diff = 0
            for user in self.__users:
                # x=((1+(ur_ratio of curr * ur of outgoing link))/(no. of ins of outgoing link * no. of followers of incoming link)
                x = 0
                for outs in self.__degree[user]["out"]:
                    x += (1 + (user_rank_ratios[user] * self.__user_rank_3[outs])) / (
                        len(self.__degree[outs]["in"]) * self.__network[outs]["followers"])
                prev = self.__user_rank_3[user]
                self.__user_rank_3[user] = x
                diff += abs(prev - self.__user_rank_3[user])
            epoch -= 1
        else:
            print("|| Success || : User Rank Algorithm(Outgoing) completed\n-----------|| Epoch done : ", e - epoch,
                  " , Difference: ", diff, "\n")

    # Tunk Rank 1, 2 ::
    # applies Tunk rank algo(ref incoming link) on the network
    def __tunk_rank_1_algo(self, epoch, mul) -> None:
        self.__getIODegrees()  # in-out degree dict is available now
        def f_t(x): return self.__network[x]["followers"] / (
            self.__network[x]["tweet_count"])  # ratio = (followers count / tweets count)
        # stores the tunk rank ratios for all users
        tunk_rank_ratios = {x: f_t(x) for x in self.__users}
        # stores the tunk ranks(ref incoming links) for all users
        self.__tunk_rank_1 = {x: 0 for x in self.__users}
        diff = 1
        e = epoch
        while (epoch and diff != 0):
            diff = 0
            for user in self.__users:
                # x=((1+(tr_ratio of curr * tr of incoming link))/(no. of outs of incoming link * no. of friends of incoming link)
                x = 0
                for inc in self.__degree[user]["in"]:
                    l = len(self.__network[inc]["friends"])  # no. of friends
                    if (l == 0):
                        l = 1
                    x += (1 + (tunk_rank_ratios[user] * self.__tunk_rank_1[inc])) / (
                        len(self.__degree[inc]["out"]) * l * mul)
                prev = self.__tunk_rank_1[user]
                self.__tunk_rank_1[user] = x
                # print(prev, self.__tunk_rank_1[user])
                diff += abs(prev - self.__tunk_rank_1[user])
            epoch -= 1
        else:
            print("|| Success || : Tunk Rank Algorithm(Incoming) completed\n-----------|| Epoch done : ", e - epoch,
                  " , Difference: ", diff, "\n")

    # applies Tunk rank algo(ref outgoing link) on the network
    def __tunk_rank_2_algo(self, epoch, mul) -> None:
        self.__getIODegrees()  # in-out degree dict is available now

        def f_t(x): return self.__network[x]["followers"] / (
            self.__network[x]["tweet_count"])  # ratio = (followers count / tweets count)
        # stores the tunk rank ratios for all users
        tunk_rank_ratios = {x: f_t(x) for x in self.__users}
        # stores the tunk ranks(ref outgoing links) for all users
        self.__tunk_rank_2 = {x: 0 for x in self.__users}
        diff = 1
        e = epoch
        while (epoch and diff != 0):
            diff = 0
            for user in self.__users:
                # x=((1+(tr_ratio of curr * tr of outgoing link))/(no. of ins of outgoing link * no. of friends of incoming link)
                x = 0
                for outs in self.__degree[user]["out"]:
                    l = len(self.__network[outs]["friends"])  # no. of friends
                    if (l == 0):
                        l = 1
                    x += (1 + (tunk_rank_ratios[user] * self.__tunk_rank_2[outs])) / (
                        len(self.__degree[outs]["in"]) * l * mul)
                prev = self.__tunk_rank_2[user]
                self.__tunk_rank_2[user] = x
                diff += abs(prev - self.__tunk_rank_2[user])
            epoch -= 1
        else:
            print("|| Success || : Tunk Rank Algorithm(Outgoing) completed\n-----------|| Epoch done : ", e - epoch,
                  " , Difference: ", diff, "\n")

    # Ranking using Graph Centrality ::

    # Shortest paths in the network ::
    def __shortestPaths(self, xmode=1, xmode1=1, filepath="", users: list = [],
                        net: dict = {}) -> None:  # Internal function for Generating All pair shortest paths
        print("\n|| Alert || : ......Starting Shortest paths creation for the whole netwrok. It may take a while....\n")
        if (xmode == 1):
            for i in net.keys():
                self.__spaths[i] = {x: [] for x in users}
                for j in net[i]:
                    self.__spaths[i][j].extend([i, j])
            # for i in self.__spaths: print(i, self.__spaths[i])
            spc = {}
            # classic apsp
            c = 0
            for k in users:
                for i in users:
                    for j in users:
                        if (i == k or j == k):
                            continue
                        elif (i == j):
                            continue
                        else:
                            curr, th1, th2 = len(self.__spaths[i][j]), len(self.__spaths[i][k]), len(
                                self.__spaths[k][j])
                            if (th1 * th2 == 0):
                                continue
                            elif (curr == 0):
                                self.__spaths[i][j] = self.__spaths[i][k][:-
                                                                          1] + self.__spaths[k][j]
                            else:
                                if (th1 + th2 < curr):
                                    self.__spaths[i][j] = self.__spaths[i][k][:-
                                                                              1] + self.__spaths[k][j]
                                elif (th1 + th2 - 1 == curr):
                                    spc[i] = {j: []}
                                    spc[i][j].append(
                                        self.__spaths[i][k][:-1] + self.__spaths[k][j])
                                    spc[i][j].append(self.__spaths[i][j])
                                else:
                                    continue
                c += 1
                if (c % 100 == 0):
                    print("|| Alert || : Shortest path created for :", c, " Users--")
                # self.__spathsflag=1

            '''print("Shortest paths: ")
            for i in mat: print(i, mat[i])
            print("Special: ")  #where there are multiple same length paths
            for i in spc: print(i, spc[i])'''

            for i in spc:
                for j in spc[i]:
                    self.__spaths[i][j] = spc[i][j]

            if (xmode1 == 1):
                with open(filepath, 'w+') as f:
                    f.write(json.dumps(self.__spaths, indent=4))
                print("\n|| Alert || : You can check the saved Shortest Paths of the Network in--> {}  path".format(
                    filepath))

        elif (xmode == 2):
            # From saved files
            with open(filepath) as rf:
                self.__spaths = json.load(rf)
            # self.__spathsflag==1

        print("\n|| Success || : All Shortest paths have been created!!\n")

    # Betweenness Centrality ::
    # using apsp for getting Betweenness-Centrality ranks
    def __betCentRank(self, xmode=1, filepath=" ", xmode1=1):
        self.__shortestPaths(xmode, xmode1, filepath,
                             users=self.__users, net=self.__user_friends)
        self.__bcrdict = {x: 0 for x in self.__users}
        # print(self.__bcrdict)
        print("|| Alert || : Staring the process of Betweenness Centrality Ranking...\n")
        c = 0
        for curr in self.__bcrdict:
            '''take a curr, then except curr check every other node spaths(shortest paths)...
            then get the ratio of-> no. of spaths where curr is in that path/total no. of shortest paths'''
            ratio = 0
            for i in self.__spaths:
                if (i != curr):
                    for j in self.__spaths[i]:
                        if (i == curr or j == curr):
                            continue
                        else:
                            x = 0
                            allpaths = self.__spaths[i][j]
                            if (len(allpaths) == 0):
                                continue
                            elif (allpaths[0] is list):  # multiple paths
                                for l in allpaths:
                                    if (curr in l):
                                        x += 1
                                ratio += (x / len(allpaths))
                            else:
                                if (curr in allpaths):
                                    ratio += 1
            self.__bcrdict[curr] = ratio
            c += 1
            if (c % 100 == 0):
                print("|| Success || : BCR rank obtained for :", c, " Users--")

    # Closeness Centrality ::
    def __clsCentRank(self, xmode=1, filepath=" ", ms=10,
                      xmode1=1):  # using apsp for getting Closeness-Centrality ranks
        self.__shortestPaths(xmode, xmode1, filepath,
                             users=self.__users, net=self.__user_friends)
        self.__ccrdict = {x: 0 for x in self.__users}
        sleep(2)
        print("|| Alert || : Staring the process of Closeness Centrality Ranking...\n")
        c = 0
        for curr in self.__users:
            dcon = 0  # disconnected
            con = 0  # connected
            for f in self.__spaths[curr]:
                if (f == curr):
                    continue
                allpaths = self.__spaths[curr][f]
                l = len(allpaths)
                if (l == 0):
                    dcon += ms  # ms = maximum dummy value
                elif (l > 0):
                    if (allpaths[0] is list):
                        con += len(allpaths[0])  # multiple paths
                    else:
                        con += l
            self.__ccrdict[curr] = (dcon + con) / len(self.__users)
            c += 1
            if (c % 100 == 0):
                print("|| Success || : CCR rank obtained for :", c, " Users--")

    def get_csv_ranks_with_nx(self, mode="bcr"):
        network = {}
        user_friends = {}
        with open('./Output/Social Network_saved_data.json') as rf:
            network = json.load(rf)
            for i, j in network.items():
                user_friends[str(i)] = j['friends']
        g = nx.Graph()
        g.add_nodes_from(user_friends.keys())

        g = nx.Graph()
        g.add_nodes_from(user_friends.keys())

        for k, v in user_friends.items():
            g.add_edges_from(([(t, k) for t in v]))

        if mode == "bcr":
            b = nx.betweenness_centrality(g)
            csv_columns = ['Name', 'ID', 'Bet-Cent Rank Score']
            csv_file = "./Output/bcr_rank_output_NEW.csv"
            with open(csv_file, 'w+', newline='') as csvfile:
                writer = DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for i in b.keys():
                    writer.writerow({'Name': self.getName(
                        str(i)), 'ID': i, 'Bet-Cent Rank Score': b[i]})

        elif mode == "ccr":
            c = nx.closeness_centrality(g)
            csv_columns = ['Name', 'ID', 'Cls-Cent Rank Score']
            csv_file = "./Output/ccr_rank_output_NEW.csv"

            with open(csv_file, 'w+', newline='') as csvfile:
                writer = DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for i in c.keys():
                    writer.writerow({'Name': self.getName(
                        str(i)), 'ID': i, 'Cls-Cent Rank Score': c[i]})
        else:
            print("Something went wrong!")
        return

    # Printing Ranks(Page, User, Tunk ranks, BCR ranks, CCR ranks) ::
    def printCSV_Ranks(self, name="page", mode=1, xmode=0, xmode1=0, sfpath=" ", filepath="/", damp=0.85, epoch=40,
                       maxScore=10, mul=10e4) -> None:  # applies Ranking algo and saves the result in CSV
        if (name == "page" and mode == 1):  # for Page Rank Algo mode 1
            if (True):
                self.__page_rank_algo(damp, epoch)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "Page Rank", "In-Degree", "Out-Degree"])
                    writer.writeheader()
                    for k in sorted(self.__page_rank.keys(), key=lambda x: self.__page_rank[x]['node_rank'],
                                    reverse=True):
                        x = self.__page_rank[k]
                        writer.writerow(
                            {"Name": self.getName(str(k)), "User Id": str(k), "Page Rank": str(x["node_rank"]),
                             "In-Degree": str(len(x["in"])), "Out-Degree": str(x["out"])})
                # self.__pr=1
            # Clearing
            self.__page_rank.clear()

        elif (name == "user" and mode == 1):  # for User Rank Algo mode 1
            if (True):
                self.__user_rank_2_algo(epoch)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "User Rank(In)", "In-Degree", "Out-Degree"])
                    writer.writeheader()
                    for k in sorted(self.__user_rank_2.keys(), key=lambda x: self.__user_rank_2[x], reverse=True):
                        x = self.__user_rank_2[k]
                        writer.writerow({"Name": self.getName(str(k)), "User Id": str(k), "User Rank(In)": str(x),
                                         "In-Degree": str(len(self.__degree[k]["in"])),
                                         "Out-Degree": str(len(self.__degree[k]["out"]))})
                # self.__ur2=1
            # Clearing
            self.__degree.clear()
            self.__user_rank_2.clear()

        elif (name == "user" and mode == 2):  # for User Rank Algo mode 2
            if (True):
                self.__user_rank_3_algo(epoch)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "User Rank(Out)", "In-Degree", "Out-Degree"])
                    writer.writeheader()
                    for k in sorted(self.__user_rank_3.keys(), key=lambda x: self.__user_rank_3[x], reverse=True):
                        x = self.__user_rank_3[k]
                        writer.writerow({"Name": self.getName(str(k)), "User Id": str(k), "User Rank(Out)": str(x),
                                         "In-Degree": str(len(self.__degree[k]["in"])),
                                         "Out-Degree": str(len(self.__degree[k]["out"]))})
                # self.__ur3=1
            # Clearing
            self.__degree.clear()
            self.__user_rank_3.clear()

        elif (name == "tunk" and mode == 1):
            if (True):
                self.__tunk_rank_1_algo(epoch, mul)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "Tunk Rank(In)", "In-Degree", "Out-Degree"])
                    writer.writeheader()
                    for k in sorted(self.__tunk_rank_1.keys(), key=lambda x: self.__tunk_rank_1[x], reverse=True):
                        x = self.__tunk_rank_1[k]
                        writer.writerow({"Name": self.getName(str(k)), "User Id": str(k), "Tunk Rank(In)": str(x),
                                         "In-Degree": str(len(self.__degree[k]["in"])),
                                         "Out-Degree": str(len(self.__degree[k]["out"]))})
                # self.__tr1=1
            # Clearing
            self.__degree.clear()
            self.__tunk_rank_1.clear()

        elif (name == "tunk" and mode == 2):
            if (True):
                self.__tunk_rank_2_algo(epoch, mul)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "Tunk Rank(Out)", "In-Degree", "Out-Degree"])
                    writer.writeheader()
                    for k in sorted(self.__tunk_rank_2.keys(), key=lambda x: self.__tunk_rank_2[x], reverse=True):
                        x = self.__tunk_rank_2[k]
                        writer.writerow({"Name": self.getName(str(k)), "User Id": str(k), "Tunk Rank(Out)": str(x),
                                         "In-Degree": str(len(self.__degree[k]["in"])),
                                         "Out-Degree": str(len(self.__degree[k]["out"]))})
                # self.__tr2=1
            # Clearing
            self.__degree.clear()
            self.__tunk_rank_2.clear()

        elif (name == "bcr" and mode == 1):  # BCR Ranks
            if (True):
                self.__betCentRank(xmode=xmode, filepath=sfpath, xmode1=xmode1)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "Bet-Cent Rank Score"])
                    writer.writeheader()
                    for k in sorted(self.__bcrdict.keys(), key=lambda x: self.__bcrdict[x], reverse=True):
                        x = self.__bcrdict[k]
                        writer.writerow(
                            {"Name": self.getName(str(k)), "User Id": str(k), "Bet-Cent Rank Score": str(x)})
            # Clearing
            self.__spaths.clear()
            self.__bcrdict.clear()

        elif (name == "ccr" and mode == 1):  # CCR Ranks
            if (True):
                maxScore = len(self.__users) + 1
                self.__clsCentRank(xmode=xmode, filepath=sfpath,
                                   ms=maxScore, xmode1=xmode1)
                with open(filepath, 'w+', encoding='utf-8', newline='') as f:
                    writer = DictWriter(
                        f, fieldnames=["Name", "User Id", "Cls-Cent Rank Score"])
                    writer.writeheader()
                    for k in sorted(self.__ccrdict.keys(), key=lambda x: self.__ccrdict[x],
                                    reverse=False):  # reverse False for nearest ones
                        x = self.__ccrdict[k]
                        writer.writerow(
                            {"Name": self.getName(str(k)), "User Id": str(k), "Cls-Cent Rank Score": str(x)})
            # Clearing
            self.__spaths.clear()
            self.__ccrdict.clear()

        else:
            print("|| Failure || : Check your inputs for {} Ranking Algorighm!!\n".format(
                name.upper()))
        print("|| Success || : You can check the output CSV of '{} Rank Algorithm' (Mode {}) in--> {}  -path\n".format(
            name.upper(), mode, filepath))

    # Lets Draw the Network!!
    def __printGraphInfo(self) -> None:
        print("Nodes: ", self.__Graph.nodes())
        print("Edges: ", self.__Graph.edges())

    def __randomNodeColors(self) -> tuple:
        return (random.random(), random.random(), random.random(), random.random())

    def drawGraph(self, un=" ", scale=1, k=5, iterations=50, node_color=1, with_labels=True, font_weight='normal',
                  font_size=8, font_color='black', node_size=100) -> None:
        self.__Graph = nx.DiGraph()
        users = [un]
        uid = {}
        for i in self.__users:
            if (self.getName(i) == un):
                uid[un] = i
                for j in self.__network[i]['friends']:
                    uid[self.getName(j)] = j
                    users.append(self.getName(j))
                break
        self.__Graph.add_nodes_from(users)
        for u in users:
            for f in self.__network[uid[u]]['friends']:
                if (f in uid.values()):
                    self.__Graph.add_edge(u, self.getName(f))
        print("|| Alert || : Total number of friends of {} : {}.\n".format(
            un, len(users) - 1))
        if (node_color == 1):
            color_map = []
            for f in self.__Graph.nodes():
                color_map.append(self.__randomNodeColors())
        else:
            color_map = ['white' for i in self.__users]
        print("|| Success || : Ploting the whole Network for \"{}\"... It may take a while for plotting...".format(un))
        sleep(5)
        # self.__printGraphInfo()
        p = nx.spring_layout(self.__Graph, scale=scale,
                             k=k, iterations=iterations)
        nx.draw(self.__Graph, pos=p, node_color=color_map, with_labels=with_labels, font_weight=font_weight,
                font_size=font_size, font_color=font_color, node_size=node_size)
        plt.show()
        # plt.savefig(filepath+"/Social_Network_Pic.png")
        # print("\nYou can check the output Picture of the Network in--> {} -path\n".format(filepath+"/Social_Network_Pic.png"))
        # Clearing
        self.__Graph.clear()
        return

    def calculate_Ai_score(self, account_based_features_filepath, mentions_count_filepath):
        """
        :param account_based_features_filepath:
        :param mentions_count_filepath:
        :return:
        A(i) = (F1 + M4 + RP3 + RT3) / n
        F1 = Number of followers
        M4 = Number of users mentioning the author
        RP3 = Number of users who have replied author’s tweets
        RT3 = Number of users who have retweeted author’s tweets
        n = number of users
        """
        print("Calculating Acquaintance Score A ( i ) ")

        try:
            account_based_features = pd.read_csv(
                "./Data/account_based_features.csv")
            mention_count = pd.read_csv("./Data/mentions_count.csv")  # M4
            reply_and_retweet_count = pd.read_csv(
                "./Data/reply_and_retweet_count.csv")  # RP3
            usernames = mention_count["User_name"].tolist()

            rt_array = []
            Followers_dict = {}
            Followers_dict_1 = {}
            mention_dict = {}
            reply_array = []
            nf = []

            for i, j in zip(account_based_features["User Name"], account_based_features["Followers"]):
                Followers_dict[i] = j
            c = 0
            for i in usernames:
                c = c + 1
                if i in list(Followers_dict.keys()):
                    Followers_dict_1[i] = Followers_dict[i]
                else:
                    nf.append(i)
                    print("Not found --> ", i)

            for i in nf:
                usernames.remove(i)
            # len(usernames)

            for username in usernames:
                mention_dict[username] = mention_count[mention_count['User_name'] == username]['Mention_count'].values[
                    0]
                reply_array.append(
                    reply_and_retweet_count[reply_and_retweet_count['User_name']
                                            == username]['RP3'].values[0]
                )
                rt_array.append(
                    reply_and_retweet_count[reply_and_retweet_count['User_name'] == username]['RT3'].values[0])

            n = len(usernames)

            with open('./Output/Acquaintance_score(Ai).csv', 'w+', encoding='utf-8', newline='') as f:
                writer = DictWriter(
                    f, ['User_name', 'Follower_count(F1)', 'M4', 'RT3', 'RP3', 'Acquaintance_score'])
                writer.writeheader()
                for i in range(n):
                    p = (Followers_dict_1[usernames[i]] +
                         mention_dict[usernames[i]] + rt_array[i] + reply_array[i])
                    writer.writerow({'User_name': usernames[i], 'Follower_count(F1)': Followers_dict_1[usernames[i]],
                                     'M4': mention_dict[usernames[i]], 'RT3': rt_array[i], 'RP3': reply_array[i],
                                     'Acquaintance_score': p})
        except Exception as e:
            print(e)
            return False
        return True

    def calculate_AAJ(self):
        """
        Acquaintance-Affinity Score AA ( j )
        AA(j) = Σ A(i) * #replies of i to j / #replies of i
                + Σ A(i) * #mentions of i to j / #mentions of i
                + Σ A(i) * #retweets of i to j / #retweets of i
        :param abf_path:
        :return:
        """
        print("Calculating Acquaintance-Affinity Score AA ( j )...")

        ai_score = pd.read_csv("./Output/Acquaintance_score.csv")
        reply_and_retweet_count = pd.read_csv(
            "./Data/reply_and_retweet_count.csv")
        mention_count = pd.read_csv("./Data/mentions_count.csv")

        user_list = ai_score['User_name'].tolist()

        Acquaitance_score = {}
        for i, j in zip(ai_score['User_name'], ai_score['Acquaintance_score']):
            Acquaitance_score[i] = j

        AAj = {}  # Acquaintance-Affinity Score AA ( j ) dictionary
        reply_dict = {}
        reply_matrix = pd.read_csv("./Data/reply_matrix.csv", index_col=0)

        mat_mention = pd.read_csv("./Data/mention_matrix.csv", index_col=0)
        mention_dict = {}

        mat_rt = pd.read_csv("./Data/retweet_matrix.csv", index_col=0)
        rt_dict = {}

        for username in user_list:
            reply_dict[username] = \
                reply_and_retweet_count[reply_and_retweet_count['User_name']
                                        == username]['RP3'].values[0]
            mention_dict[username] = mention_count[mention_count['User_name']
                                                   == username]['Mention_count'].values[0]
            rt_dict[username] = reply_and_retweet_count[reply_and_retweet_count['User_name'] == username]['RT3'].values[
                0]

        for j in user_list:
            Erp = 0
            for i in user_list:
                if i != j and reply_dict[i] != 0:
                    Erp += Acquaitance_score[i] * \
                        (reply_matrix[j][i] / reply_dict[i])

            AAj[j] = Erp

        for j in user_list:
            Em = 0
            for i in user_list:
                if i != j and mention_dict[i] != 0:
                    Em += Acquaitance_score[i] * \
                        (mat_mention[j][i] / mention_dict[i])

            AAj[j] += Em

        for j in user_list:
            Ert = 0
            for i in user_list:
                if i != j and rt_dict[i] != 0:
                    Ert += Acquaitance_score[i] * (mat_rt[j][i] / rt_dict[i])

            AAj[j] += Ert

        print(AAj)
        aaj_score = pd.DataFrame.from_dict(AAj, orient='index', columns=[
                                           'Acquaintance-Affinity Score AA ( j )'])
        aaj_score.to_csv(
            "./Output/Acquaintance-Affinity Score AA ( j ).csv", index=True)
        print("...............Done")

    def calculate_AAIj(self):
        print("Calculating Acquaintance-Affinity-Identification Score AAI ( j )...")
        # Opening JSON file
        with open('./Data/friends_library.json', 'r') as openfile:
            # Reading from json file
            json_dict = json.loads(openfile.read())

        df = pd.read_csv('./Output/Acquaintance-Affinity Score AA ( j ).csv')

        df1 = pd.read_csv('./Data/account_based_features.csv')

        ID_dict = {}  # create a dictionary where keys are ID and value are Usernames from account_based_features
        for i in df['Unnamed: 0']:
            p = df1.loc[df1['User Name'] == i]['User ID']
            p = p.to_string().split()[1]
            p = p.strip('id')
            ID_dict[p] = i

        friend_list = {}

        for i in ID_dict.keys():  # create a friendlist with ids
            p = i
            q = 'id' + str(i)
            if p in json_dict.keys() and len(json_dict[p]) != 0:

                friend_list[i] = json_dict[p].split("-")
            elif q in json_dict.keys() and len(json_dict[q]) != 0:

                friend_list[i] = json_dict[q].split("-")
            else:
                continue

        friend_list1 = {}
        f = {}
        for i in friend_list.keys():  # create a friendlist with names
            l = []
            for j in friend_list[i]:
                if j in friend_list.keys():
                    l.append(ID_dict[j])
            f[ID_dict[i]] = len(l)
            friend_list1[ID_dict[i]] = l

        df2 = pd.DataFrame.from_dict(
            f, orient='index', columns=['friends_in_dataset'])
        df2.to_csv("./Output/[Internal]Friend_in_dataset.csv",
                   index=True)

        aai = {}
        follower_dict = {}  # dictionary with following number
        for i in df['Unnamed: 0']:
            p = df1.loc[df1['User Name'] == i]['Following']
            p = p.to_string().split()[1]
            follower_dict[i] = float(p)

        aa = {}
        for i in df['Unnamed: 0']:  # dictionary with AA(j)
            p = df.loc[df['Unnamed: 0'] ==
                       i]['Acquaintance-Affinity Score AA ( j )']
            p = p.to_string().split()[1]
            p = float(p)
            aa[i] = p

        for i in friend_list1.keys():
            s = 0
            for j in friend_list1[i]:
                if follower_dict[j] != 0:
                    s += (aa[j] / follower_dict[j])
            # float("{0:.2f}".format(s))  if you want up to 5 decimal places
            aai[i] = s

        print(aai)
        df3 = pd.DataFrame.from_dict(aai, orient='index', columns=[
                                     'Acquaintance-Affinity-Identification Score AAI(j)'])
        df3.to_csv(
            "./Output/Acquaintance-Affinity-Identification Score AAI(j).csv",
            index=True)
        print("...............Done")

    #  unweighted k shell with networkx
    def check(self, h, d):
        f = 0  # there is no node of deg <= d
        for i in h.nodes():
            if h.in_degree(i) <= d:
                f = 1
                break
        return f

    # Find list of nodes with particular degree
    def find_nodes(self, h, it):
        set1 = []
        for i in h.nodes():
            if h.in_degree(i) <= it:
                set1.append(i)
        return set1

    def unweighted_k_shell_with_nx_out_degree(self, network):
        out_deg_network = {}

        for i in network.keys():
            out_deg_network[str(i)] = network[i]['out']
            # print(i,network[i]['out'])

        g1 = nx.DiGraph()
        g1.add_nodes_from(out_deg_network.keys())
        for k, v in out_deg_network.items():
            g1.add_edges_from(([(t, k) for t in v]))
            # Check if there is any node left with degree d

        # Create graph object and add nodes

        # Copy the graph
        h = g1.copy()
        it = 0

        # Bucket being filled currently
        tmp = []

        # list of lists of buckets
        buckets = []
        while 1:
            flag = self.check(h, it)
            if flag == 0:
                it += 1
                buckets.append(tmp)
                tmp = []
            if flag == 1:
                node_set = self.find_nodes(h, it)
                # print(node_set,it)
                for each in node_set:
                    h.remove_node(each)
                    tmp.append(each)
            if h.number_of_nodes() == 0:
                buckets.append(tmp)
                break
        k_shell = {}
        it = 1
        for i in buckets:
            # print(len(i))
            if len(i) == 0:
                pass
                # print(i,it)
            else:
                for j in i:
                    k_shell[j] = it
            it += 1
        csv_columns = ['ID', 'username', 'K_shell_value']
        csv_file = "./Output/Unweighted_K-Shell(Out_Degree)_Output_NEW.csv.csv"

        with open(csv_file, 'w+', newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for i in k_shell.keys():
                writer.writerow({'ID': i, 'username': self.getName(
                    i), 'K_shell_value': k_shell[i]})

    def unweighted_k_shell_with_nx(self, mode='in'):
        network = {}
        user_friends = {}
        with open('./Output/[Internal]In_Out_Degrees_Output.json') as rf:
            network = json.load(rf)
        # for out degree
        if mode == 'out':
            self.unweighted_k_shell_with_nx_out_degree(network)

        # for in degree
        in_deg_network = {}
        for i in network.keys():
            in_deg_network[str(i)] = network[i]['in']
            # print(i,network[i]['in'])
        g = nx.DiGraph()
        g.add_nodes_from(in_deg_network.keys())
        for k, v in in_deg_network.items():
            g.add_edges_from(([(t, k) for t in v]))

        # Create graph object and add nodes

        # Copy the graph
        h = g.copy()
        it = 0

        # Bucket being filled currently
        tmp = []

        # list of lists of buckets
        buckets = []
        while 1:
            flag = self.check(h, it)
            # print(flag)
            if flag == 0:
                it += 1
                buckets.append(tmp)
                tmp = []
            if flag == 1:
                node_set = self.find_nodes(h, it)
                # print(node_set,it)
                for each in node_set:
                    h.remove_node(each)
                    tmp.append(each)
            if h.number_of_nodes() == 0:
                # print(tmp)
                buckets.append(tmp)
                break
        k_shell = {}
        it = 1
        for i in buckets:
            # print(len(i))
            if len(i) == 0:
                pass
                # print(i,it)
            else:
                for j in i:
                    k_shell[j] = it
            it += 1
        csv_columns = ['ID', 'username', 'K_shell_value']
        csv_file = "./Output/Unweighted_K-Shell(In_Degree)_Output_NEW.csv"

        with open(csv_file, 'w+', newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for i in k_shell.keys():
                writer.writerow({'ID': i, 'username': self.getName(
                    i), 'K_shell_value': k_shell[i]})

    def get_SIR_score(self, abm, abf, username, dt, npts, N):
        print("catculating SIR Score")

        follower_count = abf[abf['User Name']
                             == username]['Followers'].values[0]
        tweet_rate = abm[abm['user_name'] ==
                         username]['Avg. Tweet Rate(per Month)'].values[0] / 30
        retweet_rate = abm[abm['user_name'] ==
                           username]['Avg. Retweet Rate(per Month)'].values[0] / 30

        S = np.zeros(npts)  # susceptible
        I = np.zeros(npts)  # infective
        beta = 1/follower_count  # infection rate
        gamma = (1.0/14.0)  # recovery rate

        I[0] = follower_count  # initial infective proportion
        S[0] = N - I[0]  # initial susceptible

        for i in range(npts-1):
            ds = int(S[i] - beta*(S[i]*I[i])*dt)
            di = int(I[i] + (beta*S[i]*I[i]-gamma*I[i])*dt)
            if di >= N:
                S[i+1] = 0
                I[i+1] = N
                break
            else:
                S[i+1] = ds
                I[i+1] = di

    #     calculating score
        t = (np.where(I == I.max())[0][0] + 1) * dt
        time_per_user = t / I.max()
        rem = 1 if N - I.max() <= 0 else N - I.max()

        score = t + (rem * time_per_user)
        return score*24

    def calculate_SIR(self):
        print("catculating SIR Score...")
        try:
            abm = pd.read_csv(
                "./Data/account_based_measures.csv")
            abf = pd.read_csv(
                "./Data/account_based_features.csv")

            ndays = 30
            dt = 1/24  # time step in days
            npts = int(ndays/dt)
            N = 90000

            usernames = abf['User Name'].tolist()
            # print(len(usernames))
            for i in usernames:
                if i not in abm['user_name'].tolist():
                    usernames.remove(i)
            # print(len(usernames))

            with open('./Output/SIR_score.csv', 'w+', newline='') as csvfile:
                fieldnames = ['username', 'score']
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                count = 0
                for username in usernames:
                    # score = self.get_SIR_score(abm, abf, username, dt, npts, N)

                    follower_count = abf[abf['User Name']
                                         == username]['Followers'].values[0]
                    tweet_rate = abm[abm['user_name'] ==
                                     username]['Avg. Tweet Rate(per Month)'].values[0] / 30
                    retweet_rate = abm[abm['user_name'] ==
                                       username]['Avg. Retweet Rate(per Month)'].values[0] / 30

                    S = np.zeros(npts)  # susceptible
                    I = np.zeros(npts)  # infective
                    beta = 1/follower_count if follower_count != 0 else 1  # infection rate
                    gamma = (1.0/14.0)  # recovery rate

                    I[0] = follower_count  # initial infective proportion
                    S[0] = N - I[0]  # initial susceptible

                    for i in range(npts-1):
                        ds = int(S[i] - beta*(S[i]*I[i])*dt)
                        di = int(I[i] + (beta*S[i]*I[i]-gamma*I[i])*dt)
                        if di >= N:
                            S[i+1] = 0
                            I[i+1] = N
                            break
                        else:
                            S[i+1] = ds
                            I[i+1] = di

                #     calculating score
                    t = (np.where(I == I.max())[0][0] + 1) * dt
                    time_per_user = (t / I.max()) if I.max() != 0 else 1
                    rem = 1 if N - I.max() <= 0 else N - I.max()

                    score = t + (rem * time_per_user)

                    # print(count, ":", i, "-->" , score)
                    count += 1
                    writer.writerow({'username': username, 'score': score})

                    if count % 100 == 0:
                        print(count, "users done")

            out_df = pd.read_csv('./Output/SIR_score.csv')
            out_df.sort_values(by=['score'], inplace=True)
            out_df.to_csv('./Output/SIR_score.csv', index=False)
            return True

        except Exception as e:
            print(e)
            return False
