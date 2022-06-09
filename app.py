import os
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename
from time import sleep
import traceback
from facial_recognition import load_database, who_is_it, load_model, load_labels, write_labels

app = Flask(__name__)

FRmodel = load_model()
database = load_database(FRmodel)
# app.config['data']
# print(app.instance_path)
UPLOAD_PATH = "database"
UPLOAD_IMAGE_PATH = "images"
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "uploaded")
os.makedirs(os.path.join(os.path.dirname(__file__), UPLOAD_PATH), exist_ok=True)


assets = Environment(app)
css = Bundle("src/main.css", output="css/main.css")
js = Bundle("src/*.js", output="js/main.js") # new

assets.register("css", css)
assets.register("js", js) # new
css.build()
js.build() # new

@app.route('/')
def index():
    # audioprocessing = AudioProcessing()
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/uploaddata', methods = ["POST"])
def savedata():
    if request.method == "POST":
        try:
            id_profile = request.files['id_picture']
            first_name = request.form.get("first_name")
            sir_name = request.form.get("sir_name")
            phone = request.form.get("phone")
            file_name = first_name + " "+ sir_name
            extension = secure_filename(id_profile.filename).split(".")[1]
            id_profile.filename = file_name +"."+ extension
            #print(secure_filename(id_profile.filename))
            user_info = first_name + ","+ sir_name +","+ phone +","+ extension
            
            write_labels(user_info)
            
            file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_IMAGE_PATH, secure_filename(id_profile.filename))
            id_profile.save(os.path.join(os.path.dirname(__file__), UPLOAD_IMAGE_PATH, secure_filename(id_profile.filename)))
            
            # who_is_it(file_dir, database, FRmodel)
            global FRmodel
            global database            
            FRmodel = load_model()
            database = load_database(FRmodel)
            
            return redirect(url_for('index'))  
        except Exception:
            # return redirect(url_for('home'))
            print(traceback.print_exc())
    return ""
 
@app.route('/upload', methods = ["POST"])
def upload():
    if request.method == "POST":
        try:
            data_file = request.files['original']
            file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_PATH, secure_filename(data_file.filename))
            data_file.save(os.path.join(os.path.dirname(__file__), UPLOAD_PATH, secure_filename(data_file.filename)))
            
            who_is_it(file_dir, database, FRmodel)
            
            return redirect(url_for('index'))                    
        except Exception:
            # return redirect(url_for('home'))
            print(traceback.print_exc())
    return ""
    


if __name__ == "__main__":
    
    
    app.run(debug=True)