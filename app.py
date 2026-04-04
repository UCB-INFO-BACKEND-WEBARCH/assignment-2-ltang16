import os
from flask import Flask
from flask_smorest import Api
from tasks import tasks_blp
from categories import cats_blp
from models import db



app = Flask(__name__)
app.config["API_TITLE"] = "Task Manager API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/tasks")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)
api.register_blueprint(tasks_blp)
api.register_blueprint(cats_blp)



# =================================================
# Run app, initialize tables if necessary
# =================================================

@app.cli.command("db-init")
def db_init():
    db.create_all()
    print("Database initialized!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)