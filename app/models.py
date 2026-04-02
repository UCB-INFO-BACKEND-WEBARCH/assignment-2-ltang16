from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app #TODO: DO I NEED TO IMPORT THIS SINCE THE FILES ARE SPLIT OUT?



db = SQLAlchemy()
db.init_app(app) #TODO: IS THIS CORRECT? DO I NEED THIS LINE? or should it be "db=SQLAlchemy(app)"?



# Task model
class TaskModel(db.Model):
    __name__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("CategoryModel", back_populates="tasks")
    created_at = db.Column(db.DateTime, default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category_id": self.category_id,
            "category": self.category.to_dict(), #TODO: IS THIS THE CORRECT WAY TO INCLUDE CATEGORY? 
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    


# Category model
class CategoryModel(db.Model):
    __name__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=True)
    tasks = db.relationship("TaskModel", back_populates="category", lazy="dynamic") #TODO: IS THIS NECESSARY IF I DON'T NEED TO INCLUDE ALL RELATED TASKS?

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }