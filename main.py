# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from riotwatcher import RiotWatcher, LolWatcher, ApiError #Importing Riotwatcher & other (Riot API)

lolWatcher_api_key = LolWatcher('RGAPI-704ce981-8404-4b57-bf27-21e702fed59b')
region = 'na1'


me = lolWatcher_api_key.summoner.by_name(region, 'Sobileo')

print(me)









# See PyCharm help at https://www.jetbrains.com/help/pycharm/
