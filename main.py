# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from riotwatcher import RiotWatcher, LolWatcher, ApiError #Importing Riotwatcher & other (Riot API)
from os.path import exists
import json
import urllib.request
from urllib.error import HTTPError
import time

#Need to make sure to put this all within try function in order to keep errors minimmal


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


api_key = 'RGAPI-07230a07-25cc-4bec-b1a9-738de3de27c6'
lolWatcher_api_key = LolWatcher(api_key)
region = 'na1'   #Working with the north american region


list_of_summoners = [lolWatcher_api_key.summoner.by_name(region, 'Sobileo'),
                     lolWatcher_api_key.summoner.by_name(region, 'Quantum Bebop'),
                     lolWatcher_api_key.summoner.by_name(region, 'No Gank Incoming'),
                     lolWatcher_api_key.summoner.by_name(region, 'FM Fallen'),
                     lolWatcher_api_key.summoner.by_name(region, 'Airpiane'),
                     lolWatcher_api_key.summoner.by_name(region, 'Ominous Cow')]

list_of_puuids = []
list_of_matches = []
list_of_matches_from_file = []


def areThereMatchDuplicates():
    dataFile = open("D:\PyCharmProjects\DataScienceProject\dataFile.txt", 'r')
    list_of_matches_from_file = dataFile.readlines()
    dataFile.close()

    if(set(list_of_matches).isdisjoint(set(list_of_matches_from_file)) and not (len(list_of_matches_from_file) > 0)): #If they do not have duplicates and they are not empty
        return False
    else:
        return True


def checkForTextFile():#This is going to check for a text file before we start to manipulate data to put into it.
    dataFile = open("D:\PyCharmProjects\DataScienceProject\dataFile.txt", 'a+')
    if(areThereMatchDuplicates()):
        print("There are duplicates")
        return
    else:
        print("There are no duplicates")
        for x_match in list_of_matches:
            dataFile.write(str(x_match))
            dataFile.write('\n')
            #print(str(x_match))
    dataFile.close()


def printListOfSummoners(): #Prints list of the summoner objects (This includes a lot of information)
    for x_puuid_id in list_of_summoners:
        list_of_puuids.append(x_puuid_id['puuid']) #This is to collect the accountId of each account
    for x_puuid in list_of_puuids:
        #print(lolWatcher_api_key.match.matchlist_by_puuid(region, x_puuid))
        for x_matches in range(0, 19): #If you don't put the range and 0, 19 in parenthesis, it will not loop through them all it will only go through the selected numbers
            list_of_matches.append(lolWatcher_api_key.match.matchlist_by_puuid(region, x_puuid)[x_matches])
    print("This is how many matches have been sourced : " + str(len(list_of_matches)))
    checkForTextFile()


url_list = []

def createRiotAPIUrl():
    for x_match in list_of_matches:
        url_list.append('https://americas.api.riotgames.com/lol/match/v5/matches/' + str(x_match) + '?api_key=' + str(api_key))


list_of_all_champions = []
list_of_winning_comps = []
list_of_losing_comps = []
def getChampionList():
    try:
        for x_url in url_list:
            #print("Looping")
            time.sleep(1) #Cannot request all of the requests at the same time, so we have to slow down the number of requests by using time.sleep
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


try:
    printListOfSummoners()
    time.sleep(2.5)
    createRiotAPIUrl()
    time.sleep(2.5)
    getChampionList()
    printWinningCompJunglers()
except HTTPError as err:
    if err.code == 429:
        time.sleep(120)
        print("Requesting too much")
        pass
    else:
        print(err.code)
        pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
