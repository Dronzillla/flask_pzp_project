from flask import Blueprint, abort, redirect, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User
from blueprintapp.blueprints.upload.models import Project
from flask_admin.menu import MenuLink
from blueprintapp.utils.utilities import admin_required
from flask_login import login_required, current_user


admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


class MyHomeView(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        if current_user.is_authenticated and current_user.is_admin:
            return self.render("admin/index.html")
        flash(
            "You either have to log in or you don't have permission to view that page. "
        )
        return redirect(url_for("auth.login"))
        # abort(403)


admin = Admin(name="Admin page", template_mode="bootstrap4", index_view=MyHomeView())


# Only logged in admin user can view admin pages
class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return True

    def inaccessible_callback(self, name, **kwargs):
        flash(
            "You either have to log in or you don't have permission to view that page. "
        )
        return redirect(url_for("auth.login"))


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Project, db.session))
# Add menu link to main page
custom_link = MenuLink(name="Main page", url="/")
admin.add_link(custom_link)


# Attach the admin interface to the app later
def init_admin(app):
    admin.init_app(app)
