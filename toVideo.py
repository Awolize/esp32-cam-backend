# server.py
from datetime import datetime
import subprocess
import os
import glob

from flask import Flask, jsonify, send_file
app = Flask(__name__)

last_updated = datetime.utcnow()


@app.route('/api/new_video/')
def get_tasks():
    toVideo()
    return jsonify(success=True)


def clear_images():
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)


@app.route('/api/get_video/')
def get_video():
    return send_file('videos/3.mp4', download_name='3.mp4')


@app.route('/api/get_thumbnail/')
def get_thumbnail():
    return send_file('images/thumbnail.png', download_name='thumbnail.png')


@app.route('/api/fetch_info/')
def fetch_info():
    global last_updated

    files = glob.glob('images/*')

    print(f"Number of files: {len(files)}")
    return jsonify(len=f"{len(files)}", last_updated=last_updated)


def toVideo():
    global last_updated
    last_updated = datetime.utcnow()

    ffmpeg = "/usr/bin/ffmpeg"

    try:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-framerate",
                "30",
                "-pattern_type",
                "glob",
                "-i",
                "./images/*.png",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "videos/2.mp4",
            ],
        )

    except Exception as e:
        print("Could not create video 2.mp4, empty images dir?")
        return

    clear_images()

    try:
        import shutil
        shutil.copyfile('videos/3.mp4', 'videos/1.mp4')
    except Exception as e:
        print(e)

    try:
        subprocess.run(
            [
                ffmpeg,
                "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "videos/3.mp4"
            ],
        )

        os.remove("videos/1.mp4")
        os.remove("videos/2.mp4")

    except Exception as e:
        print(e)
        pass

    return


if __name__ == '__main__':
    # toVideo() # for testing
    app.run(host='0.0.0.0', debug=True)
