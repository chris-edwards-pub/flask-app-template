from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

__version__ = "{{ cookiecutter.initial_version }}"

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = None
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("{{ cookiecutter.project_module }}.config.Config")
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from {{ cookiecutter.project_module }}.auth import bp as auth_bp
    from {{ cookiecutter.project_module }}.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from {{ cookiecutter.project_module }}.commands import register_commands

    register_commands(app)

    @app.context_processor
    def inject_version():
        return {"app_version": __version__}

    @app.context_processor
    def inject_project_name():
        return {"project_name": "{{ cookiecutter.project_name }}"}

    return app
