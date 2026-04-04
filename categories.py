from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from models import db, CategoryModel
from schemas import SingleCategorySchema, AllCategorySchema, CategoryCreateSchema



cats_blp = Blueprint("categories", __name__, description="CRUD operations that can be performed on categories")



# =================================================
# Actions performed on full categories list route
# =================================================

@cats_blp.route("/categories")
class CategoryList(MethodView):

    # Route to GET all categories, including the count of associated tasks
    @cats_blp.response(200, AllCategorySchema(many=True))
    def get(self):
        categories = CategoryModel.query
        full_categories = []
        for c in categories:
            c_dict = c.to_dict()
            c_dict["task_count"] = len(c.tasks)
            full_categories.append(c_dict)
        return jsonify({"categories": full_categories})
    

    
    # Route to POST (create) a new category
    @cats_blp.arguments(CategoryCreateSchema)
    @cats_blp.response(201, AllCategorySchema)
    def post(self, category_data):
        new_category = CategoryModel(**category_data)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201
    


# =================================================
# Actions performed on single category route
# =================================================

@cats_blp.route("/categories/<int:category_id>")
class Category(MethodView):

    # Route to GET a single category, including the list of tasks in that category
    @cats_blp.response(200, SingleCategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category not found.")
        category_dict = category.to_dict()
        category_dict["tasks"] = [{"id": t.id, "title": t.title, "completed": t.completed} for t in category.tasks]
        return jsonify(category_dict)
    
    
    
    # Route to DELETE a single category -- but prevents deletion of categories that have tasks associated with them
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category not found.")
        if len(category.tasks) > 0:
            return jsonify({"error": "Cannot delete category with existing tasks. Move or delete tasks first."}), 400
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted."}), 200