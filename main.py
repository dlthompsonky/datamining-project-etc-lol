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


api_key = 'RGAPI-61a6526d-6b58-4d5f-9863-7ef3edcf0078'
lolWatcher_api_key = LolWatcher(api_key)
region = 'na1'   #Working with the north american region

list_of_summoners = [lolWatcher_api_key.summoner.by_name(region, 'Quantum Bebop'),
                     lolWatcher_api_key.summoner.by_name(region, 'Sobileo'),
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

#Legacy values that could be used later.
#selected_role = "Jungle"
#selected_champion = "Belveth"


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
            time.sleep(.8) #Cannot request all of the requests at the same time, so we have to slow down the number of requests by using time.sleep
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


def sortListOfChampions(list_selected): #I didn't want to use double for loop.
    print("Starting the sorting")
    idx = 0
    selected_list = []
    selected_list = list_selected

    while idx < len(selected_list):
        if idx == 0:
            idx += 1
            continue
        elif idx > 0:
            first_word = str(selected_list[idx])
            second_word = str(selected_list[idx - 1])
            #print("Here is the first word: " + first_word)
            #print("Here is the second word: " + second_word)
            if first_word[0] < second_word[0]:
                #print("First word is out of place.")
                temp = str(second_word)
                selected_list.remove(str(second_word))
                selected_list.append(temp)
                idx = 0
            elif first_word[0] == second_word[0]:
                if first_word[1] < second_word[1]:
                    #print("First word is out of place.")
                    temp = str(second_word)
                    selected_list.remove(str(second_word))
                    selected_list.append(temp)
                    idx = 0
                elif first_word[1] == second_word[1]:
                    if len(first_word) >= 3 and len(second_word) >= 3:
                        if first_word[2] < second_word[2]:
                            #print("First word is out of place.")
                            temp = str(second_word)
                            selected_list.remove(str(second_word))
                            selected_list.append(temp)
                            idx = 0
                        else:
                            idx += 1
                    elif len(first_word) < len(second_word):
                        #print("First word is shorter")
                        temp = str(second_word)
                        selected_list.remove(str(second_word))
                        selected_list.append(temp)
                        idx = 0
                    else:
                        idx += 1
                else:
                    idx += 1
            else:
                idx += 1
    return selected_list


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


def generateRow(sorted_list, selected_champion):
    #This method is to generate the row by seeing the header of the heatmap_data.csv file and deciding based on how the character's are sorted what should be placed where
    #This should later take into account the win / loss
    print("Starting to generate row data.")
    lines_read_in_csvFile = []
    row_of_selected_string = []

    #First we are grabbing the lines in the CSV to then manipulate and rewrite them
    with open("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", 'r', newline='') as csvFileForReading:
        lines_read_in_csvFile = csvFileForReading.readlines()
        csvFileForReading.close()

    #Then we are going to grab the row of the champion we selected
    for (idx, each_row_in_lines) in enumerate(lines_read_in_csvFile):
        if idx != 0:
            print("Here is each row in lines: " + each_row_in_lines.strip() + " | and here is what we're looking for: " + str(selected_champion))
            row_Idx_string = ""
            if "," in each_row_in_lines.strip():
                split_list = each_row_in_lines.strip().split(",")
                row_Idx_string = split_list[0]
            else:
                row_Idx_string = each_row_in_lines.strip()
            if row_Idx_string == selected_champion:
                row_of_selected_string.append(each_row_in_lines.strip())
                break

    print("Here is the row selected: " + str(row_of_selected_string))

    row_to_be_written_in_file = ""
    csvFile = pd.read_csv("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", engine='python')  # delimiter=',',  index_col=0, lineterminator="\r\n"

    for (csvIdx, each_column_of_csv) in enumerate(csvFile):
        #found_champion = False
        if csvIdx == 0:
            print("Length of the csvFile : " + str(len(csvFile)) + " | Here is the length of the other : " + str(len(row_of_selected_string)))
            while len(row_of_selected_string) < len(csvFile): #Trying to set the length of the row array to the same as the columns (since we're doing a square heatmap)
                row_of_selected_string.append("")
            print(" Here is the length of the other after : " + str(len(row_of_selected_string)))
            print("Here is the first column: " + each_column_of_csv)
            print("Here is the row of selected string after modification: " + str(row_of_selected_string).strip())
            #row_to_be_written_in_file += str(selected_champion)
        else:
            for each_champion in sorted_list:
                print("Here is the column: " + str(each_column_of_csv))
                if str(each_champion) == str(each_column_of_csv):
                    #print("Here is the each score of selected : " + str(each_score_of_selected_row))
                    if row_of_selected_string[csvIdx] == '':
                        row_of_selected_string[csvIdx] = '1|1'
                        #row_to_be_written_in_file = str(row_of_selected_string.strip())
                        break
                    elif '1' in row_of_selected_string[csvIdx]:
                        temp_win_loss = row_of_selected_string[csvIdx].split('|')
                        temp_wins = type(int(temp_win_loss[0]))
                        temp_total_games = type(int(temp_win_loss[1]))
                        temp_wins += 1
                        temp_total_games += 1
                        temp_score = str(temp_wins) + '|' + str(temp_total_games)
                        row_of_selected_string[csvIdx] = temp_score
                        #row_to_be_written_in_file = str(row_of_selected_string.strip())
                        print("Here is the win / losses: " + temp_score)
                        break
        #if csvIdx < (len(csvFile) - 1):
        #   row_to_be_written_in_file += ","
    for each_entry in row_of_selected_string:
        if each_entry == '':
            row_to_be_written_in_file += ","
        else:
            row_to_be_written_in_file += (each_entry + ",")
    #row_to_be_written_in_file = ''.join(row_of_selected_string)
    return row_to_be_written_in_file


def testingPandas():
    files = [file for file in os.listdir('./Comp_Data')]
    all_comps = pd.DataFrame()

    for file in files:
        df = pd.read_csv("./Comp_Data/" + file)
        all_comps = pd.concat([all_comps, df]).reset_index(drop=True)
    print(all_comps.head)

    wins = 0
    losses = 0

    csvData = pd.read_csv("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", delimiter=',', index_col=0)
    columns = list(csvData)

    #This can be used to produce a Dataframe with null values easily
    #heatmap_df = pd.DataFrame()
    #heatmap_df = pd.concat([heatmap_df, csvData])
    #print(heatmap_df.head)
    print("=================================================================================================================")

    for (idx1, each_column) in enumerate(all_comps):
        if (str(all_comps[each_column][0]) != "loss") or (str(all_comps[each_column][0]) != "win") or (str(all_comps[each_column][0]) != "win / loss"):
            for (idx2, each_row) in enumerate(all_comps[each_column]):
                if all_comps['win / loss'][idx2] == 'win':
                    wins += 1
                    for (columnsIdx, each_column_of_columns) in enumerate(columns):
                        if columnsIdx != 0:
                            if str(each_column_of_columns) == str(all_comps[each_column][idx2]):
                                row_to_be_sorted = []
                                row_to_be_written_in_file = ""

                                for (limiter_index, each_entry) in enumerate(all_comps):
                                    if str(all_comps[each_entry][idx2]) != "win" and str(all_comps[each_entry][idx2]) != str(all_comps[each_column][idx2]):
                                        if limiter_index < 4:
                                            row_to_be_sorted.append(str(all_comps[each_entry][idx2]))
                                        else:
                                            row_to_be_sorted.append(str(all_comps[each_entry][idx2]))
                                sorted_list = sortListOfChampions(row_to_be_sorted)

                                row_to_be_written_in_file = generateRow(sorted_list, all_comps[each_column][idx2])

                                lines_read_in_csvFile = []

                                with open("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", 'r+', newline='') as csvFileForReading:
                                    lines_read_in_csvFile = csvFileForReading.readlines()
                                    csvFileForReading.close()

                                for (lineIdx, each_row_of_linesCSV) in enumerate(lines_read_in_csvFile):
                                    if lineIdx != 0:
                                        #print("Here is the dataReader row: " + each_row_of_linesCSV.strip() + " | Here is what we're looking for: " + str(all_comps[each_column][idx2]))
                                        if each_row_of_linesCSV.strip() == all_comps[each_column][idx2]:
                                            lines_read_in_csvFile[lineIdx] = row_to_be_written_in_file + "\n" #(str(lines_read_in_csvFile[lineIdx]).strip() +
                                            print("This is the lines to be written in the csvFile: " + str(lines_read_in_csvFile[lineIdx]))
                                            print("This is the row to be written: " + row_to_be_written_in_file)
                                            break

                                #print(str(lines_read_in_csvFile).strip())
                                #lines_read_in_csvFile.append("\n")

                                with open("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", 'w+', newline='') as csvFileForReading:
                                    csvFileForReading.writelines(lines_read_in_csvFile)
                                    csvFileForReading.close()

                                print("This is the row to be written: " + str(row_to_be_written_in_file))
                elif all_comps['win / loss'][idx2] == 'loss':
                    losses += 1
                    #print("Looping and : " + str(all_comps['win / loss'][idx]))

    print("These are the wins: " + str(wins))
    print("These are the losses: " + str(losses))

    #winrate_on_selected_champion = (wins / (wins + losses)) * 100
    #print("The winrate of: " + str(selected_champion) + " " + str(winrate_on_selected_champion) + " %")


def initializeHeatMapCSV():
    if (not (exists("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv") == True)):
        with open("D:\PyCharmProjects\DataScienceProject\heatmap_data.csv", 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            total_header = []
            total_header.append(str("row_name"))
            for each_row in open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'r+'):
                stripped_row = each_row.strip()
                total_header.append(stripped_row)
                #print(str(stripped_row))
            writer.writerow(total_header)

            for each_champion in open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'r+'):
                total_single_champion_row = []
                stripped_champion_row = each_champion.strip()
                total_single_champion_row.append(stripped_champion_row)
                writer.writerow(total_single_champion_row)

            csvFile.close()


