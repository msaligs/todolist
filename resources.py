from flask_restful import Api, Resource, reqparse, marshal_with,fields
from model import *

api = Api()

parser = reqparse.RequestParser()
parser.add_argument('t_content')

task_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'date_created': fields.String
}

class Api_task(Resource):
    @marshal_with(task_fields)
    def get(self):
        all_tasks = {}
        t1 = TaskList.query.all()
        for t in t1:
            tl = [t.content,t.date_created]
            all_tasks[t.id] = tl
        return all_tasks
    
    def put(self,id):
        t1 = TaskList.query.get(id)
        info = parser.parse_args()
        t1.content = info['t_content']
        db.session.commit()
        return {'task_content':info['t_content'],'status':'Updated'}, 201
    def  delete(self,id):
        task = TaskList.query.get(id)
        print(task)
        if task is None:
            return {'error':'Task not found'}, 404
        
        db.session.delete(task)
        db.session.commit()
        return '', 204
    
api.add_resource(Api_task,"/api/all_task","/api/update_task/<int:id>","/api/delete_task/<int:id>")
