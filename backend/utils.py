import sqlite3
import requests
import os


def extract_win_rate_any_champ(gameVersion):
    # champDataAny = [
    #     {
    #     'champName': 'Amumu',
    #     'laneName': 'JUNGLE',
    #     'iconImageLink': 'https://cdn.communitydragon.org/10.16.1/champion/Amumu/square',
    #     'winRate': '51.2'
    #     }
    # ]
    adc_list = ['Jinx', 'Ezreal', 'KogMaw', 'Jhin', 'Seraphine', 'Nilah', 'Xayah',
                    'Karthus', 'KaiSa', 'Twitch', 'Ziggs', 'Samira', 'Draven', 'Vayne',
                    'Swain', 'Tristana', 'Veigar', 'Ashe', 'Zeri', 'Sivir', 'Varus',
                    'MissFortune', 'Lucian', 'Caitlyn', 'Aphelios', 'Yasuo', 'Kalista']
    champDataAny = []
    column1 = 'gameVersion'
    conn = sqlite3.connect('data/riot_data.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM champ_win_rate_any WHERE {column1}='{gameVersion}'")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        # ('Talon', 27, 11, '13.8', 0.7105263157894737, 'JUNGLE')
        champName,  wins, losses, _, winRate, lane = row
        champName = ''.join(champName.split())
        playedGames = wins + losses
        if playedGames < 20:
            if playedGames < 10:
                continue
            if winRate > 0.5:
                winRate = 0.25
        if lane == 'BOTTOM' and champName not in adc_list:
            lane = 'SUPPORT'
        entry = {
            'champName': champName,
            'laneName': lane,
            'iconImageLink': f'./public/icons/{champName}.png',
            'winRate': round(winRate * 100, 1)
            }
        champDataAny.append(entry)
    return champDataAny
    # fname = f'data/icons/{champName}.png'
    # if not os.path.exists(fname):
    #     url = f'https://cdn.communitydragon.org/13.9.0/champion/{champName}/square'
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #             with open(fname, 'wb') as f:
    #                 f.write(response.content)
    #             print(f'saved as: {fname}')