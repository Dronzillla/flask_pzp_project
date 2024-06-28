from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from blueprintapp.app import db


dashboard = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard.route("/")
@login_required
def index():
    username = current_user.username
    return render_template("dashboard/index.html", username=username)
