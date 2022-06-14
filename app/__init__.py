from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
import os
import pandas as pd
from io import BytesIO
from pathlib import Path

# This file work for initialize projects that will run on the website.

# This code work for calling library Flask-SQLAlchemy to use the function inside that library.
db = SQLAlchemy()

# This code work for calling library Flask-Migrate to use the function inside that library.
migrate = Migrate()

# The code below work for running main app with Flask framework using configuration from file config.py.
# This code also register the blueprint from other folder / file.
def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)
    migrate.app = app

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.dokter import dokter_bp
    app.register_blueprint(dokter_bp)

    from app.dokter_history import dokter_history_bp
    app.register_blueprint(dokter_history_bp)

    from app.pasien import pasien_bp
    app.register_blueprint(pasien_bp)

    from app.pasien_history import pasien_history_bp
    app.register_blueprint(pasien_history_bp)

    from app.trans import trans_bp
    app.register_blueprint(trans_bp)

    return app