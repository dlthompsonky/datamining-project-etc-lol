# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import os
import sys
from riotwatcher import RiotWatcher, LolWatcher, ApiError #Importing Riotwatcher & other (Riot API)
from os.path import exists
import json
import urllib.request
from urllib.error import HTTPError
import time
#below are the Data-Plotting modules:
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd

plt.style.use("seaborn")
field_names_for_team_comps = ['Top', 'Jungle', 'Mid', 'Bot', 'Support', 'win / loss']


def initializeWinningCompFileHeader():
    if (not (exists("D:\PyCharmProjects\DataScienceProject\Comp_Data\winningComps.csv") == True)):
        with open("D:\PyCharmProjects\DataScienceProject\Comp_Data\winningComps.csv", 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(field_names_for_team_comps)
            print("Initializing Winning Comp File & Header")
            csvFile.close()


def initializeLosingCompFileHeader():
    if (not (exists("D:\PyCharmProjects\DataScienceProject\Comp_Data\losingComps.csv") == True)):
        with open("D:\PyCharmProjects\DataScienceProject\Comp_Data\losingComps.csv", 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(field_names_for_team_comps)
            print("Initializing Winning Comp File & Header")
            csvFile.close()


class WinningComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''
    dataToBeWritten = [[topLaner], [jungler], [midLaner], [botLaner], [support]]


class LosingComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''
    dataToBeWritten = [[topLaner], [jungler], [midLaner], [botLaner], [support]]


api_key = 'RGAPI-6c06a463-4aeb-4a6c-bbe4-f704af5a5259'
lolWatcher_api_key = LolWatcher(api_key)
region = 'na1'   #Working with the north american region

list_of_summoners = [lolWatcher_api_key.summoner.by_name(region, 'Sobileo'),
                     lolWatcher_api_key.summoner.by_name(region, 'Quantum Bebop'),
                     lolWatcher_api_key.summoner.by_name(region, 'No Gank Incoming'),
                     lolWatcher_api_key.summoner.by_name(region, 'FM Fallen'),
                     lolWatcher_api_key.summoner.by_name(region, 'Airpiane'),
                     lolWatcher_api_key.summoner.by_name(region, 'Ominous Cow')]


#Lists being used below
list_of_puuids = []
list_of_matches = []
list_of_matches_from_file = []
url_list = []
list_of_all_champions = []
list_of_winning_comps = []
list_of_losing_comps = []


def areThereMatchDuplicates():
    matchesSourcedFile = open("D:\PyCharmProjects\DataScienceProject\matchesSourcedFile.txt", 'r')
    list_of_matches_from_file = matchesSourcedFile.readlines()
    matchesSourcedFile.close()

    if(set(list_of_matches).isdisjoint(set(list_of_matches_from_file)) and not (len(list_of_matches_from_file) > 0)): #If they do not have duplicates and they are not empty
        return False
    else:
        return True


def checkForTextFile():#This is going to check for a text file before we start to manipulate data to put into it.
    matchesSourcedFile = open("D:\PyCharmProjects\DataScienceProject\matchesSourcedFile.txt", 'a+')
    if(areThereMatchDuplicates()):
        print("There are duplicates")
        return
    else:
        print("There are no duplicates")
        for x_match in list_of_matches:
            matchesSourcedFile.write(str(x_match))
            matchesSourcedFile.write('\n')
            #print(str(x_match))
    matchesSourcedFile.close()


def printListOfSummoners(): #Prints list of the summoner objects (This includes a lot of information)
    for x_puuid_id in list_of_summoners:
        list_of_puuids.append(x_puuid_id['puuid']) #This is to collect the accountId of each account
    for x_puuid in list_of_puuids:
        #print(lolWatcher_api_key.match.matchlist_by_puuid(region, x_puuid))
        for x_matches in range(0, 19): #If you don't put the range and 0, 19 in parenthesis, it will not loop through them all it will only go through the selected numbers
            list_of_matches.append(lolWatcher_api_key.match.matchlist_by_puuid(region, x_puuid)[x_matches])
    print("This is how many matches have been sourced : " + str(len(list_of_matches)))
    checkForTextFile()


def createRiotAPIUrl():
    for x_match in list_of_matches:
        url_list.append('https://americas.api.riotgames.com/lol/match/v5/matches/' + str(x_match) + '?api_key=' + str(api_key))


def getChampionList():
    try:
        for x_url in url_list:
            #print("Looping")
            time.sleep(.75) #Cannot request all of the requests at the same time, so we have to slow down the number of requests by using time.sleep
            with urllib.request.urlopen(x_url) as url:
                data = json.loads(url.read().decode())
                wc = WinningComp()
                lc = LosingComp()
                for i in range(0, 10):
                    if data['info']['participants'][i]['win'] is True:
                        if data['info']['participants'][i]['individualPosition'] == "TOP":
                            wc.topLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "JUNGLE":
                            wc.jungler = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "MIDDLE":
                            wc.midLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "BOTTOM":
                            wc.botLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "UTILITY":
                            wc.support = data['info']['participants'][i]['championName']
                    elif data['info']['participants'][i]['win'] is False:
                        if data['info']['participants'][i]['individualPosition'] == "TOP":
                            lc.topLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "JUNGLE":
                            lc.jungler = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "MIDDLE":
                            lc.midLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "BOTTOM":
                            lc.botLaner = data['info']['participants'][i]['championName']
                        elif data['info']['participants'][i]['individualPosition'] == "UTILITY":
                            lc.support = data['info']['participants'][i]['championName']
                    list_of_all_champions.append(data['info']['participants'][i]['championName'])
                list_of_winning_comps.append(wc)
                list_of_losing_comps.append(lc)
    except HTTPError as err:
        print(err) #There is better error handling than this. Just using pass as placement for big issues right now.
        pass


def printWinningCompJunglers():
    for wc in list_of_winning_comps:
        print(str(wc.jungler))


def writeWCtoCSV():
    with open("D:\PyCharmProjects\DataScienceProject\Comp_Data\winningComps.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for wc in list_of_winning_comps:
            writer.writerow([wc.topLaner, wc.jungler, wc.midLaner, wc.botLaner, wc.support, 'win'])
        csvFile.close()


def writeLCtoCSV():
    with open("D:\PyCharmProjects\DataScienceProject\Comp_Data\losingComps.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for lc in list_of_losing_comps:
            writer.writerow([lc.topLaner, lc.jungler, lc.midLaner, lc.botLaner, lc.support, 'lose'])
        csvFile.close()


selected_role = 'Jungle'
selected_champion = 'Belveth'


def testingPandas():
    winningCompsData = pd.read_csv("D:\PyCharmProjects\DataScienceProject\Comp_Data\winningComps.csv")

    files = [file for file in os.listdir('./Comp_Data')]
    all_Comps = pd.DataFrame()

    for file in files:
        df = pd.read_csv("./Comp_Data/" + file)
        all_Comps = pd.concat([all_Comps, df])
    print(all_Comps.head)

    total_duplicate_games_champion = all_Comps.pivot_table(index=[selected_role], aggfunc='size')

   # winrate_of_champion = float

    #for each_champ in total_duplicate_games_champion:
   #     if each_champ is 'Belveth'

    print(total_duplicate_games_champion)


def initializeCompDir():
    if not os.path.exists("D:\PyCharmProjects\DataScienceProject\Comp_Data"):
        os.makedirs("D:\PyCharmProjects\DataScienceProject\Comp_Data")


try:
    #printListOfSummoners()
    #createRiotAPIUrl()
    #getChampionList()
    #initializeWinningCompFileHeader() #Here we're initializing the header's for the different CSV Files
    #initializeLosingCompFileHeader()
    #writeWCtoCSV() #and Here we're actually writing the data for the CSV files
    #writeLCtoCSV()
    printWinningCompJunglers()
    initializeCompDir()
    testingPandas()
except HTTPError as err:
    if err.code == 429:
        time.sleep(120)
        print("Requesting too much")
        pass
    else:
        print(err.code)
        pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
