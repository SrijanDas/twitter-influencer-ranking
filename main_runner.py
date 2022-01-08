import os
from time import sleep
import traceback
from Social_Network import *


def deleteFiles(cwd):
    fpath = cwd + "/Output"
    for i in os.listdir(fpath):
        fname = fpath + '/' + i
        os.remove(fname)


def checkIn(cwd) -> bool:
    dpath = cwd + "/Data".replace('\\', '/')
    need = ['friends_library.json', 'account_based_features.csv', 'account_based_measures.csv']
    l = os.listdir(dpath)
    for i in need:
        if (i not in l): return False
    else:
        return True


def introduction(cwd):
    starbox(2)
    sleep(1)
    print(
        "\n/////     Welcome to the Project-UI of \"Influential User Identification using Twitter\".                     \\\\\\\\\\")
    sleep(1)
    print(
        "/////     Project Mentor: Kumar Gaurav Das || Project Members: Mourima Biswas, Avyudoy Ghosh, Deep Roy.     \\\\\\\\\\\n")
    starbox(r=2, c=70)  # 155 for full screen
    print("\nChecking Input folder...Organizing \"Output\" folder and Staring the Project Internals......")
    # Input
    sleep(2)
    if (checkIn(cwd)):
        print("\n|| CHECKED || : Input Files are in the {} -Folder\n".format(cwd.replace('\\', '/') + "/Data"))
    else:
        print(
            "\n|| Failure || : Input Files are missing from the {} -Folder\n".format(cwd.replace('\\', '/') + "/Data"))
    # Output folder creation
    sleep(2)
    if ('Output' not in os.listdir(cwd)):
        os.mkdir(cwd + "/Output")
    else:
        s = cwd + "/Output"
        print("OUTPUT FOLDER  - " + s.replace('\\', '/'))
        for i in sorted(os.listdir(cwd + "/Output")):
            print("|-- " + i)
        print(
            "\n|| Alert || : Already found \"Output\" folder and showing it's contents above. Now you choose--> \nDo you want to delete it's content(s) and start with a Clean Output Folder[Press Y/y] || You want to  keep all the files in Output folder as it is and want to create new Output Files along with them[Press N/n]?")
        print("--> Press Y/y for Yes")
        print("--> Press N/n for No")
        print("|| Enter your choice --> ", end="")
        opt = str(input())
        if (opt in ['Y', 'y']):
            deleteFiles(cwd)
    print("|| Advancing with this setting..")
    print("...\n......\n.........\n-----------------------------")


### Creating Social Network Object
def start(files) -> Social_Network:
    print("Initiating process to make the Social Network.\nYou can choose the option to make it...")
    sleep(2)
    print("--> Press 1 to Make from available previously created saved file of a network (For faster network creation)")
    print("--> Press 2 to Make a new network from scratch")
    print("Enter your choice--> ", end="")
    n = int(input())
    print("\nDo you want to save the network for future use?\n--> Press Y/y for \"Yes\"\n--> Press N/n for \"No\"")
    print("|| Enter your choice--> ", end="")
    s = str(input())
    t = True if (s in ["Y", 'y']) else False
    if (n == 1):
        sn = Social_Network(mode=0, libf=files[4])
    elif (n == 2):
        sn = Social_Network(mode=1, save=t, libf=files[1], infof=files[2], agef=files[3], savepath1=files[4],
                            savepath2=files[21])
    else:
        print("|| Failure || : Wrong inputs for Network Creation...Recreating\n")
        return start(files)
    sn.get_usersCount()
    sn.getCsvUsers(files[0])
    return sn


def optList() -> int:  # feature list
    print("-------------------------------------------------------------------------------------")
    print("--> Press 0 to Exit this interface")
    print("--> Press 1 to get \"K-Shell\" -Ranking Output")
    # print("--> Press 2 to get \"TOPSIS\" -Ranking Output")
    print("--> Press 2 to get \"Page Rank\" -Ranking Output")
    print("--> Press 3 to get \"User Rank\" -Ranking Output")
    print("--> Press 4 to get \"Tunk Rank\" -Ranking Output")
    print("--> Press 5 to get \"Betweenness Centrality\" -Ranking Output")
    print("--> Press 6 to get \"Closeness Centrality\" -Ranking Output")
    print("--> Press 7 to plot and see \"Visual Representation\" of a User in created Social Network")
    print("|| Enter your choice of Operation --> ", end="")
    opt = int(input())
    if (opt not in range(9)):
        print("|| Failure || : Wrong Inputs for Operation Selection!!...Try Again->\n")
        optList()
    else:
        return opt


