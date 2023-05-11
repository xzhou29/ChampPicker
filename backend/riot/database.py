import sqlite3
from collections import defaultdict


def initialization():
    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Create the 'summoner_info' table
    c.execute('''
    CREATE TABLE IF NOT EXISTS summoner_info (
        summonerId TEXT PRIMARY KEY,
        summonerName TEXT,
        tier TEXT,
        division TEXT,
        wins INTEGER,
        losses INTEGER
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS match_history (
        match_id TEXT,
        summonerId TEXT,
        puuid TEXT,
        gameDuration INTEGER,
        gameVersion TEXT,
        gameMode TEXT,
        gameType TEXT,
        mapId INTEGER,
        championId INTEGER,
        win INTEGER,
        championName TEXT,
        champLevel INTEGER,
        lane TEXT,
        teamId INTEGER,
        PRIMARY KEY (match_id, championName)
    )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# insert or update
# save all data from selected tier about:
# d['summonerId'], d['summonerName'], tier, d['rank'], d['wins'], d['losses']
def insert_update_summoner_info(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Insert or update the list of summoners in the 'summoner_info' table
    c.executemany('''
    INSERT OR REPLACE INTO summoner_info (summonerId, summonerName, tier, division, wins, losses)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# insert or update
def insert_update_match_history(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Insert the list of tuples into the 'match_history' table
    c.executemany('''
    INSERT OR REPLACE INTO match_history (
        match_id, summonerId, puuid, gameDuration, gameVersion, gameMode, gameType,
        mapId, championId, win, championName, champLevel, lane, teamId
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# get a list of summoner IDs
def get_all_summoner_ids() -> list:
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Fetch all the summonerId values from the 'summoner_info' table
    c.execute('SELECT summonerId, summonerName FROM summoner_info')
    summoner_ids = c.fetchall()
    # Close the connection
    conn.close()
    # Convert the list of tuples to a list of summonerId values
    summoner_ids_list = [item[0] for item in summoner_ids]
    # summoner_ids_list = [item[0] for item in summoner_ids]
    return summoner_ids_list


def get_all_matches():
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Fetch all rows from the 'match_history' table
    c.execute("""
    SELECT * FROM match_history
    WHERE gameMode=='CLASSIC'""")
    rows = c.fetchall()
    conn.close()
    # Close the connection
    # Group the rows by match_id and store overlapping items in a list
    matches = defaultdict(list)
    for row in rows:
        match_id = row[0]
        matches[match_id].append(row)
    # Convert the defaultdict to a regular dict
    matches = dict(matches)
    # Print the grouped matches
    return matches


def drop_table(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Execute the SQL command to delete the 'match_history' table
    c.execute(f'DROP TABLE IF EXISTS {table_name}')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def create_table_champ_win_rate_any():
    conn = sqlite3.connect('data/riot_data.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS champ_win_rate_any (
        champ TEXT,
        wins INTEGER,
        losses INTEGER,
        gameVersion TEXT,
        winRate REAL,
        lane TEXT,
        PRIMARY KEY (gameVersion, champ, lane)
    )
    ''')
    conn.commit()
    conn.close()


# insert or update
def insert_update_champ_win_rate_any(data):
    conn = sqlite3.connect('data/riot_data.db')
    c = conn.cursor()
    c.executemany('''
    INSERT OR REPLACE INTO champ_win_rate_any (champ, wins, losses, gameVersion, winRate, lane)
    VALUES (?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()


def is_exist_in_champ_win_rate_any(champ, gameVersion, lane):
    column1 = 'champ'
    column2 = 'gameVersion'
    column3 = 'lane'
    conn = sqlite3.connect('data/riot_data.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM champ_win_rate_any "
              f"WHERE {column1} = ? AND {column2} = ? AND {column3} = ?",
              (champ, gameVersion, lane))
    row = c.fetchone()
    conn.close()
    return row



def create_table_two_champ_combo_ally():
    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Create the 'summoner_info' table
    c.execute('''
    CREATE TABLE IF NOT EXISTS two_champ_combo_ally (
        champ1 TEXT,
        champ2 TEXT,
        wins INTEGER,
        losses INTEGER,
        tier TEXT,
        division TEXT,
        gameVersion TEXT,
        winRate REAL,
        PRIMARY KEY (champ1, champ2, gameVersion)
    )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# insert or update
def insert_update_two_champ_combo_ally(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Insert or update the list of summoners in the 'summoner_info' table
    c.executemany('''
    INSERT OR REPLACE INTO two_champ_combo_ally (champ1, champ2, wins, losses, tier, division, gameVersion, winRate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def is_exist_in_two_champ_combo_ally(v1, v2, v3):
    # Set the conditions to match the desired row
    column1 = 'champ1'
    column2 = 'champ2'
    column3 = 'gameVersion'
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Execute the SQL command to fetch the row that matches the conditions
    c.execute(f"SELECT * FROM two_champ_combo_ally "
              f"WHERE {column1} = ? AND {column2} = ? AND {column3} = ?",
              (v1, v2, v3))
    # Fetch the row from the result
    row = c.fetchone()
    conn.close()
    return row


def view_table(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name} ")
    # Commit the changes and close the connection
    rows = c.fetchall()
    conn.close()
    return rows


def view_table_schema(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Replace 'your_table_name' with the name of the table you want to check
    # Execute the SQL command to fetch the schema of the table from sqlite_master
    c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_schema = c.fetchone()
    if table_schema:
        print("Table schema:", table_schema[0])
    else:
        print("Table not found.")
    # Close the connection
    conn.close()


def get_win_rate_by_champ(table_name, champ):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    sql_command = f"SELECT * FROM {table_name} WHERE champ1 == '{champ}' OR champ2 == '{champ}'"
    c.execute(sql_command)
    rows = c.fetchall()
    conn.close()
    result_dict = {}
    for row in rows:
        if row[0] == champ:
            result_dict[row[1]] = row[7]
        else:
            result_dict[row[0]] = row[7]
    sorted_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}
    tuples_list = list(sorted_dict.items())
    return tuples_list


def get_win_rate_by_two_champ_combo(table_name, champ):
    # Connect to the SQLite database
    conn = sqlite3.connect('data/riot_data.db')
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    sql_command = f"SELECT * FROM {table_name} WHERE champ1 == '{champ}' OR champ2 == '{champ}'"
    c.execute(sql_command)
    rows = c.fetchall()
    conn.close()
    result_dict = {}
    for row in rows:
        if row[0] == champ:
            result_dict[row[1]] = row[7]
        else:
            result_dict[row[0]] = row[7]
    sorted_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}
    tuples_list = list(sorted_dict.items())
    return tuples_list