from flask import Flask, request, redirect, render_template,flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from model import *
from resources import *
from flask_cors import CORS 
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.sqlite3"
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

app.app_context().push()
# #################### for API Instance
api.init_app(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/task')
    return render_template('index.html')


@app.route('/user_login' , methods = ['GET','POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect('/task')
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()

        if user is not None and check_password_hash(user.password,password):
            login_user(user)
            flash("Login successful!","success")
            return redirect('/task')
        else:
            flash("Invalid email or password!","danger")
            return redirect('/')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/task', methods=['GET','POST'])
@login_required
def task():
    if request.method == 'GET':
        # tasks = Todo.query.order_by(Todo.date_created).all()
        id = current_user.id
        tasks = Task.query.filter_by(user_id = id).order_by(Task.date_created.desc()).all()
        # tasks = Task.query.order_by(Task.date_created.desc()).all()
        # tasks = Task.query.all()
        return render_template('task.html', tasks = tasks)
        return render_template('login.html')
    
    elif request.method =='POST':
        task_content = request.form.get("task")
        
        task = Task.query.filter_by(content = task_content).first()
        if task is None:
            new_task = Task(content = task_content,user_id = current_user.id)
            db.session.add(new_task)
            try:
                db.session.commit()
                flash("New task created!","success")
                return redirect('/task')
            except Exception as e:
                flash("something went wrong while creating task! Try again.","danger")
                print(datetime.utcnow())
                print(e)
                return redirect('/task')
        else:
            flash("Task already exist!","warning")
            return redirect('/task')


@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user is None:
            new_user = User(username = username,email = email,password = generate_password_hash(password))

            db.session.add(new_user)
            try:
                db.session.commit()
                flash("New user created successfully!","success")
                return redirect('/user_login')
            except:
                flash("Something went wrong while creating user! Try again.","danger")
                return redirect('/register')
        else:
            flash("email already exist!","warning")
            return redirect('/register')

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    task.date_completed = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        db.session.commit()
        flash("Task completed successfully!","success")
        return redirect('/task')
    except:
        flash("Something went wrong while completing the task!","danger")
        return redirect('/task')


# @app.route('/delete/<int:id>',methods = ['GET','POST'])
# def delete(id):
#     # get the url on which application is running
#     # url = request.host
#     response = requests.delete(f"http://{request.host}/api/delete_task/{id}")
#     if response.status_code == 204:
#         flash("Task deleted successfully!","success")
#         return redirect('/')
    
#     elif response.status_code == 404:
#         flash("No Task with the given id!","warning")
#         return redirect('/')
#     else:
#         flash(f"An error occurred: {response.status_code}","danger")
#         return redirect('/')
    



@app.route('/update/<int:id>',methods = ['GET','POST'])
@login_required
def  update(id):
    task = Task.query.get_or_404(id)
    
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
    app.run(debug=True)
