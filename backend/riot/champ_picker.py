# extract data
import sqlite3


class ChampPicker:
    def __init__(self):
        self.team_1 = {}
        self.team_2 = {}
        self.previous_team_1_list = []
        self.previous_team_2_list = []
        self.team_1_win_rate = 50.0
        self.team_2_win_rate = 50.0
        self.selected_champs = set()
        self.selected_lanes_team_1 = set()
        self.selected_lanes_team_2 = set()
        self.lanes_map = self.get_lanes_map()
        self.team_1_champs_with_win_rate = None
        self.team_2_champs_with_win_rate = None

    def update_data(self, selections):
        # STEP 1
        self.get_team_info(selections)
        self.champ_recommender()

    def get_team_info(self, selections):
        for key in selections:
            team, name, lane = selections[key]
            self.selected_champs.add(name)
            if team == 'Team 1':
                self.team_1[key] = selections[key]
                if lane != 'Lane':
                    self.selected_lanes_team_1.add(lane)
            else:
                self.team_2[key] = selections[key]
                if lane != 'Lane':
                    self.selected_lanes_team_2.add(lane)

    def get_lanes_map(self, current_game_version='13.9', threshold=10):
        # champ: [lane1, lean2, ...]
        lanes_map = {}
        rows = self.view_table('match_history')
        for row in rows:
            champ = row[10]
            lane = row[12]
            game_version = row[4]
            game_version = game_version.split('.')[:2]
            game_version = '.'.join(game_version)
            if game_version == current_game_version and lane != 'NONE':
                if champ in lanes_map:
                    if lane not in lanes_map[champ]:
                        lanes_map[champ][lane] = 1
                    else:
                        lanes_map[champ][lane] += 1
                else:
                    lanes_map[champ] = {lane: 1}
        new_map = {}
        for lane in ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM']:
            new_map[lane] = set()
        for champ in lanes_map:
            lane_map = lanes_map[champ]
            for lane in lane_map:
                if lane_map[lane] > threshold:
                    new_map[lane].add(champ)
        return new_map

    def view_table(self, table_name):
        conn = sqlite3.connect('data/riot_data.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name} ")
        rows = c.fetchall()
        conn.close()
        return rows

    def champ_recommender(self):
        # to recommend a list of champs for user with win rate based on selected champs
        num_selected_champs = len(self.selected_champs)
        if num_selected_champs == 10:
            return
        else:
            return self.switch_case(num_selected_champs)

    def switch_case(self, num_selected_champs):
        #
        def get_win_rate_all_combos(selected, table_name='two_champ_combo_ally'):
            win_rate_list = []
            length = len(selected)
            if length == 0:
                return 0.5
            elif length == 1:
                win_rate_list = self.get_win_rate_by_champ_from_combo(table_name, selected[0])
            else:
                for i in range(0, length - 1):
                    for j in range(i + 1, length):
                        champ1 = selected[i]
                        champ2 = selected[j]
                        # print(champ1, champ2)
                        win_rate_list += self.get_win_rate_by_two_champ_combo(table_name, champ1, champ2)
            average = sum(win_rate_list) / len(win_rate_list)
            return average

        def get_win_rate_one_to_selected(champ, selected, table_name='two_champ_combo_ally'):
            win_rate_list = []
            length = len(selected)
            for selected_champ in selected:
                champ1, champ2 = sorted([champ, selected_champ])
                win_rate_list += self.get_win_rate_by_two_champ_combo(table_name, champ1, champ2)
            average = sum(win_rate_list) / len(win_rate_list)
            return average

        def get_champ_with_win_rate(selected):
            all_results = []
            # champName: 'Annie',
            # laneName: 'MIDDLE',
            # iconImageLink: 'https://cdn.communitydragon.org/10.16.1/champion/Annie/square',
            # winRate: '51.2%'
            for lane in self.lanes_map:
                champ_set_for_this_lane = self.lanes_map[lane]
                for champ in champ_set_for_this_lane:
                    if champ in self.selected_champs:
                        continue
                    win_rate = get_win_rate_one_to_selected(champ, selected)
                    data_entry = {'champName': champ,
                                  'laneName': lane,
                                  'winRate': "{:.1f}".format(round(win_rate * 100, 1)),
                                  'iconImageLink': f"https://cdn.communitydragon.org/13.9.0/champion/"
                                                   f"{''.join(champ.split())}/square"
                                  }
                    all_results.append(data_entry)
            return all_results

        def any_selected():
            # team 1 win rate
            team_1_list = [item[1] for item in self.team_1.values()]
            team_1_list = sorted(team_1_list)
            team_1_win_rate = get_win_rate_all_combos(team_1_list)
            # team 2 win rate
            team_2_list = [item[1] for item in self.team_2.values()]
            team_2_list = sorted(team_2_list)
            team_2_win_rate = get_win_rate_all_combos(team_2_list)

            # calculate win rate
            self.team_1_win_rate = round((team_1_win_rate / (team_1_win_rate + team_2_win_rate) ) * 100, 1)
            self.team_2_win_rate = 100 - self.team_1_win_rate

            if team_1_list != self.previous_team_1_list:
                self.team_1_champs_with_win_rate = get_champ_with_win_rate(team_1_list)
                self.previous_team_1_list = team_1_list

            if team_2_list != self.previous_team_2_list :
                self.team_2_champs_with_win_rate = get_champ_with_win_rate(team_2_list)
                self.previous_team_2_list = team_2_list

        switch_dict = {
            1: any_selected,
            2: any_selected,
            3: any_selected,
            4: any_selected,
            5: any_selected,
            6: any_selected,
            7: any_selected,
            8: any_selected,
            9: any_selected,
        }
        # Get the function from the dictionary based on the value
        func = switch_dict.get(num_selected_champs)
        # If the function is found in the dictionary, call it with the selected_champs argument
        if func:
            return func()
        return None

    def get_win_rate_by_two_champ_combo(self, table_name, champ1, champ2):
        conn = sqlite3.connect('data/riot_data.db')
        c = conn.cursor()
        sql_command = f"SELECT * FROM {table_name} WHERE champ1 == '{champ1}' AND champ2 == '{champ2}'"
        c.execute(sql_command)
        rows = c.fetchall()
        conn.close()
        win_rate = []
        for row in rows:
            win_rate.append(row[7])
        if not win_rate:
            return [0.3]
        return win_rate

    def get_win_rate_by_champ_from_combo(self, table_name, champ):
        conn = sqlite3.connect('data/riot_data.db')
        c = conn.cursor()
        sql_command = f"SELECT * FROM {table_name} WHERE champ1 == '{champ}' OR champ2 == '{champ}'"
        c.execute(sql_command)
        rows = c.fetchall()
        conn.close()
        win_rate = []
        for row in rows:
            win_rate.append(row[7])
        if not win_rate:
            return [0.3]
        return win_rate

    def get_win_rate_by_champ_from_any(self, table_name, champ):
        conn = sqlite3.connect('data/riot_data.db')
        c = conn.cursor()
        sql_command = f"SELECT * FROM {table_name} WHERE champ1 == '{champ}' OR champ2 == '{champ}'"
        c.execute(sql_command)
        rows = c.fetchall()
        conn.close()
        win_rate = []
        for row in rows:
            win_rate.append(row[7])
        if not win_rate:
            return [0.3]
        return win_rate