import database
import sqlite3


def champ_recommender(selected_champs, next_selection_lane, lanes_map) -> None:
    # to recommend a list of champs for user with win rate based on selected champs
    num_selected_champs = len(selected_champs)
    if num_selected_champs == 10:
        pass
    else:
        return switch_case(num_selected_champs, selected_champs, next_selection_lane, lanes_map)


def switch_case(value, selected, next_selection_lane, lanes_map):
    switch_dict = {
        1: one_selected,
        2: two_selected,
        3: three_selected,
        4: four_selected,
        5: five_selected,
        6: six_selected,
        7: seven_selected,
        8: eight_selected,
        9: nine_selected,
    }
    # Get the function from the dictionary based on the value
    func = switch_dict.get(value)
    # If the function is found in the dictionary, call it with the selected_champs argument
    if func:
        return func(selected, next_selection_lane, lanes_map)
    return None


def one_selected(selected, next_selection_lane, lanes_map):
    # BLUE: 1 - RED: 0
    champ_1 = selected[0][0]
    lane_1 = selected[0][1]
    # TODO should use solo and any
    two_champ_combo_ally_win_rates = database.get_win_rate_by_champ('two_champ_combo_ally', champ_1)

    return two_champ_combo_ally_win_rates


def two_selected(selected_champs, lanes_map):
    # BLUE: 1 - RED: 1
    pass


def three_selected(selected_champs, next_selection_lane, lanes_map):
    # BLUE: 1 - RED: 2 - for BLUE
    champ_1 = selected_champs[0][0]
    lane_1 = selected_champs[0][1]
    two_champ_combo_ally_win_rates = database.get_win_rate_by_champ('two_champ_combo_ally', champ_1)
    # TODO two_champ_combo_any_win_rates + two_champ_combo_solo_win_rates
    return two_champ_combo_ally_win_rates


def four_selected(selected_champs, lanes_map):
    # BLUE: 2 - RED: 2
    pass


def five_selected(selected_champs, next_selection_lane, lanes_map):
    # BLUE: 3 - RED: 2
    blue_champs, blue_lanes = [], []
    red_champs, red_lanes = [], []
    for i in [0, 3, 4]:
        blue_champs.append(selected_champs[i][0])
        blue_lanes.append(selected_champs[i][1])
    for i in [1, 2]:
        red_champs.append(selected_champs[i][0])
        red_lanes.append(selected_champs[i][1])
    two_champ_combo_ally_win_rates = database.get_win_rate_by_champ('two_champ_combo_ally', blue_champs[1])
    two_champ_combo_ally_win_rates_2 = database.get_win_rate_by_champ('two_champ_combo_ally', blue_champs[2])
    two_champ_combo_ally_win_rates = combine_two_list(two_champ_combo_ally_win_rates, two_champ_combo_ally_win_rates_2)
    # TODO two_champ_combo_any_win_rates + two_champ_combo_solo_win_rates
    if next_selection_lane:
        two_champ_combo_ally_win_rates = lane_filter(two_champ_combo_ally_win_rates, lanes_map[next_selection_lane])
    return two_champ_combo_ally_win_rates



def six_selected(selected_champs, lanes_map):
    # BLUE: 3 - RED: 3
    pass


def seven_selected(selected_champs, lanes_map):
    # BLUE: 3 - RED: 4
    pass


def eight_selected(selected_champs, lanes_map):
    # BLUE: 4 - RED: 4
    pass


def nine_selected(selected_champs, lanes_map):
    # BLUE: 5 - RED: 4
    pass


def final_win_rate_prediction(selected_champs, lanes_map):
    # BLUE: 5 - RED: 5
    pass


def combine_two_list(list1, list2):
    combined_dict = {}
    count_dict = {}
    for item in list1 + list2:
        key, value = item
        if key in combined_dict:
            combined_dict[key] += value
            count_dict[key] += 1
        else:
            combined_dict[key] = value
            count_dict[key] = 1
    average_dict = {k: v / count_dict[k] for k, v in combined_dict.items()}
    average_dict = {k: v for k, v in sorted(average_dict.items(), key=lambda item: item[1], reverse=True)}
    average_list = list(average_dict.items())
    return average_list


def lane_filter(tuples_list, white_list):
    filtered_list = [item for item in tuples_list if item[0] in white_list]
    return filtered_list


def get_lanes_map(current_game_version='13.9', threshold=10):
    # champ: [lane1, lean2, ...]
    lanes_map = {}
    rows = database.view_table('match_history')
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
                # new_map[champ].add(lane)
    return new_map



# lanes_map = get_lanes_map()
# selected_champs = []
# # BLUE
# selected_champs.append(('Graves', 'JUNGLE'))
# # RED
# selected_champs.append(('Brand', 'SUPPORT'))
# selected_champs.append(('Talon', 'MID'))
# # BLUE
# selected_champs.append(('FiddleSticks', 'MID'))
# selected_champs.append(('Irelia', 'TOP'))
# # RED
# next_selection_lane = 'TOP'
