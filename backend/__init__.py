from flask import g, render_template, send_file, Flask, send_from_directory
from logging.config import dictConfig
import requests
import logging

def create_app(config_filename, config_overrides=dict()):
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    # create and configure the app
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile(config_filename)
    app.config.update(config_overrides)

    # initialize
    with app.app_context():
        app.API_KEY = app.config['API_KEY']
    from . import api
    app.register_blueprint(api.bp, url_prefix='/api')

    # @app.route('/static/<path:filename>')
    # def serve_static(filename):
    #     response = send_from_directory(app.static_folder, filename)
    #     # Set caching headers
    #     response.cache_control.max_age = 31536000  # Cache for 1 year
    #     response.expires = int(time.time() + 31536000)
    #     return response
    # Disable logging for static file requests
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if app.debug:
            return requests.get('http://localhost:3000/{}'.format(path)).text
            # return send_from_directory(app.static_folder, 'index.html')
        return send_from_directory(app.static_folder, 'index.html')


    return app

