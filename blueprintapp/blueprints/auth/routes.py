from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
from blueprintapp.app import db
from blueprintapp.blueprints.auth.forms import LoginForm, RegistrationForm
from blueprintapp.blueprints.auth.models import User
from urllib.parse import urlparse

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return f"{current_user.username}"
        # return redirect(url_for("core.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    nologin = False
    if current_user.is_authenticated:
        return f"{current_user.username}"
        # return redirect(url_for("core.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            nologin = True
        # if user is None:
        #     nologin = True
        #     # form.email.errors.append("Invalid email")
        # elif not user.check_password(form.password.data):
        #     nologin = True
        # form.password.errors.append("Invalid password.")
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("core.index")
            return redirect(next_page)
    return render_template("auth/login.html", form=form, message=nologin)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))
