from flask import Flask, render_template


from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db: SQLAlchemy = SQLAlchemy(app)


# Models file

from flask_sqlalchemy import SQLAlchemy


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
