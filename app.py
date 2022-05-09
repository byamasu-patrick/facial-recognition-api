import os
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename
from audio_processing import AudioProcessing
from time import sleep
import traceback

app = Flask(__name__)
# app.config['data']
# print(app.instance_path)
UPLOAD_PATH = "data"
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(os.path.join(os.path.dirname(__file__), UPLOAD_PATH), exist_ok=True)


assets = Environment(app)
css = Bundle("src/main.css", output="css/main.css")
js = Bundle("src/*.js", output="js/main.js") # new

assets.register("css", css)
assets.register("js", js) # new
css.build()
js.build() # new

@app.route('/')
def home():
    # audioprocessing = AudioProcessing()
    return render_template("index.html", audio_file=request.args.get('processed_audio'))

@app.route('/upload/<path:filename>')
def download_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)
 
@app.route('/upload', methods = ["POST"])
def upload():
    if request.method == "POST":
        try:
            audio_file = request.files['audiofile']
            audio_file.save(os.path.join(os.path.dirname(__file__), UPLOAD_PATH, secure_filename(audio_file.filename)))
            audioprocessing = AudioProcessing()
            
            sleep(0.5)
            print(secure_filename(audio_file.filename))
            file_ = secure_filename(audio_file.filename)
	        # 
            audioprocessing.convert(UPLOAD_PATH, file_)
	
            return redirect(url_for('home', processed_audio=file_))                    
        except Exception:
            # return redirect(url_for('home'))
            print(traceback.print_exc())
    return ""
    


if __name__ == "__main__":
    
    
    app.run(debug=True)