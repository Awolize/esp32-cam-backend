# server.py
import time
import os
import glob
from pathlib import Path
from cv2 import log
import django
import ffmpeg
from shutil import copyfile

from flask import Flask, jsonify, send_file

app = Flask(__name__)

last_updated = int(time.time())


@app.route("/api/new_video/")
def get_tasks():
    toVideo()
    return jsonify(success=True)


def clear_images():
    files = glob.glob("images/0*")
    for f in files:
        os.remove(f)


@app.route("/api/get_video/")
def get_video():
    return send_file("videos/3.mp4", download_name="3.mp4")


@app.route("/api/get_thumbnail/")
def get_thumbnail():
    return send_file("images/thumbnail.png", download_name="thumbnail.png")


@app.route("/api/fetch_info/")
def fetch_info():
    global last_updated

    files = glob.glob("images/*")

    print(f"Number of files: {len(files)}")
    return jsonify(len=f"{len(files)}", last_updated=last_updated)


def toVideo():
    global last_updated
    last_updated = int(time.time())
    print(last_updated)

    try:

        (
            ffmpeg.input("./images/*.png", pattern_type="glob", framerate=30)
            .output(
                "videos/2.mp4", pix_fmt="yuv420p"
            )  # pix_fmt='yuv420p', vframes=100)
            .overwrite_output()
            .run()
        )

    except Exception as e:
        print("Could not create video 2.mp4, empty images dir?")
        print(e)
        return

    clear_images()

    if not Path.exists(Path("videos/3.mp4")):
        Path.rename(Path("videos/2.mp4"), "videos/3.mp4")

        return

    try:

        copyfile("videos/3.mp4", "videos/1.mp4")
    except Exception as e:
        print(e)

    try:

        in_file1 = ffmpeg.input("videos/1.mp4")
        in_file2 = ffmpeg.input("videos/2.mp4")
        print()
        (
            ffmpeg.concat(
                in_file1,
                in_file2,
            )
            .output("videos/3.mp4", pix_fmt="yuv420p")
            .overwrite_output()
            .run()
        )

        Path("videos/1.mp4").unlink(missing_ok=False)
        Path("videos/2.mp4").unlink(missing_ok=False)

    except Exception as e:
        print(e)
        pass

    return


if __name__ == "__main__":
    # toVideo()  # for testing

    app.run(host="0.0.0.0", debug=True)
