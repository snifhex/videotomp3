import os
from moviepy.editor import *

from config import UPLOAD_FOLDER, DOWNLOAD_FOLDER


def video_to_mp3(file):
    video = VideoFileClip(os.path.join(UPLOAD_FOLDER, file))
    filename = f"{file.rsplit('0', 1)[0]}.mp3"
    video.audio.write_audiofile(os.path.join(DOWNLOAD_FOLDER, filename))
    os.remove(f'uploads/{file}')
    return filename
