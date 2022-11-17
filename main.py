# HELLO!
# Make sure to read, "README.md", for instructions on how to use.
#
# Importing Riotwatcher (to better use Riot's API system & gather names / matches easily).
from riotwatcher import RiotWatcher, LolWatcher, ApiError
# File management and other:
import csv
import os
from os.path import exists
import json
import urllib.request
from urllib.error import HTTPError
import time
from dotenv import load_dotenv
# Below are the Data-Plotting modules:
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
from enum import Enum

load_dotenv()


class WinningComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''


class LosingComp:
    topLaner = ''
    jungler = ''
    midLaner = ''
    botLaner = ''
    support = ''


# Manipulate API KEY - Needs to be refreshed every 24 hours
api_key = os.getenv("API_KEY")
region = 'na1'

if api_key and api_key != '':
    print("Success getting API_KEY")
    lolWatcher_api_key = LolWatcher(api_key)
else:
    print("Error getting API_KEY")
    exit()

list_of_names_to_manipulate = ['PwVx Hc9999na', 'c2 meteos', 'Wakanda f0rever', 'MU APA', 'SiddyWiddy123',
                               'Twitchtv Cupic', 'winnie poohbear', 'Topo', 'Fishlord', 'zeyzal7',
                               'Wx Mjm978244659', 'winstxn', 'ctrI c', 'Davemon', 'VEGETOOOOOOOOOOO',
                               'duoking1', 'Pentaless', 'dog kachu', 'TTV KoKooPuffs', 'Nikkone',
                               '100 Tenacity', 'Rebopah', 'known win trader', 'FORA999', '100 Sword']

list_of_summoners = []
for each_name in list_of_names_to_manipulate:
    list_of_summoners.append(lolWatcher_api_key.summoner.by_name(region, str(each_name)))

plt.style.use("seaborn")
field_names_for_heatmap = []
field_names_for_team_comps = ['Top', 'Jungle', 'Mid', 'Bot', 'Support', 'win / loss']

# Lists being used below
list_of_puuids = []
list_of_matches = []
list_of_matches_from_file = []
url_list = []
list_of_champions = []
list_of_winning_comps = []
list_of_losing_comps = []
list_of_heatmap_champs = [[]]

def initializeFileHeaders():
    print("Initializing file headers.")
    initializeWinningCompFileHeader()
    initializeLosingCompFileHeader()


def initializeWinningCompFileHeader():
    if not exists("winningComps.csv") is True:
        csvFile = open("Comp_Data/winningComps.csv", 'w', newline='')
        writer = csv.writer(csvFile)
        writer.writerow(field_names_for_team_comps)
        print("Initializing Winning Comp File & Header")
        csvFile.close()


def initializeLosingCompFileHeader():
    if not exists("losingComps.csv") is True:
        csvFile = open("Comp_Data/losingComps.csv", 'w', newline='')
        writer = csv.writer(csvFile)
        writer.writerow(field_names_for_team_comps)
        print("Initializing Losing Comp File & Header")
        csvFile.close()


def areThereMatchDuplicates():
    matchesSourcedFile = open("matchesSourcedFile.txt", 'r')
    list_of_matches_from_file = matchesSourcedFile.readlines()
    matchesSourcedFile.close()

    if set(list_of_matches).isdisjoint(set(list_of_matches_from_file)) and not (len(list_of_matches_from_file) > 0):  # If they do not have duplicates and they are not empty
        return False
    else:
        return True


def checkForTextFile():  # This is going to check for a text file before we start to manipulate data to put into it.
    matchesSourcedFile = open("matchesSourcedFile.txt", 'a+')
    if areThereMatchDuplicates():
        print("There are duplicates")
        return
    else:
        print("There are no duplicates")
        for x_match in list_of_matches:
            matchesSourcedFile.write(str(x_match) + '\n')
    matchesSourcedFile.close()


# Prints list of the summoner objects (This includes a lot of information)
def getListOfSummoners():
    for x_puuid_id in list_of_summoners:
        list_of_puuids.append(x_puuid_id['puuid'])
    for x_puuid in list_of_puuids:
        for x_matches in range(0, 19):
            list_of_matches.append(lolWatcher_api_key.match.matchlist_by_puuid(region, x_puuid)[x_matches])
            time.sleep(.25)  # Trying to slow down requests
    print("This is how many matches have been sourced : " + str(len(list_of_matches)))
    checkForTextFile()


