from flask import Blueprint

bp = Blueprint("main", __name__)

from {{ cookiecutter.project_module }}.main import routes  # noqa: E402, F401
