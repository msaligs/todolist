# ToDoList Flask Application

This is a simple ToDoList application built using Flask, which allows users to create, update, and delete tasks. The application uses SQLAlchemy for database management and integrates with a RESTful API for task management.

## Installation

1. Clone the repository using the following command:
   ```
   git clone https://github.com/msaligs/todolist.git
   ```

2. Navigate to the project directory:
   ```
   cd todolist
   ```

3. Install the required dependencies using `pip`:
   ```
   pip install -r requirements.txt
   ```

4. Create the database by running the following commands:
   ```
   python
>>> from app import db  
>>> db.create_all()
>>> exit()

   ```

## Usage

1. Run the Flask application locally:
   ```
   flask run
   ```

2. Access the application in your web browser by visiting `http://127.0.0.1:5000/`.

3. Create, update, and delete tasks as needed through the user interface.

## API Integration

The application also provides an API for task management. The API can be accessed using the following endpoints:

- `GET /api/tasks`: Get a list of all tasks.
- `POST /api/tasks`: Create a new task.
- `GET /api/tasks/<task_id>`: Get details of a specific task.
- `PUT /api/tasks/<task_id>`: Update a specific task.
- `DELETE /api/tasks/<task_id>`: Delete a specific task.

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-CORS
- requests
  
