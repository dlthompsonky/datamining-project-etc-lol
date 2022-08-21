# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from riotwatcher import RiotWatcher, LolWatcher, ApiError #Importing Riotwatcher & other (Riot API)
from os.path import exists
import json

#Need to make sure to put this all within try function in order to keep errors minimmal

lolWatcher_api_key = LolWatcher('RGAPI-704ce981-8404-4b57-bf27-21e702fed59b')
region = 'na1' #Working with the north american region


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


#checkForTextFile()
printListOfSummoners()









# See PyCharm help at https://www.jetbrains.com/help/pycharm/
