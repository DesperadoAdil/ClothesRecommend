# -*- coding: UTF-8 -*-

from datetime import datetime
import json

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


from flask import make_response

def return_response(status, ret):
    response = make_response(json.dumps(ret, cls=DateEncoder, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json;charset=utf8'
    response.status_code = status
    return response
