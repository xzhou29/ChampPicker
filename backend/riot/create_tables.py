import database
from tqdm import tqdm

# champ1 champ2 wins losses gameVersion team
def two_champ_combo_ally(team):
    for i in range(0, len(team) - 1):
        for j in range(i + 1, len(team)):
            row_1 = team[i]
            row_2 = team[j]
            _, _, _, _, gameVersion, _, _, _, _, win, championName_1, _, _, teamId = row_1
            _, _, _, _, _, _, _, _, _, _, championName_2, _, _, _ = row_2
            if championName_1 > championName_2:
                tmp = championName_1
                championName_1 = championName_2
                championName_2 = tmp
            # (champ1, champ2, wins, losses, tier, division, gameVersion)
            gameVersion = gameVersion.split('.')[:2]
            gameVersion = '.'.join(gameVersion)
            date_row = (championName_1, championName_2, 1 if win else 0, 0 if win else 1,
                        None, None, gameVersion, int(win))
            existing_row = database.is_exist_in_two_champ_combo_ally(championName_1, championName_2, gameVersion)
            if existing_row is not None:
                # update
                update_two_champ_combo_ally(date_row, existing_row)
            else:
                # insert
                insert_into_two_champ_combo_ally(date_row)


def insert_into_two_champ_combo_ally(data):
    database.insert_update_two_champ_combo_ally([data])
    # print(data)



def update_two_champ_combo_ally(data, existing_row):
    champ1, champ2, win, lose, _, _, gameVersion, _ = data
    _, _, wins, losses, tier, division, gameVersion, _ = existing_row
    win_rate = (wins+win) / (wins+win + losses+lose)
    new_data = (champ1, champ2, wins+win, losses+lose, tier, division, gameVersion, win_rate)
    database.insert_update_two_champ_combo_ally([new_data])

def two_champ_combo_solo():
    pass


def two_champ_combo_vs():
    pass


# champ1 champ2 wins losses gameVersion team
def champ_win_rate_any(champs):
    for i in range(0, len(champs)):
        row = champs[i]
        _, _, _, _, gameVersion, _, _, _, _, win, championName, _, lane, teamId = row
        gameVersion = gameVersion.split('.')[:2]
        gameVersion = '.'.join(gameVersion)
        date_row = (championName, 1 if win else 0, 0 if win else 1, gameVersion, 0.0, lane)
        existing_row = database.is_exist_in_champ_win_rate_any(championName, gameVersion, lane)
        if existing_row is not None:
            # update
            champName, win, lose, gameVersion, _, lane = date_row
            _, wins, losses, _, _, _ = existing_row
            win_rate = (wins + win) / (wins + win + losses + lose)
            new_data = (champName, wins + win, losses + lose, gameVersion, win_rate, lane)
            database.insert_update_champ_win_rate_any([new_data])
        else:
            # insert
            database.insert_update_champ_win_rate_any([date_row])


# matches = database.get_all_matches()
# print(f'number of matches: {len(matches)}')
#
# # TABLE ONE: all two-champ-combo-ally
# database.drop_table('two_champ_combo_ally')
# database.create_table_two_champ_combo_ally()
# # Iterate over the dictionary using tqdm
# for key, match_data in tqdm(matches.items(), desc='Processing items'):
#     two_champ_combo_ally(match_data)



# # TABLE TWO: individual champ win rate
# database.drop_table('champ_win_rate_any')
# database.create_table_champ_win_rate_any()
# # Iterate over the dictionary using tqdm
# for key, match_data in tqdm(matches.items(), desc='Processing items'):
#     champ_win_rate_any(match_data)

#
print(database.view_table_schema('champ_win_rate_any'))
print(database.view_table('champ_win_rate_any'))

