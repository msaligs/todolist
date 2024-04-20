from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db =SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    content = db.Column(db.String(200),nullable = False,unique = True)
    date_created = db.Column(db.String(20) , default =lambda : datetime.now().strftime("%Y-%m-%d %H:%M") )
    # date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_completed = db.Column(db.String(20))
    completed = db.Column(db.Boolean, default = False)
    def __repr__(self):
        return '<Task %r>' % self.id
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,unique=True, nullable = False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    password = db.Column(db.String(128), nullable = False)

    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)