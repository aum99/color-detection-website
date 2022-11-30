from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from colorthief import ColorThief
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/"
app.config["SECRET_KEY"] = "Thisisasecretkey"

class ImageForm(FlaskForm):
    submit = SubmitField("Generate")

@app.route('/', methods=["GET","POST"])
def home_page():
    form = ImageForm()
    if form.validate_on_submit():
        image = request.files["inputGroupFile"]
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = f"static/{image.filename}"
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=10)
        os.remove(f"static/{image.filename}")
        print(palette)
        return render_template('colors.html', palette=palette)
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)