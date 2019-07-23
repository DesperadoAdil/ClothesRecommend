# -*- coding: UTF-8 -*-
from flask import request
from . import app, celery, api
from .models import Task
from .utils import return_response
from flask_restful import Resource
import time
import json

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/taskk', methods = ["POST", "GET"])
def taskk():
    task = create_task.delay(10, 20)
    while True:
        if task.ready():
            break
    return "TASK!,%s, %s" % (task,task.get())


@celery.task
def create_task(x, y):
    time.sleep(15)
    return x+y


@api.resource("/task")
class TaskList(Resource):

    """
    return task list.
    """
    def get(self):
        ret = {}
        ret["data"] = []
        status = 202
        ret['message'] = "accepted"

        tasks = Task.query.order_by(Task.create_time.desc()).all()
        if tasks:
            for task in tasks:
                ret["data"].append(task.dict())
            ret["message"] = "success"
            status = 200
        else:
            ret["message"] = "task not found"
            ret.pop("data")
            status = 404

        return return_response(status=status, ret=ret)


    """
    create a task.
    """
    def post(self):
        ret = {}
        status = 202
        ret['message'] = "accepted"

        try:
            data = json.loads(request.get_data())
            place = data["place"]
        except:
            ret["message"] = "invalid request"
            status = 400
            return return_response(status=status, ret=ret)

        task = create_task.delay(1, 2)
        ta = Task().insert(str(task), place)
        if ta:
            ret["message"] = "success"
            status = 201
        else:
            ret["message"] = "invalid request"
            status = 400

        return return_response(status=status, ret=ret)


api.resource("/task/<string:id>")
class TaskID(Resource):

    """
    get a task by id.
    """
    def get(self, id):
        pass


    """
    delete a task by id.
    """
    def delete(self, id):
        pass
