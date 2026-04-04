import os
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from redis import Redis
from rq import Queue
from tasks import tasks_blp
from categories import cats_blp
from models import db



# Build Flask app and set up configurations
app = Flask(__name__)
app.config["API_TITLE"] = "Task Manager API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/tasks")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Enable database migration tracking
migrate = Migrate(app, db)

# Import API blueprints to access routes
api = Api(app)
api.register_blueprint(tasks_blp)
api.register_blueprint(cats_blp)

# Redis connection and queue
redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
notification_queue = Queue("notifications", connection=redis_client)



# =================================================
# Run app, initialize tables if necessary
# =================================================

@app.cli.command("db-init")
def db_init():
    db.create_all()
    print("Database initialized!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)