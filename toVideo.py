# server.py
from flask import Flask, jsonify, send_file
app = Flask(__name__)


@app.route('/api/new_video/')
def get_tasks():
    toVideo()
    return jsonify(success=True)


@app.route('/api/clear_images/')
def clear_images():
    import os
    import glob

    files = glob.glob('images/*')
    for f in files:
        print(f)
        os.remove(f)

    return jsonify(success=True)


@app.route('/api/get_video/')
def get_video():
    return send_file('videos/out.mp4', download_name='out.mp4')


@app.route('/api/get_thumbnail/')
def get_thumbnail():
    return send_file('images/00000.png', download_name='00000.png')


@app.route('/api/fetch_info/')
def fetch_info():
    import glob

    files = glob.glob('images/*')

    print(f"Number of files: {len(files)}")
    return jsonify(len=f"{len(files)}")


def toVideo():
    import subprocess

    ffmpeg = "/usr/bin/ffmpeg"

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
            "videos/out.mp4",
        ],
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
