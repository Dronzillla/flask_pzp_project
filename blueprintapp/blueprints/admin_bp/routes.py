from flask import Blueprint
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from blueprintapp.app import db
from blueprintapp.blueprints.auth.models import User
from blueprintapp.blueprints.upload.models import Project
from flask_admin.menu import MenuLink


admin_bp = Blueprint("admin_bp", __name__, template_folder="templates")


class MyHomeView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")


admin = Admin(name="Admin page", template_mode="bootstrap4", index_view=MyHomeView())

# Add db model views
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Project, db.session))
# Add menu link to main page
custom_link = MenuLink(name="Main page", url="/")
admin.add_link(custom_link)


# Attach the admin interface to the app later
def init_admin(app):
    admin.init_app(app)
