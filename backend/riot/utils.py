import requests
import pandas as pd

API_KEY = 'RGAPI-f3a7c190-dd67-4bf3-9703-50f698b4cfb4'
# Set the base URL for the Riot API
BASE_URL = 'https://na1.api.riotgames.com/lol/'




# get a list of encrypted summonerIds
# challenger, grandmaster, master
# Get the PUUID of a summoner
def get_summoner_id_by_summoner_name(summoner_name):
    url = f"{BASE_URL}summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data['id']
    else:
        return None


# Get the PUUID of a summoner
def get_summoner_puuid_by_summoner_name(summoner_name):
    url = f"{BASE_URL}summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data['puuid']
    else:
        return None


# Get the match history of a player using their PUUID
def get_match_history_by_puuid(puuid, count=20):
    match_base_url = 'https://americas.api.riotgames.com/lol/'
    url = f"{match_base_url}match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Function to get match details by match ID
def get_match_details_by_match_id(match_id):
    match_base_url = 'https://americas.api.riotgames.com/lol/'
    url = f"{match_base_url}match/v5/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        match_data = response.json()
        return match_data
    else:
        return None


# Function to get PUUID by Summoner ID
def get_puuid_by_summoner_id(summoner_id):
    url = f"{BASE_URL}summoner/v4/summoners/{summoner_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data['puuid']
    else:
        return None


def get_all_summoner_ids(tier, queue='RANKED_SOLO_5x5'):
    tier = tier.lower()
    if tier in ['master', 'challenger', 'grandmaster']:
        url = f'{BASE_URL}league/v4/{tier}leagues/by-queue/{queue}?api_key={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            # dict_keys(['tier', 'leagueId', 'queue', 'name', 'entries'])
            return response.json()
        else:
            return None

    # {"leagueId":"0b4e9073-f875-45a2-a6ab-9e45b5ac6ead","queueType":"RANKED_SOLO_5x5","tier":"DIAMOND","rank":"II","summonerId":"R-deQofH4ILQZxMwNbDUK6po94vjiKGzBWm9CnBnl_xMrCq0","summonerName":"Da Rizzler","leaguePoints":0,"wins":142,"losses":151,"veteran":false,"inactive":false,"freshBlood":false,"hotStreak":false}
    elif tier == 'diamond':
        data = []  # Initialize an empty list to store the response data tuples
        divisions = ['I', 'II']
        page_num = 1  # Set the initial page number
        for division in divisions:
            while True:
                # league/v4/entries/RANKED_SOLO_5x5/DIAMOND/II?page=1&api_key=
                url = f'{BASE_URL}league/v4/entries/RANKED_SOLO_5x5/DIAMOND/{division}?page={page_num}&api_key={API_KEY}'
                response = requests.get(url)
                if response.status_code == 200:
                    response_data = response.json()
                    if len(response_data) == 0:
                        break  # Exit the loop if there is no more data to retrieve
                    data.extend(response_data)  # Append the response data tuples to the list
                    page_num += 1  # Increment the page number for the next request
                else:
                    print(f"Error: {response.status_code}")
                    break  # Exit the loop if there is an error
        return data
    else:
        return None



