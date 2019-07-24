# -*- coding: UTF-8 -*-

SECRET_KEY = "nmsl"

CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_INCLUDE = []

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root12345@localhost:3306/clothes?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 3600

SESSION_TYPE = "redis"
SESSION_PERMANENT = True
SESSION_USE_SIGNER = True
SESSION_KEY_PREFIX = ''
import redis
SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')

import os
BASEDIR = os.path.dirname(__file__)