def initializeChampList():
    if (not (exists("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt") == True)):
        list_of_champions_file = open("D:\PyCharmProjects\DataScienceProject\listOfChampions.txt", 'r+')

        for each_row in list_of_champions_file:
            stripped_row = each_row.strip()
            list_of_heatmap_champs.append(stripped_row)

        list_of_champions_file.close()
    else:
        print("List of champions already exists | Try deleting it and restarting")


def initializeCompDir():
    if not os.path.exists("D:\PyCharmProjects\DataScienceProject\Comp_Data"):
        os.makedirs("D:\PyCharmProjects\DataScienceProject\Comp_Data")


try:
    #getListOfSummoners()
    #createRiotAPIUrl()
    #getChampionList()
    #sortListOfChampions(list_of_champions)
    #writeListOfChampionsToTXT() #Writing the list of champions that we got previously so the, "getChampionList" doesn't have to be used repeatedly
    #initializeFileHeaders()     #Here we're initializing the headers for the different team composition (CSV) files
    #writeTCtoCSV()              #Writing the Team compositions to CSV files.
    #initializeCompDir()
    initializeChampList()
    initializeHeatMapCSV()
    testingPandas()
except HTTPError as err:
    if err.code == 429:
        time.sleep(120)
        print("Requesting too much")
        pass
    else:
        print(err.code)
        pass

