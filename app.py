import os
from flask import Flask, redirect, url_for, render_template, request, send_from_directory, jsonify
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename
from time import sleep
import traceback
import base64
import cv2
import numpy as np
from flask_cors import CORS, cross_origin
from facial_recognition import load_database, who_is_it, load_model, load_labels, write_labels, verify

app = Flask(__name__)

CORS(app, support_credentials=True)

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

def save(encoded_data, filename):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    print(img)
    return cv2.imwrite(filename, img)

@app.route('/')
def index():
    # audioprocessing = AudioProcessing()
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/test', methods = ["POST"])
@cross_origin(supports_credentials=True)
def test():
    return jsonify({'success': 'Arrived'})   

@app.route('/uploaddata', methods = ["POST"])
@cross_origin(supports_credentials=True)
def savedata():
    if request.method == "POST":
        try:
            global FRmodel
            global database
            user_infos = request.get_json()
            id_profile = user_infos['id_picture']
            first_name = user_infos["first_name"]
            sir_name = user_infos["sir_name"]
            phone = user_infos["phone"]
            file_name = first_name.lower() + "_"+ sir_name.lower() +".png"
            
            user_info = first_name + ","+ sir_name +","+ phone +",png"
            
            write_labels(user_info)
            
            file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_IMAGE_PATH, file_name)
            save(id_profile, file_dir)
                      
            FRmodel = load_model()
            database = load_database(FRmodel)
            
            return jsonify({'success': 'Data uploaded successfuly'})   
        except Exception:
            # return redirect(url_for('home'))
            print(traceback.print_exc())
    return ""
 
@app.route('/upload', methods = ["POST"])
@cross_origin(supports_credentials=True)
def upload():
    try:        
        person = request.get_json()
        base_64_image = person['upload_image']
        first_name = person['first_name']
        sir_name = person['sir_name']
        fullname = first_name.lower() + "_"+ sir_name.lower() +".png"
        file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_PATH, fullname)
        save(base_64_image, file_dir)
        identity = fullname = first_name.lower() + " "+ sir_name.lower()
        
        dist, door_open = verify(file_dir, identity, database, FRmodel)
        if door_open and dist is not None:
            return jsonify({'success': 'Picture has been tested and percentage is going to be sent very soon', 'result': "It's " + str(person)})                    
        else:
            return jsonify({'success': 'Picture has been tested and percentage is going to be sent very soon', 'result': "It's not " + str(person)})                    
       
    except Exception:
        # return redirect(url_for('home'))
        print(traceback.print_exc())
    return ""
    


if __name__ == "__main__":    
    
    app.run(host='192.168.0.102', port=5000, debug=True)