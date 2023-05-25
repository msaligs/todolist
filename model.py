from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db =SQLAlchemy()

class TaskList(db.Model):
    id = db.Column(db.Integer(),primary_key = True, nullable = False)
    content = db.Column(db.String(200),nullable = False,unique = True)
    date_created = db.Column(db.String(20) , default =lambda : datetime.now().strftime("%Y-%m-%d %H:%M") )
    def __repr__(self):
        return '<Task %r>' % self.id