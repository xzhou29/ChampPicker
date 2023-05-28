# from flask import current_app
import requests
import pandas as pd
import utils
import database
import sys
from tqdm import tqdm

# Now you can access the API_KEY
# api_key = current_app.API_KEY
# replace this by your own API key
api_key = 'RGAPI-f3a7c190-dd67-4bf3-9703-50f698b4cfb4'
# Set the base URL for the Riot API
BASE_URL = 'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/'
tiers = ['CHALLENGER', 'GRANDMASTER', 'MASTER']
# tiers = ['DIAMOND']
# database.drop_table('match_history')
database.initialization()
# sys.exit(0)
# fetch data from RIOT API and save into our database
collected_match_ids = set()
for tier in tiers:
    # 1 - Fetch a list of summoners from the League API with the desired rank or higher.
    data = utils.get_all_summoner_ids(tier)
    if tier in ['CHALLENGER', 'GRANDMASTER', 'MASTER']:
        entries = data['entries']
    else:
        entries = data
    # (['summonerId', 'summonerName', 'leaguePoints', 'rank', 'wins', 'losses'])
    # Convert the list of dictionaries to a list of tuples
    summoners_tuples = [(
        d['summonerId'], d['summonerName'], tier, d['rank'], d['wins'], d['losses']
    ) for d in entries]
    database.insert_update_summoner_info(summoners_tuples)
    # print(summoners_tuples[0])
    # 2 - Get the PUUIDs of these summoners using the Summoner API.
    summoner_ids = database.get_all_summoner_ids()
    print(f'summoner_ids: {len(summoner_ids)}')
    for i in tqdm(range(len(summoner_ids))):
        summoner_id = summoner_ids[i]
        #summoner_id = 'fwJlhPePOrjfgltmPkDCAUMfjs9d8bynvQzFJZXgy0f7eML1eJrQoT_LEg'
        puuid = utils.get_puuid_by_summoner_id(summoner_id)
        # 3 - Obtain the match history for each PUUID using the Match API.
        match_ids = utils.get_match_history_by_puuid(puuid, count=40)
        if not match_ids:
            continue
        for match_id in tqdm(match_ids):
            # avoid overlapped match
            if match_id not in collected_match_ids:
                collected_match_ids.add(match_id)
                # 4 - Filter the matches to include only solo ranked games.
                data_result = []
                match_detail = utils.get_match_details_by_match_id(match_id)
                if match_detail:
                    gameDuration = match_detail['info']['gameDuration']
                    gameVersion = match_detail['info']['gameVersion']
                    gameMode = match_detail['info']['gameMode']
                    gameType = match_detail['info']['gameType']
                    mapId = match_detail['info']['mapId']
                    # print("match_detail['info']['participants'] - ", match_detail['info']['participants'][0].keys())
                    for row in match_detail['info']['participants']:
                        summonerId = row['summonerId']
                        championId = row['championId']
                        win = row['win']
                        championName = row['championName']
                        champLevel = row['champLevel']
                        lane = row['lane']
                        teamId = row['teamId']
                        # timePlayed = row['timePlayed']
                        # unique key <match_id> + <summonerId>
                        date_row = tuple([match_id, summonerId, puuid, gameDuration, gameVersion, gameMode, gameType, mapId,
                             championId, win, championName, champLevel, lane, teamId])
                        data_result.append(date_row)
                    database.insert_update_match_history(data_result)
