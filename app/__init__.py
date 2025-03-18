from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    myapp = Flask(__name__)
    myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    myapp.secret_key = 'secret_key'
    db.init_app(myapp)
    migrate = Migrate(myapp, db)

    from app import routes, models

    User, Item = models.construct_models(db)

    main_bp = routes.construct_routes(db, Item, User)

    myapp.register_blueprint(main_bp)
    return myapp
