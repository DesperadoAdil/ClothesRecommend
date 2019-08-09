# -*- coding: UTF-8 -*-
from flask import request, session, url_for, render_template, current_app
from sqlalchemy import and_
from . import app, celery, api
from .models import Task
from .utils import return_response
from .demo.demo import get_demo_result
from flask_restful import Resource
import time
import json
import random
import os


@celery.task
def create_task(place):
    result = get_demo_result(place)
    return result


#@api.resource("/task")
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
                dic = task.dict()
                if session.get(task.instance):
                    ta = session.get(task.instance)
                    dic["ready"] = ta.ready()
                    dic["state"] = ta.state
                    if ta.ready():
                        dic["result"] = ta.get()
                    ret["data"].append(dic)

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

        task = create_task.delay(place)
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


#@api.resource("/task/<string:id>")
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


#api.add_resource(TaskList, "/task")
api.add_resource(TaskList, "/api/task")
#api.add_resource(TaskID, "/task/<string:id>")
api.add_resource(TaskID, "/api/task/<string:id>")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")
