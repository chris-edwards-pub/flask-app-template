from flask import render_template
from flask_login import login_required

from {{ cookiecutter.project_module }}.main import bp


@bp.route("/")
@login_required
def index():
    return render_template("index.html")
