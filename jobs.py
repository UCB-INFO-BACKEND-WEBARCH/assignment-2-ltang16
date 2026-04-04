from flask import Flask
from models import db, TaskModel
import os 
import time



# Distinct Flask app context for worker
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/tasks")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



# Function that simulates sending a task reminder notification if its deadline is within 24 hours
# Runs in the worker process! Occurs after the user has already received their task creation response 
def send_notification(task_id):
    with app.app_context():
        task = TaskModel.query.get_or_404(task_id, description="Task not found.")
        time.sleep(5)
        print(f"Reminder: Task '{task.title}' is due soon!")