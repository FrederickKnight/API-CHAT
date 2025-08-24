from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
from .error_handler import register_error_handlers

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
cors = CORS()
socketio = SocketIO()

basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.abspath(os.path.join(basedir, 'static', 'uploads'))
    
app:Flask = Flask(__name__)

def create_app():
    
    if os.environ.get("DB_URL") is None:
        load_dotenv()

    register_error_handlers(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = upload_folder

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    socketio.init_app(app, cors_allowed_origins="*",async_mode="eventlet")
    
    from app.models import (
        BaseModel,
    )
    
    with app.app_context():
        db.create_all()

    define_routes(app)
    
    return app

def define_routes(app:Flask):
    # -------------------------------- Routes --------------------------------
    
    from app.routes import (
        AuthUserRoute,
    )
    
    #user & auth
    app.register_blueprint(AuthUserRoute().get_blueprint(),url_prefix="/api/auth/user")

    # from app.routes import (
    #     ExampleRoute,
    # )

    # # routes
    # app.register_blueprint(ExampleRoute().get_blueprint(),url_prefix="/api/example/")