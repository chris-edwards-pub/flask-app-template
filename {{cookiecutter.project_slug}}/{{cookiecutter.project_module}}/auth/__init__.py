from flask import Blueprint

bp = Blueprint("auth", __name__)

from {{ cookiecutter.project_module }}.auth import routes  # noqa: E402, F401
