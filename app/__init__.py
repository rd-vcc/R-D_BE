from flask import Flask
from app.config import Config
from app.extensions import db
from flask_cors import CORS
from app.routes.project import project
from app.routes.plan import plan
from app.routes.userrole import user
from app.routes.auth import auth
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(
        app,
        resources={r"/*": {"origins": r"http://localhost:\d+"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )
    app.register_blueprint(project)
    app.register_blueprint(plan)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    return app