def createRiotAPIUrl():
    print("Creating URLs to be mined.")
    for x_match in list_of_matches:
        url_list.append('https://americas.api.riotgames.com/lol/match/v5/matches/' + str(x_match) + '?api_key=' + str(api_key))


def getChampionList():
    try:
        print("Starting to get champion list.")
        for x_url in url_list:
            # print("Looping")
            with urllib.request.urlopen(x_url) as url:
                data = json.loads(url.read().decode())
                wc = WinningComp()
                lc = LosingComp()
                pleaseContinue = False
                for checkerI in range(0, 5):
                    if data['info']['participants'][checkerI]['championName'] == "":
                        pleaseContinue = True
                        break
                if pleaseContinue:
                    continue
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
                    if list_of_champions.count(data['info']['participants'][i]['championName']) > 0 and len(list_of_champions) > 0:  # Checking for duplicates in the list of champions
                        continue
                    else:
                        list_of_champions.append(data['info']['participants'][i]['championName'])
                    time.sleep(1)
                list_of_winning_comps.append(wc)
                list_of_losing_comps.append(lc)
    except HTTPError as err:
        print(err)  # There is better error handling than this. Just using pass as placement for big issues right now.
        pass


def sortListOfChampions(list_selected):
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
            if first_word[0] < second_word[0]:
                temp = str(second_word)
                selected_list.remove(str(second_word))
                selected_list.append(temp)
                idx = 0
            elif first_word[0] == second_word[0]:
                if first_word[1] < second_word[1]:
                    temp = str(second_word)
                    selected_list.remove(str(second_word))
                    selected_list.append(temp)
                    idx = 0
                elif first_word[1] == second_word[1]:
                    if len(first_word) >= 3 and len(second_word) >= 3:
                        if first_word[2] < second_word[2]:
                            temp = str(second_word)
                            selected_list.remove(str(second_word))
                            selected_list.append(temp)
                            idx = 0
                        else:
                            idx += 1
                    elif len(first_word) < len(second_word):
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
    print("Writing champion list to TXT file")
    if not (exists("listOfChampions.txt") is True):
        champion_list_file = open("listOfChampions.txt", 'a+')
        for each_champion in list_of_champions:
            champion_list_file.write(str(each_champion))
            champion_list_file.write('\n')
        champion_list_file.close()


def writeTCtoCSV():
    print("Writing TC to CSV")
    writeWCtoCSV()
    writeLCtoCSV()


