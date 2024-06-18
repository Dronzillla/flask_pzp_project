from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from openpyxl import load_workbook
from io import BytesIO

from parse_project import ProjectParser


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"


class UploadForm(FlaskForm):
    file = FileField("Upload .xlsm file")
    submit = SubmitField("Upload")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file.filename.endswith(".xlsm"):
            # Read the file in memory
            in_memory_file = BytesIO(file.read())
            # Load workbook
            workbook = load_workbook(
                filename=in_memory_file, keep_vba=False, data_only=True
            )
            parser = ProjectParser(workbook=workbook)

            parser.fetch_project_info()

            date = 1
            return f"{date}"
        else:
            return "Only .xlsm files are allowed."
    return render_template("upload.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
