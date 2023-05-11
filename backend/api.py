from flask import Flask, jsonify, Blueprint, request, Response, send_file, current_app
from flask_cors import CORS
from backend.riot.champ_picker import ChampPicker
from backend import utils
from flask import send_from_directory
import time

bp = Blueprint('api', __name__, static_folder='static')
CORS(bp)


@bp.route('/', methods=['GET'])
def hello():
    return "Hello, World!"


@bp.route('/champ_picker', methods=['POST'])
def champ_picker():
    selections = request.json
    # print(selections)
    # Do something with the selections object
    # Compute the win rates...+
    if len(selections) < 5:
        team_one_win_rate = None
        team_two_win_rate = None
    else:
        picker = ChampPicker()
        picker.update_data(selections)
        team_one_win_rate = picker.team_1_win_rate
        team_two_win_rate = picker.team_2_win_rate
        # team_1_champs_pick = picker.team_1_champs_with_win_rate
        # team_2_champs_pick = picker.team_2_champs_with_win_rate

    return jsonify({
        'teamOneWinRate': team_one_win_rate,
        'teamTwoWinRate': team_two_win_rate,
    })


@bp.route('/initial_data', methods=['POST'])
def initial_data():
    champDataAny = utils.extract_win_rate_any_champ(request.json)
    return jsonify({
        'champDataAny': champDataAny,
    })