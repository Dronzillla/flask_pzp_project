from blueprintapp.app import db
from blueprintapp.app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    is_admin = db.Column(db.Boolean)
    is_verified = db.Column(db.Boolean)
    password_hash = db.Column(db.String(200))

    # Relationships (PK) one to many
    project = db.relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A function how users are logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