def operate(opt, sn, files):  # Operate according to the choice->"opt"
    if (opt == 1):
        doKshell(sn, files)
    # elif(opt==2): doTopsis(sn, files)
    elif (opt == 2):
        doPageRank(sn, files)
    elif (opt == 3):
        doUserRank(sn, files)
    elif (opt == 4):
        doTunkRank(sn, files)
    elif (opt == 5):
        doBCR(sn, files)
    elif (opt == 6):
        doCCR(sn, files)
    elif (opt == 7):
        doDraw(sn)
    else:
        print("|| Failure || : Wrong Inputs for Ranking Selection!!\n")


def doKshell(sn, files):
    print("\n|| K-Shell Ranking || selected->")
    print("--> Press 1 to get Unweighted K-Shell Output of the network")
    print("--> Press 2 to get Weighted K-Shell Output of the network")
    print("|| Enter your choice--> ", end="")
    opt = int(input())
    if (opt not in [1, 2]):
        print("|| Failure || : Wrong Inputs for K-Shell Ranking Selection!!...Try Again->\n")
        doKshell(sn, files)
    else:
        if (opt == 1):  # UnWeighted
            print("\n|| Unweighted K-Shell Ranking || selected->")
            print("--> Press 1 to get Unweighted K-Shell Output for In-degree of the network")
            print("--> Press 2 to get Unweighted K-Shell Output for Out-degree of the network")
            print("|| Enter your choice--> ", end="")
            n = int(input())
            if (n not in [1, 2]):
                print("|| Failure || : Wrong Inputs for Unweighted K-Shell Ranking Selection!!...Try Again->\n")
                doKshell(sn, files)
            else:
                if (n == 1):
                    sn.printCSV_ukshellRank(mode="in", inputfile=files[3], outputfile=files[14], infofiles={
                        'IODegree': files[24],
                        'UserDegrees': files[25]
                    })
                else:
                    sn.printCSV_ukshellRank(mode="out", inputfile=files[3], outputfile=files[19], infofiles={
                        'IODegree': files[24],
                        'UserDegrees': files[26]
                    })
        else:  # Weighted
            print("\n|| Weighted K-Shell Ranking || selected->")
            print("--> Press 1 to get Weighted K-Shell Output for In-degree of the network")
            print("--> Press 2 to get Weighted K-Shell Output for Out-degree of the network")
            print("--> Press 3 to get [Not Converted]-Weighted K-Shell Output for In-degree of the network")
            print("--> Press 4 to get [Not Converted]-Weighted K-Shell Output for Out-degree of the network")
            print("|| Enter your choice--> ", end="")
            n = int(input())
            if (n not in [1, 2, 3, 4]):
                print("|| Failure || : Wrong Inputs for Weighted K-Shell Ranking Selection!!...Try Again->\n")
                doKshell(sn, files)
            else:
                if (n == 1):
                    sn.printCSV_wkshellRank(mode="in", convertFlag=True, inputfile=files[3], outputfile=files[15],
                                            infofiles={
                                                'IODegree': files[24],
                                                'UserDegreesBefore': files[29],
                                                'UserDegrees': files[31]
                                            })
                elif (n == 2):
                    sn.printCSV_wkshellRank(mode="out", convertFlag=True, inputfile=files[3], outputfile=files[20],
                                            infofiles={
                                                'IODegree': files[24],
                                                'UserDegreesBefore': files[30],
                                                'UserDegrees': files[32]
                                            })
                elif (n == 3):
                    sn.printCSV_wkshellRank(mode="in", convertFlag=False, inputfile=files[3], outputfile=files[22],
                                            infofiles={
                                                'IODegree': files[24],
                                                'UserDegreesBefore': files[29],
                                                'UserDegrees': files[27]
                                            })
                else:
                    sn.printCSV_wkshellRank(mode="out", convertFlag=False, inputfile=files[3], outputfile=files[23],
                                            infofiles={
                                                'IODegree': files[24],
                                                'UserDegreesBefore': files[30],
                                                'UserDegrees': files[28]
                                            })


