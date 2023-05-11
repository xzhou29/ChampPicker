import database
from tqdm import tqdm


def analyze_match(data):
    two_champ_combo_ally(data)


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
    champ1, champ2, win, lose, _, _, gameVersion = data
    _, _, wins, losses, tier, division, gameVersion = existing_row
    win_rate = (wins+win) / (wins+win + losses+lose)
    new_data = (champ1, champ2, wins+win, losses+lose, tier, division, gameVersion, win_rate)
    database.insert_update_two_champ_combo_ally([new_data])

def two_champ_combo_solo():
    pass


def two_champ_combo_vs():
    pass

# TABLE ONE: all two-champ-combo-ally
# TABLE TWO: all individual champ
# TABLE THREE:

# database.drop_table('two_champ_combo_ally')
database.create_table_two_champ_combo_ally()
matches = database.get_all_matches()
# print(matches)
# Iterate over the dictionary using tqdm
for key, match_data in tqdm(matches.items(), desc='Processing items'):
    analyze_match(match_data)

# print(database.view_table('two_champ_combo_ally'))


