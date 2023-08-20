from flask import Flask, request, redirect, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from model import *
from resources import *
from flask_cors import CORS 
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.sqlite3"
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

app.app_context().push()
# #################### for API Instance
api.init_app(app)
CORS(app)

@app.route('/', methods=['GET','POST'])
def ToDoList():
    if request.method == 'GET':
        # tasks = Todo.query.order_by(Todo.date_created).all()
        tasks = TaskList.query.order_by(TaskList.date_created.desc()).all()
        # tasks = TaskList.query.all()
        return render_template('index.html', tasks = tasks)
    
    elif request.method =='POST':
        task_content = request.form.get("content")
        
        task = TaskList.query.filter_by(content = task_content).first()
        if task is None:
            new_task = TaskList(content = task_content)
            db.session.add(new_task)
            try:
                flash("New task created!","success")
                db.session.commit()
                return redirect('/')
            except:
                flash("something went wrong while creating task! Try again.","danger")
                return redirect('/')
        else:
            flash("Task already exist!","warning")
            return redirect('/')


@app.route('/delete/<int:id>',methods = ['GET','POST'])
def delete(id):
    # get the url on which application is running
    # url = request.host
    response = requests.delete(f"http://{request.host}/api/delete_task/{id}")
    if response.status_code == 204:
        flash("Task deleted successfully!","success")
        return redirect('/')
    
    elif response.status_code == 404:
        flash("No Task with the given id!","warning")
        return redirect('/')
    else:
        flash(f"An error occurred: {response.status_code}","danger")
        return redirect('/')
    



@app.route('/update/<int:id>',methods = ['GET','POST'])
def  update(id):
    task = TaskList.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form.get('content')
        try:
            db.session.commit()
            flash("Task updated successfully.","success")
            return redirect('/')
        except:
            flash("something goes wrong while updating the task","danger")
            return render_template('update.html',task = task)
        
    else:
        return render_template('update.html',task = task)



if __name__ == "__main__":
    app.run()