def writeWCtoCSV():
    with open("Comp_Data/winningComps.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for wc in list_of_winning_comps:
            writer.writerow([wc.topLaner, wc.jungler, wc.midLaner, wc.botLaner, wc.support, 'win'])
        csvFile.close()


def writeLCtoCSV():
    with open("Comp_Data/losingComps.csv", 'a+', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for lc in list_of_losing_comps:
            writer.writerow([lc.topLaner, lc.jungler, lc.midLaner, lc.botLaner, lc.support, 'loss'])
        csvFile.close()


class WinOrLoss(Enum):
    WIN = 0
    LOSS = 1


def generateRow(sorted_list, selected_champion, win_or_loss):
    row_of_selected_string = []

    if not isinstance(win_or_loss, WinOrLoss):
        raise TypeError("Win or loss must be an instance of the Enum class")

    csvFileForReading = open("heatmap_data.csv", 'r', newline='')
    lines_read_in_csvFile = csvFileForReading.readlines()
    csvFileForReading.close()

    for (idx, each_row_in_lines) in enumerate(lines_read_in_csvFile):
        row_Idx_string = ""

        if "," in each_row_in_lines:
            split_list = each_row_in_lines.split(",")
            row_Idx_string = split_list[0]
            if str(row_Idx_string) == str(selected_champion):
                row_of_selected_string = split_list
                break
        else:
            row_Idx_string = str(each_row_in_lines).strip()
            if str(row_Idx_string) == str(selected_champion):
                print("Found a match!")
                row_of_selected_string.append(row_Idx_string)
                break

    csvFile = pd.read_csv("heatmap_data.csv", engine='python')

    for (csvIdx, each_column_of_csv) in enumerate(csvFile):
        if csvIdx == 0:
            split_list_of_csvFile = csvFile[each_column_of_csv]

            while len(row_of_selected_string) < len(split_list_of_csvFile) + 1:
                row_of_selected_string.append("")
        else:
            for each_champion in sorted_list:
                if str(each_champion) == str(each_column_of_csv):
                    if row_of_selected_string[csvIdx] == '':
                        if win_or_loss == WinOrLoss.WIN:
                            row_of_selected_string[csvIdx] = '1|1'
                        else:
                            row_of_selected_string[csvIdx] = '0|1'
                        break
                    elif '|' in row_of_selected_string[csvIdx]:
                        temp_win_loss = row_of_selected_string[csvIdx].split('|')
                        temp_wins = int(temp_win_loss[0])
                        temp_total_games = int(temp_win_loss[1])
                        if win_or_loss == WinOrLoss.WIN:
                            temp_wins += 1
                        temp_total_games += 1
                        temp_score = str(temp_wins) + '|' + str(temp_total_games)
                        row_of_selected_string[csvIdx] = temp_score
                        break
    row_to_be_written_in_file = ",".join(row_of_selected_string)

    return row_to_be_written_in_file


def constructHeatmapData():
    files = [file for file in os.listdir('./Comp_Data')]
    all_comps = pd.DataFrame()
    for file in files:
        df = pd.read_csv("./Comp_Data/" + file)
        all_comps = pd.concat([all_comps, df]).reset_index(drop=True)

    print("Constructing heatmap data.")
    print(all_comps.head())

    wins = 0
    losses = 0

    csvData = pd.read_csv("heatmap_data.csv", delimiter=',', index_col=0)
    columns = list(csvData)
    print("===========================================================================================================")

    for (idx1, each_column) in enumerate(all_comps[:-1]):
        # if (str(all_comps[each_column]) != "loss") or (str(all_comps[each_column]) != "win") or (str(all_comps[each_column]) != "win / loss"):
        for (idx2, each_row) in enumerate(all_comps[each_column]):
            if all_comps['win / loss'][idx2] == 'win':
                compareAndConstruct(columns, all_comps, each_column, idx2, WinOrLoss.WIN)
            elif all_comps['win / loss'][idx2] == 'loss':
                compareAndConstruct(columns, all_comps, each_column, idx2, WinOrLoss.LOSS)

    changeFracToDecimals()


def compareAndConstruct(columns, all_comps, each_column, idx2, win_or_loss):
    for (columnsIdx, each_column_of_columns) in enumerate(columns):
        if str(each_column_of_columns) == str(all_comps[each_column][idx2]):
            row_to_be_sorted = []
            for (limiter_index, each_entry) in enumerate(all_comps):
                if str(all_comps[each_entry][idx2]) != "win" and str(all_comps[each_entry][idx2]) != str(
                        all_comps[each_column][idx2]):
                    if limiter_index < 4:
                        row_to_be_sorted.append(str(all_comps[each_entry][idx2]))
                    else:
                        row_to_be_sorted.append(str(all_comps[each_entry][idx2]))

            sorted_list = sortListOfChampions(row_to_be_sorted)
            row_to_be_written_in_file = generateRow(sorted_list, all_comps[each_column][idx2], win_or_loss)
            lines_read_in_csvFile = []

            with open("heatmap_data.csv", 'r+', newline='') as csvFileForReading:
                lines_read_in_csvFile = csvFileForReading.readlines()
                csvFileForReading.close()

            for (lineIdx, each_row_of_linesCSV) in enumerate(lines_read_in_csvFile):
                split_list_of_lines = each_row_of_linesCSV.strip().split(",")
                checker_champion = split_list_of_lines[0]
                if checker_champion == all_comps[each_column][idx2]:
                    lines_read_in_csvFile[lineIdx] = row_to_be_written_in_file + "\n"
                    break

            with open("heatmap_data.csv", 'w+', newline='') as csvFileForWriting:
                csvFileForWriting.writelines(lines_read_in_csvFile)
                csvFileForWriting.close()


def constructHeatMap():
    print("Constructing heatmap now.")
    total_column_labels = []
    for each_row in open("listOfChampions.txt", 'r+'):
        stripped_row = each_row.strip()
        total_column_labels.append(stripped_row)

    heatmap_df = pd.read_csv("heatmap_data.csv", delimiter=',', index_col=0)
    # Stylizing the Heatmap
    plt.figure(figsize=(11, 11))
    heatmap_df.index.names = ["Champions"]
    sns.color_palette("magma", as_cmap=True)
    sns.set(font_scale=.55, style="ticks", rc={'axes.facecolor': 'cornflowerblue', 'figure.facecolor': 'cornflowerblue'})
    heatmap = sns.heatmap(heatmap_df, cbar=True, vmax=1, vmin=0, annot=False, linewidths=.025, linecolor='black', xticklabels=total_column_labels, yticklabels=total_column_labels)
    heatmap.set_title("Champion Win-rate Correspondence")
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=75)
    heatmap.tick_params('both', length=10, width=1.5, which='both')

    plt.tight_layout()
    plt.show()


def changeFracToDecimals():
    lines_read_in_csvFile = []

    with open("heatmap_data.csv", 'r', newline='') as csvFileForReading:
        lines_read_in_csvFile = csvFileForReading.readlines()
        csvFileForReading.close()

    for (tempIdx, each_row) in enumerate(lines_read_in_csvFile):
        list_of_row = each_row.split(",")
        for (tempIdx2, each_entry) in enumerate(list_of_row):
            if "|" in each_entry:
                list_of_fraction_numbers = each_entry.split("|")
                wins = list_of_fraction_numbers[0]
                total_games = list_of_fraction_numbers[1]
                percentage_of_winning = (float(wins) / float(total_games))
                list_of_row[tempIdx2] = round(percentage_of_winning, 3)
        lines_read_in_csvFile[tempIdx] = (",".join(list(map(str, list_of_row))).strip() + "\n")

    with open("heatmap_data.csv", 'w+', newline='') as csvFileForWriting:
        csvFileForWriting.writelines(lines_read_in_csvFile)
        csvFileForWriting.close()


def initializeHeatMapCSV():
    print("Initializing heatmap CSV.")
    if not exists("heatmap_data.csv") is True:
        with open("heatmap_data.csv", 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            total_header = []
            total_header.append(str("row_name"))
            for each_row in open("listOfChampions.txt", 'r+'):
                stripped_row = each_row.strip()
                total_header.append(stripped_row)
            writer.writerow(total_header)
        csvFile.close()

    csvFileChecker = open("heatmap_data.csv", 'r+')
    checker_list = csvFileChecker.readlines()

    if len(checker_list) <= 2:
        csvListOfChamps = open("listOfChampions.txt", 'r+')
        csvHeatMapFile = open("heatmap_data.csv", 'a+', newline='')
        writer = csv.writer(csvHeatMapFile)
        for each_champion in csvListOfChamps:
            total_single_champion_row = []
            stripped_champion_row = each_champion.strip()
            total_single_champion_row.append(stripped_champion_row)
            writer.writerow(total_single_champion_row)
        csvListOfChamps.close()


def initializeHeatMapListFromChampList():
    print("Initializing Heatmap List")
    if exists("listOfChampions.txt"):
        list_of_champions_file = open("listOfChampions.txt", 'r+')
        list_of_champions_file_list = list_of_champions_file.readlines()

        for each_row in list_of_champions_file_list:
            stripped_row = each_row.strip()
            list_of_heatmap_champs.append(stripped_row)

        list_of_champions_file.close()
    else:
        print("List of champions doesn't exist")


def initializeCompDir():
    if not os.path.exists("Comp_Data"):
        os.makedirs("Comp_Data")


# Manipulate Methods (Make sure to read the README.txt)
try:
    initializeCompDir()                        # Initializes Comp_Data Folder
    getListOfSummoners()                       # Getting Summoner's names and their puu_id
    createRiotAPIUrl()                         # Getting Riot Url (to better access their APIs)
    getChampionList()                          # Getting List of Champions from games selected
    sortListOfChampions(list_of_champions)     # Sorting the list
    writeListOfChampionsToTXT()                # Writing "getChampionList" so it doesn't have to be used repeatedly
    initializeFileHeaders()                    # Initializing the headers for the different team composition (CSV) files
    writeTCtoCSV()                             # Writing the Team compositions to CSV files.
    initializeHeatMapListFromChampList()
    initializeHeatMapCSV()                     # Initializing Heatmap CSV (Prepping the formatting columns/ header)
    constructHeatmapData()                     # Forming all heatmap data from the previously taken Api data
    constructHeatMap()                         # Using the CSV (with pandas / sns / matplot) to create Heatmap
except HTTPError as err:
    if err.code == 429:
        print("Requesting too much")
        exit()