# Topsis
# def doTopsis(sn, files):
#     print("\n|| TOPSIS Ranking || selected->")
#     print("--> Press 1 to get TOPSIS Output for In-degree of the network")
#     print("--> Press 2 to get TOPSIS Output for Out-degree of the network")
#     print("|| Enter your choice--> ", end="")
#     n=int(input())
#     if(n not in [1, 2]):
#         print("|| Failure || : Wrong Inputs for TOPSIS Ranking Selection!!...Try Again->\n")
#         doTopsis(sn, files)
#     else:
#         print("|| Enter 7-weights based on User's features accordingly (Note: Sum of all given weights must be equal to 1) -->")
#         names="Avg. Tweet Rate(per Month),Avg. Retweet Rate(per Month),Avg. Reply Rate(per Month),Avg. Fav Count(per Month),Avg. Retweeted Count(per Month),Avg. Quote Count(per Month),k-shell value".split(',')
#         w=[]
#         c=1
#         for i in names:
#             print("--> {}.) Enter weight for \"{}\" = ".format(c, i), end="")
#             w.append(float(input()))
#             c+=1
#         print("|| Alert || : Sum of all weights: "+str(round(sum(w), 2)))
#         print("Starting TOPSIS...It may take a while....")
#         if(n==1): sn.printCSV_topsis(w, mode="in", inputfile=files[3], outputfile=files[16], outf=files[17])    # outf for topsis output, inpf, outf for kshell
#         else: sn.printCSV_topsis(w, mode="out", inputfile=files[3], outputfile=files[16], outf=files[21])    # outf for topsis output, inpf, outf for kshell

def doPageRank(sn, files):
    print("\n|| Page Rank || selected->")
    print("|| Do you want to provide damp and epoch(Press 1) OR keep it as default(Press 2)")
    print("|| Enter your choice--> ", end="")
    opt = int(input())
    d, ep = 0.85, 40
    if (opt == 1):
        print("|| Enter Damp and Epoch accordingly-->")
        print("--> Damp = ", end="")
        d = float(input())
        print("--> Epoch = ", end="")
        ep = int(input())
    else:
        print("|| Advancing with default settings for Page Rank...\n")
    sn.printCSV_Ranks(name="page", mode=1, filepath=files[10], damp=d, epoch=ep)


def doUserRank(sn, files):
    print("\n|| User Rank || selected->")
    print("Now there are 2-types of User Rank Method available for the Social Network.")
    # print("--> Press 1 for - Feature based User Rank algorithm where No epoch is needed")
    print("--> Press 1 for - User Rank algorithm based on Incoming Links where epoch can be provided")
    print("--> Press 2 for - User Rank algorithm based on Outgoing Links where epoch can be provided")
    print("|| Enter your choice--> ", end="")
    opt = int(input())
    ep, f = 40, 5
    if (opt in [1, 2]):
        f = 6 if (opt == 2) else 5
        print("|| Do you want to provide epoch(Press 1) OR keep it as default(Press 2)")
        print("|| Enter your choice--> ", end="")
        n = int(input())
        if (n == 1):
            print("--> Enter Epoch = ", end="")
            ep = int(input())
        sn.printCSV_Ranks(name="user", mode=opt, filepath=files[f], epoch=ep)
    else:
        print("|| Failure || : Wrong Inputs for User Rank Ranking Selection!!...Try Again->\n")
        doUserRank(sn, files)


def doTunkRank(sn, files):
    print("\n|| Tunk Rank || selected->")
    print("Now there are 2-types of Tunk Rank Method available for the Social Network.")
    print("--> Press 1 for - Tunk Rank algorithm based on Incoming Links where epoch can be provided")
    print("--> Press 2 for - Tunk Rank algorithm based on Outgoing Links where epoch can be provided")
    print("|| Enter your choice--> ", end="")
    opt = int(input())
    if (opt in [1, 2]):
        ep, f, m = 40, 11, 10e4
        f = 8 if (opt == 1) else 9
        print("|| Do you want to provide epoch, multiplier(Press 1) OR keep it as default(Press 2)")
        print("|| Enter your choice--> ", end="")
        n = int(input())
        if (n == 1):
            print("--> Enter Epoch = ", end="")
            ep = int(input())
            print("--> Enter Multiplier = ", end="")
            m = int(input())
        sn.printCSV_Ranks(name="tunk", mode=opt, filepath=files[f], epoch=ep, mul=m)
    else:
        print("|| Failure || : Wrong Inputs for Tunk Rank Ranking Selection!!...Try Again->\n")
        doTunkRank(sn, files)


