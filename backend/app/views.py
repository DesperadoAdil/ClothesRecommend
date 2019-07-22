# -*- coding: UTF-8 -*-
from flask import Flask
from app import app

@app.route('/')
def hello_world():
    return 'Hello World!'
