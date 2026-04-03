from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from models import db, CategoryModel
from schemas import SingleCategorySchema, AllCategorySchema, CategoryCreateSchema



cats_blp = Blueprint("categories", __name__, description="CRUD operations that can be performed on categories")



# Actions performed on full categories list route
@cats_blp.route("/categories")
class CategoryList(MethodView):

    # Route to GET all categories, including the count of associated tasks
    @cats_blp.response(200, AllCategorySchema(many=True))
    def get(self):
        categories = CategoryModel.query
        return jsonify({"categories": [c.to_dict() for c in categories]})
    
    # Route to POST (create) a new category
    @cats_blp.arguments(CategoryCreateSchema)
    @cats_blp.response(201, AllCategorySchema)
    def post(self, category_data):
        new_category = CategoryModel(**category_data)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201