def doBCR(sn, files):
    print("\n|| Betweenness Centrality || selected->")
    print(
        "|| Alert || : It may take a while for creating all the shortest paths in the network....Starting the process---\n")
    print("|| Alert || : Select your choice for Shortest Paths creation-->")
    print("--> Press 1 to Make from the network right now")
    print(
        "--> Press 2 to Make from available previously created saved file of Shortest paths of the network (For faster path creation)")
    print("|| Enter your choice--> ", end="")
    m, n = int(input()), 0
    if (m == 1):
        print(
            "\nDo you want to save the created Shortest Paths for future use?\n--> Press 1 for \"Yes\"\n--> Press 2 for \"No\"")
        print("|| Enter your choice--> ", end="")
        n = int(input())
    sn.printCSV_Ranks(name="bcr", mode=1, xmode=m, xmode1=n, sfpath=files[18], filepath=files[12])


def doCCR(sn, files):
    print("\n|| Closeness Centrality || selected->")
    print(
        "|| Alert || : It may take a while for creating all the shortest paths in the network....Starting the process---\n")
    print("|| Alert || : Select your choice for Shortest Paths creation-->")
    print("--> Press 1 to Make from the network right now")
    print(
        "--> Press 2 to Make from available previously created saved file of Shortest paths of the network (For faster rank generation)")
    print("|| Enter your choice--> ", end="")
    m, n = int(input()), 0
    if (m == 1):
        print(
            "\nDo you want to save the created Shortest Paths for future use?\n--> Press 1 for \"Yes\"\n--> Press 2 for \"No\"")
        print("|| Enter your choice--> ", end="")
        n = int(input())
    sn.printCSV_Ranks(name="ccr", mode=1, xmode=m, xmode1=n, sfpath=files[18], filepath=files[13])


def doDraw(sn):
    print("\n|| Visual Representation || selected->")
    print(
        "|| You can plot sub-network of any user in the Social Network. You just have to mention the User-Name of that User.")
    print("|| Enter User Name of that particular user --> ", end="")
    name = str(input())
    print("Do you want to provide labels font size, and node size(Press 1) OR keep it as default(Press 2)")
    print("|| Enter your choice--> ", end="")
    opt = int(input())
    wl, fs, ns = True, 8, 100
    if (opt == 1):
        print("--> Enter \"Y\" / \"N\" if you want Labels on the drawn nodes or not --> ", end="")
        wl = True if (input() in ["Y", "y"]) else False
        if (wl):
            print("--> Enter the Font-Size  --> ", end="")
            fs = int(input())
        print("--> Enter the Node-Size --> ", end="")
        ns = int(input())
    sn.drawGraph(un=name, with_labels=wl, font_size=fs, node_size=ns)


def checkOut():
    print("\n|| Output Watchlist || ::\n")
    curr = os.getcwd() + "/Output/"
    for i in os.listdir(curr):
        s = curr + i
        print("==> " + s.replace('\\', '/'))


def starbox(r=2, c=155):
    print()
    for i in range(r):
        for j in range(c):
            print("*", end="")
        print()


# Main
def main(files):
    # Intro
    introduction(cwd)
    # Creating SN
    sn = start(files)
    opt = 1
    while (opt != 0):
        sleep(1)
        try:
            choice = optList()
            if (choice != 0):
                operate(choice, sn, files)
            else:
                break
        except Exception:
            print("\n|| WARNING!! || :: Problem Occured...\n")
            traceback.print_exc()
            sleep(2)
            print("\nReturning to Operations List...")
            continue
    print("\nWant to see the paths of Output files?-> Press 1 for YES || Press 2 for NO")
    print("|| Enter your choice--> ", end="")
    n = int(input())
    if (n == 1): checkOut()
    sleep(1)
    print("\n/////     Thank you for using \"Influential User Identifaction Project UI\".     \\\\\\\\\\")
    sleep(1)
    starbox()


