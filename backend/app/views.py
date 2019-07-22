# -*- coding: UTF-8 -*-
from app import app, celery
import time

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/task', methods = ["POST", "GET"])
def task():
    task = create_task.delay(10, 20)
    while True:
        if task.ready():
            break
    return "TASK!,%s" % task


@celery.task
def create_task(x, y):
    time.sleep(5)
    return x+y
