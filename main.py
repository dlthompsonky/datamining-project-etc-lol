# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from riotwatcher import RiotWatcher, LolWatcher, ApiError #Importing Riotwatcher & other (Riot API)
import json

lolWatcher_api_key = LolWatcher('RGAPI-704ce981-8404-4b57-bf27-21e702fed59b')
region = 'na1'


list_of_summoners = [lolWatcher_api_key.summoner.by_name(region, 'Sobileo'),
                     lolWatcher_api_key.summoner.by_name(region, 'Quantum Bebop'),
                     lolWatcher_api_key.summoner.by_name(region, 'No Gank Incoming'),
                     lolWatcher_api_key.summoner.by_name(region, 'FM Fallen'),
                     lolWatcher_api_key.summoner.by_name(region, 'Airpiane'),
                     lolWatcher_api_key.summoner.by_name(region, 'Ominous Cow')]

list_of_account_IDS = []


def printListOfSummoners(): #Prints list of the summoner objects (This includes a lot of information)
    for x_summoner in list_of_summoners:
        print(x_summoner)
    for x_summoner_id in list_of_summoners:
        print(x_summoner_id['accountId']) #This is to collect the accountId of each account


printListOfSummoners()









# See PyCharm help at https://www.jetbrains.com/help/pycharm/
