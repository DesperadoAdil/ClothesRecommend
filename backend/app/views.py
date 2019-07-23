# -*- coding: UTF-8 -*-
from flask import request, session, url_for
from sqlalchemy import and_
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
    return "TASK!, %s, %s" % (task, task.get())


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

        tasks = Task.query.filter_by(is_deleted=False).order_by(Task.create_time.desc()).all()
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
        ta = Task().insert(task.task_id, place)
        if ta:
            session[ta.instance] = task

            ret["id"] = ta.id
            ret["instance"] = ta.instance
            ret["link"] = url_for('taskid', id=ta.instance, _external=True)
            ret["message"] = "success"
            status = 201
        else:
            ret["message"] = "invalid request"
            status = 400

        return return_response(status=status, ret=ret)


@api.resource("/task/<string:id>")
class TaskID(Resource):

    """
    get a task by id.
    """
    def get(self, id):
        ret = {}
        status = 202
        ret['message'] = "accepted"

        task = Task.query.filter(and_(Task.instance==id, Task.is_deleted==False)).first()
        if not task:
            ret["message"] = "task not found"
            status = 404
        else:
            if session.get(id):
                ta = session.get(id)
                ret["ready"] = ta.ready()
                ret["state"] = ta.state
                if ta.ready():
                    ret["result"] = ta.get()
            else:
                ret["ready"] = False
                ret["state"] = "SESSION LOST"

            ret["data"] = task.dict()
            ret["message"] = "success"
            status = 200

        return return_response(status=status, ret=ret)


    """
    delete a task by id.
    """
    def delete(self, id):
        ret = {}
        status = 202
        ret['message'] = "accepted"

        task = Task.query.filter(and_(Task.instance==id, Task.is_deleted==False)).first()
        if not task:
            ret["message"] = "task not found"
            status = 404
        else:
            if session.get(id):
                session.pop(id)

            if task.delete():
                ret["message"] = "success"
                status = 200
            else:
                ret["message"] = "unknown error"
                status = 500

        return return_response(status=status, ret=ret)
