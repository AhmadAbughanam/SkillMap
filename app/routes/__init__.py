from .main import main_bp
from .skills import skills_bp
from .llm import llm_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(llm_bp)
