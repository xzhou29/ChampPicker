#!/bin/bash
PYTHONPAHT=. FLASK_APP="backend:create_app('config.py')" FLASK_ENV=development flask run --port 3000  --host=0.0.0.0 --no-reload

