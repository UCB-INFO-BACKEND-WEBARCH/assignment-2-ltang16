from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from models import db, TaskModel, CategoryModel
from schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
import datetime



tasks_blp = Blueprint("tasks", __name__, description="CRUD operations that can be performed on tasks")
#TODO: do I need to use this format??? how would I separate out the format from exploration 10??? 



# Actions performed on full tasks list route
@tasks_blp.route("/tasks")
class TaskList(MethodView):

    # Route to GET all tasks, optionally filtering on completion status
    @tasks_blp.response(200, TaskSchema(many=True))
    def get(self):
        completed = request.args.get("completed")
        tasks = TaskModel.query
        if completed:
            if completed == "true":
                tasks = tasks.filter_by(completed=True)
            else:
                tasks = tasks.filter_by(completed=False)
        return jsonify({"tasks": [t.to_dict() for t in tasks]})
    
    # Route to POST (create) a new task
    @tasks_blp.arguments(TaskCreateSchema)
    @tasks_blp.response(201, TaskSchema)
    def post(self, task_data):
        # Check if the given category ID exists -- if not, throw an error
        category_id = task_data.get("category_id")
        ids = [c.to_dict().get("id") for c in CategoryModel.query.all()]
        if category_id and (category_id not in ids):
            return jsonify({"error": "The new task's category ID must already exist."}), 400
        new_task = TaskModel(**task_data)
        new_task.created_at = datetime.datetime.now(datetime.UTC)
        db.session.add(new_task)
        db.session.commit()



# Actions performed on single task route
@tasks_blp.route("/tasks/<int:task_id>")
class Task(MethodView):

    # Route to GET the task, category information included
    @tasks_blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id, description="Task not found.")
        return task
    
    # Route to PUT (update) the task with whatever fields are provided
    @tasks_blp.arguments(TaskUpdateSchema)
    @tasks_blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get_or_404(task_id, description="Task not found.")
        # Check if category ID (if given) exists -- if not, throw an error
        if task_data.get("category_id"):
            ids = [c.to_dict().get("id") for c in CategoryModel.query.all()]
            if task_data.get("category_id") not in ids:
                return jsonify({"error": "The category ID must already exist."}), 400
        task.title = task_data.get("title", task.title)
        task.description = task_data.get("description", task.description)
        task.completed = task_data.get("completed", task.completed)
        task.due_date = task_data.get("due_date", task.due_date)
        task.category_id = task_data.get("category_id", task.category_id)
        task.updated_at = datetime.datetime.now(datetime.UTC)
        db.session.commit()
        return task
    
    # Route to DELETE the task
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id, description="Task not found.")
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted."}), 200