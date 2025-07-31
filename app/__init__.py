import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from config import Config

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


def create_app(config_class=Config):
    # app = Flask(__name__, template_folder="/app/templates", static_folder="static")
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # from app.routes import register_blueprints
    # register_blueprints(app)

    # Register blueprints AFTER app is created
    from app.routes.main import main_bp
    from app.routes.skills import skills_bp
    from app.routes.llm import llm_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(llm_bp)

    # ✅ Use context here if you're doing db.create_all or other app-specific work
    with app.app_context():
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        if not os.path.exists(db_path):
            db.create_all()
            print(f"✅ Created SQLite DB at: {db_path}")

    return app


__all__ = ["db", "cache", "create_app"]
