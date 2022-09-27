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

field_names_for_heatmap = []
field_names_for_team_comps = ['Top', 'Jungle', 'Mid', 'Bot', 'Support', 'win / loss']

class WinningComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''
    #dataToBeWritten = [[topLaner], [jungler], [midLaner], [botLaner], [support]]


class LosingComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''
    #dataToBeWritten = [[topLaner], [jungler], [midLaner], [botLaner], [support]]


api_key = 'RGAPI-b17554b7-d868-4d16-bbcf-c8aa134cc6d7'
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
list_of_champions = []
list_of_winning_comps = []
list_of_losing_comps = []
list_of_heatmap_champs = [[]]  #2D Array Syntax


def initializeFileHeaders():
    initializeWinningCompFileHeader()
    initializeLosingCompFileHeader()


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
            print("Initializing Losing Comp File & Header")
            csvFile.close()


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


def getListOfSummoners(): #Prints list of the summoner objects (This includes a lot of information)
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
                    if list_of_champions.count(data['info']['participants'][i]['championName']) > 0 and len(list_of_champions) > 0: #Checking for duplicates in the list of champions
                        print("The champion : " + str(data['info']['participants'][i]['championName']) + " is already in the list")
                    else:
                        list_of_champions.append(data['info']['participants'][i]['championName'])
                list_of_winning_comps.append(wc)
                list_of_losing_comps.append(lc)
    except HTTPError as err:
        print(err) #There is better error handling than this. Just using pass as placement for big issues right now.
        pass


def writeListOfChampionsToTXT():
    champion_list_file = open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'a+')
    for each_champion in list_of_champions:
        champion_list_file.write(str(each_champion))
        champion_list_file.write('\n')
    champion_list_file.close()


def writeTCtoCSV():
    writeWCtoCSV()
    writeLCtoCSV()


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
            writer.writerow([lc.topLaner, lc.jungler, lc.midLaner, lc.botLaner, lc.support, 'loss'])
        csvFile.close()


selected_role = "Jungle"
selected_champion = "Belveth"


def testingPandas():
    files = [file for file in os.listdir('./Comp_Data')]
    all_comps = pd.DataFrame()

    for file in files:
        df = pd.read_csv("./Comp_Data/" + file)
        all_comps = pd.concat([all_comps, df]).reset_index(drop=True)
    print(all_comps.head)

    wins = 0
    losses = 0
    csvData = pd.read_csv("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv")
    columns = list(csvData)

    for (idx1, each_column) in enumerate(all_comps):
        if str(all_comps[each_column]) != "win / loss":
            for (idx2, each_row) in enumerate(all_comps[each_column]):
                if all_comps['win / loss'][idx2] == 'win':
                    wins += 1
                    for each_column_of_columns in columns:
                        row_to_be_written = ""
                        print("Here is the column : " + str(each_column_of_columns) + " | Here is the champion: " + str(all_comps[each_column][idx2]))
                        if str(each_column_of_columns) == str(all_comps[each_column][idx2]):
                            print("Found a match")
                            for (limiter_index, each_entry) in enumerate(all_comps):
                                if str(all_comps[each_entry][idx2]) != "win":
                                    if (limiter_index < 5):
                                        row_to_be_written += str(all_comps[each_entry][idx2]) + ","
                                    else:
                                        row_to_be_written += str(all_comps[each_entry][idx2])
                                    print("This is the entry for " + str(idx2) + ": " + str(all_comps[each_entry][idx2]))
                            print("This is the row to be written: " + str(row_to_be_written))
                elif all_comps['win / loss'][idx2] == 'loss':
                    losses += 1
                    #print("Looping and : " + str(all_comps['win / loss'][idx]))

    print("These are the wins: " + str(wins))
    print("These are the losses: " + str(losses))

    winrate_on_selected_champion = (wins / (wins + losses)) * 100
    print("The winrate of: " + str(selected_champion) + " " + str(winrate_on_selected_champion) + " %")


def initializeHeatMapCSV():
    if (not (exists("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv") == True)):
        with open("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            total_header = []
            for each_row in open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'r+'):
                stripped_row = each_row.strip()
                total_header.append(str(stripped_row))
                #print(str(stripped_row))
            total_header.append("winrate")
            total_header.append("number of games")
            writer.writerow(total_header)
            csvFile.close()

def heatmapAttempt():
    heatmapDataFrame = pd.DataFrame()


def initializeChampList():
    list_of_champions_file = open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'r+')

    for each_row in list_of_champions_file:
        stripped_row = each_row.strip()
        list_of_heatmap_champs.append(stripped_row)

    list_of_champions_file.close()


def initializeCompDir():
    if not os.path.exists("D:\PyCharmProjects\DataScienceProject\Comp_Data"):
        os.makedirs("D:\PyCharmProjects\DataScienceProject\Comp_Data")


try:
    #getListOfSummoners()
    #createRiotAPIUrl()
    #getChampionList()
    #writeListOfChampionsToTXT() #Writing the list of champions that we got previously so the, "getChampionList" doesn't have to be used repeatedly
    #initializeFileHeaders()     #Here we're initializing the headers for the different team composition (CSV) files
    #writeTCtoCSV()              #Writing the Team compositions to CSV files.
    initializeCompDir()
    #initializeChampList()
    testingPandas()
    #initializeHeatMapCSV()
except HTTPError as err:
    if err.code == 429:
        time.sleep(120)
        print("Requesting too much")
        pass
    else:
        print(err.code)
        pass

