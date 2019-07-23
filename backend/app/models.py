# -*- coding: UTF-8 -*-
from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {
        'mysql_charset' : 'utf8'
    }

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    instance = db.Column(db.String(64), unique=True, nullable=False)
    place = db.Column(db.String(64), unique=False, nullable=False)
    create_time = db.Column(db.DateTime(timezone="Asia/Shanghai"), default=datetime.now())

    def __repr__(self):
        return '<Task %r %r %r>' % (self.id, self.instance, self.place)

    def dict(self):
        ret = {}
        try:
            ret['id'] = self.id
            ret['instance'] = self.instance
            ret['place'] = self.place
            ret['create_time'] = self.create_time
            return ret
        except:
            return None

    def insert(self, instance, place):
        try:
            self.instance = instance
            self.place = place
            self.create_time = datetime.now()
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return None
