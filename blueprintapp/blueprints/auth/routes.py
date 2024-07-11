from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
from blueprintapp.app import db
from blueprintapp.blueprints.auth.forms import (
    LoginForm,
    RegistrationForm,
    UpdatePasswordForm,
    ConfirmDeleteForm,
)
from blueprintapp.blueprints.auth.models import User
from blueprintapp.blueprints.auth.db_operations import (
    db_create_new_user,
    db_read_user_by_email,
    db_update_current_user_password,
    db_read_user_by_id,
    db_delete_user,
)
from urllib.parse import urlparse
from blueprintapp.utils.utilities import verified_user
from blueprintapp.blueprints.auth.emails import mail_admins_new_user_registration


auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db_create_new_user(
            username=form.username.data.lower(),
            email=form.email.data.lower(),
            password=form.password.data,
        )
        flash(
            "Congratulations, you are now a registered user. Note that admin user has to confirm your account.",
            "info",
        )
        mail_admins_new_user_registration(email=form.email.data.lower())
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_read_user_by_email(email=form.email.data.lower())
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "error")
        # Check if user is verified
        elif not user.is_verified:
            flash(
                "Your account needs to be verified by an admin for you to log in.",
                "error",
            )
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("dashboard.index")
            return redirect(next_page)
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
@verified_user
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@auth.route("/update_password", methods=["GET", "POST"])
@login_required
@verified_user
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        # Verify user current password
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "error")
            return redirect(url_for("auth.update_password"))
        # Set current user password
        db_update_current_user_password(password=form.new_password.data)
        flash("Your password has been updated.", "success")
        return redirect(
            url_for("dashboard.index")
        )  # Redirect to the dashboard or another appropriate page
    return render_template("auth/update_password.html", form=form)


@auth.route("/user/delete", methods=["GET"])
@login_required
@verified_user
def confirm_delete_user():
    form = ConfirmDeleteForm()
    form.user_id.data = current_user.id
    return render_template("auth/confirm_delete.html", form=form)


@auth.route("/user/delete", methods=["POST"])
@login_required
@verified_user
def delete_user():
    form = ConfirmDeleteForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        if current_user.id != int(user_id):
            return "Unauthorized", 403
        user = db_read_user_by_id(id=user_id)
        if user is None:
            return "User not found", 404
        # Delete user and any related data
        db_delete_user(user=user)
        # Logout user
        logout_user()
        flash("Your account has been successfully deleted.", "success")
        return redirect(url_for("core.index"))
    else:
        return "Invalid form submission", 400
