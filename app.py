from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from model import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.sqlite3"
db.init_app(app)

app.app_context().push()

@app.route('/', methods=['GET','POST'])
def ToDoList():
    if request.method == 'GET':
        # tasks = Todo.query.order_by(Todo.date_created).all()
        tasks = TaskList.query.order_by(TaskList.date_created).all()
        # tasks = TaskList.query.all()
        return render_template('index.html', tasks = tasks)
    
    elif request.method =='POST':
        task_content = request.form['content']
        new_task = TaskList(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "Task is Already there"
        return redirect('/')


@app.route('/delete/<int:id>',methods = ['GET','POST'])
def delete(id):
    content = TaskList.query.get_or_404(id)
    try:
        db.session.delete(content)
        db.session.commit()
    except:
        return "unable to delete!"
    
    return redirect('/')



@app.route('/update/<int:id>',methods = ['GET','POST'])
def  update(id):
    task = TaskList.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "unable to update the task"
        
    else:
        return render_template('update.html',task = task)
    


if __name__ == "__main__":
    app.run(debug=True)
