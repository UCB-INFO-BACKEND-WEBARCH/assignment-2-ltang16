import os
from flask import Flask, jsonify, request
from flask_smorest import Api
from routes.tasks import tasks_blp
from models import db



app = Flask(__name__)
app.config["API_TITLE"] = "Task Manager API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
#TODO: SWITCH THIS TO POSTGRES IN FINAL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///tasks.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)
api.register_blueprint(tasks_blp)









# =================================================
# Run app, initialize tables if necessary
# =================================================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)