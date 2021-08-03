import os
import uuid
from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, DOWNLOAD_FOLDER
from utils import video_to_mp3

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def video_converter():
    if request.method == 'POST':
        video = request.files.get('video')
        if video and allowed_file(video.filename):
            filename, extension = os.path.splitext(video.filename)
            filename = f'{filename}{uuid.uuid4()}{extension}'
            filename = secure_filename(filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            converted_video = video_to_mp3(filename)
            return redirect(f'/download/{converted_video}', code=302)
        else:
            return "Error: Upload Correct Video"

    return render_template('upload.html')


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, threaded=True)