import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import ModuleServer
import Settings
import json

app = Flask(__name__)

def start():
    app.config['UPLOAD_FOLDER'] = Settings.UPLOAD_FOLDER
    app.run(host="10.10.5.140")
    print("Webserver running")

def allowed_file(filename):
    components = filename.split(".")
    ext = components[len(components) - 1]
    return ext in Settings.ALLOWED_EXTENSIONS

@app.route("/")
def root():
    return "Running Neuralmodule server " + Settings.VERSION

@app.route("/loadmodule/<modulename>")
@app.route("/loadModule/<modulename>")
def loadmodule(modulename):
    ModuleServer.loadNeuralModule(modulename)
    return "Loaded " + modulename

@app.route("/predict/<modulename>", methods=['GET','POST'])
def predict(modulename):
    if not ModuleServer.isModuleLoaded(modulename):
        return modulename + " is not loaded"

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploadedImagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return json.dumps(ModuleServer.predict(modulename, uploadedImagePath).tolist(), separators=(',',':'))
        else:
            return "Couldnt upload image"

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

i = 0
start()
while(True):
    i = i + 1
    #Keep the script alive. Maybe delete unused modules after a certain time.

