# -*- coding: UTF-8 -*-
from flask import Flask
from celery import Celery
from flask_session import Session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

Session(app)
api = Api(app)
db = SQLAlchemy(app, use_native_unicode="utf8")

from app import views, models, utils