if __name__ == "__main__":
    # Files
    cwd = os.getcwd().replace("\\", "/")

    # PLEASE MAINTAIN THE INPUT FILE NAMES AND FOLDER NAMES
    # INPUT FILE LOCATIONS (CUSTOMIZABLE AFTER CURRENT WORKING DIRECTORY) -------***************
    files = {
        1: cwd + '/Data/friends_library.json'.replace('\\', '/'),  # Friends json
        2: cwd + '/Data/account_based_features.csv'.replace('\\', '/'),  # ACM output
        3: cwd + '/Data/account_based_measures.csv'.replace('\\', '/'),  # AVGM output

        # THE DON'T TOUCH ZONE***********************************************************************************************
        0: cwd + '/Output/usersList.csv'.replace('\\', '/'),  # user_name and ID
        4: cwd + '/Output/Social Network_saved_data.json'.replace('\\', '/'),  # faster input form saved network
        5: cwd + '/Output/user_rank_1_output.csv'.replace('\\', '/'),  # user rank 1
        6: cwd + '/Output/user_rank_2_output.csv'.replace('\\', '/'),  # user rank 2
        7: cwd + '/Output/user_rank_3_output.csv'.replace('\\', '/'),  # user rank 3
        8: cwd + '/Output/tunk_rank_1_output.csv'.replace('\\', '/'),  # tunk rank 1
        9: cwd + '/Output/tunk_rank_2_output.csv'.replace('\\', '/'),  # tunk rank 2
        10: cwd + '/Output/page_rank_output.csv'.replace('\\', '/'),  # page rank 1
        11: cwd + '/Output/'.replace('\\', '/'),  # folder path for network image
        12: cwd + '/Output/bcr_rank_output.csv'.replace('\\', '/').replace('\\', '/'),  # Betweenness Centrality Rank 1
        13: cwd + '/Output/ccr_rank_output.csv'.replace('\\', '/').replace('\\', '/'),  # Closeness Centrality Rank 1
        14: cwd + '/Output/Unweighted_K-Shell(In_Degree)_Output.csv'.replace('\\', '/'),  # used in ukshell
        15: cwd + '/Output/Weighted_K-Shell(In_Degree)_Output.csv'.replace('\\', '/'),  # used in wkshell
        # 16 : cwd + '/Output/__wkshell_for_topsis.csv'.replace('\\', '/'),                       # helper file used for kshell of topsis
        # 17 : cwd + '/Output/TOPSIS_Output(In_Degree).csv'.replace('\\', '/'),                            # used in topsis
        18: cwd + '/Output/Shortest_paths_saved_data.json',  # Saved Shortest paths
        19: cwd + '/Output/Unweighted_K-Shell(Out_Degree)_Output.csv'.replace('\\', '/'),
        20: cwd + '/Output/Weighted_K-Shell(Out_Degree)_Output.csv'.replace('\\', '/'),
        21: cwd + '/Output/Rejection_List.csv'.replace('\\', '/'),
        22: cwd + '/Output/Weighted_K-Shell_NotConverted(In_Degree)_Output.csv'.replace('\\', '/'),
        23: cwd + '/Output/Weighted_K-Shell_NotConverted(Out_Degree)_Output.csv'.replace('\\', '/'),

        # Internal files during kshells

        24: cwd + '/Output/[Internal]In_Out_Degrees_Output.json'.replace('\\', '/'),

        25: cwd + '/Output/[Internal]Unweighted_K-Shell(In_Degree)_Degrees_Output.csv'.replace('\\', '/'),
        26: cwd + '/Output/[Internal]Unweighted_K-Shell(Out_Degree)_Degrees_Output.csv'.replace('\\', '/'),

        27: cwd + '/Output/[Internal]Weighted_K-Shell_NotConverted(In_Degree)_Degrees_Output.csv'.replace('\\', '/'),
        28: cwd + '/Output/[Internal]Weighted_K-Shell_NotConverted(Out_Degree)_Degrees_Output.csv'.replace('\\', '/'),
        29: cwd + '/Output/[Internal]Weighted_K-Shell_Before_Converted(In_Degree)_Degrees_Output.csv'.replace('\\',
                                                                                                              '/'),
        30: cwd + '/Output/[Internal]Weighted_K-Shell_Before_Converted(Out_Degree)_Degrees_Output.csv'.replace('\\',
                                                                                                               '/'),
        31: cwd + '/Output/[Internal]Weighted_K-Shell_Converted(In_Degree)_Degrees_Output.csv'.replace('\\', '/'),
        32: cwd + '/Output/[Internal]Weighted_K-Shell_Converted(Out_Degree)_Degrees_Output.csv'.replace('\\', '/')

    }
    main(files)
