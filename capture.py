import time
from PIL import Image
import requests
from io import BytesIO
import glob
from datetime import datetime
import cv2
import numpy as np
import numpy.typing as npt


def getTime() -> str:
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def getFrame() -> npt.NDArray:
    cap: cv2.VideoCapture = cv2.VideoCapture(url)
    ret, frame = cap.read()
    cap.release()
    return ret, frame


url = "http://192.168.1.165:8081"
img_path = img_path = "images/" + "000000.png"  # init name
freq_seconds = 60

while True:
    ret, frame = getFrame()
    if ret == True:
        cv2.fastNlMeansDenoisingColored(frame, frame, 10, 10, 7, 21)
        cv2.putText(
            frame,
            str(datetime.now().strftime("%Y/%m/%d, %H:%M:%S")),
            (20, 40),
            2,
            0.8,
            (255, 255, 2),
        )

        currentImages = glob.glob("images/0*.png")
        if len(currentImages) > 0:
            currentImages.sort()
            currentImages[-1] = currentImages[-1].replace("//", "\\")
            count = int(currentImages[-1].replace("images/", "").replace(".png", ""))
            count = count + 1
            img_path = "images/" + str(count).zfill(6) + ".png"

        print(getTime(), img_path)
        cv2.imwrite(img_path, frame)
    else:
        print("Failed to get frame")

    time.sleep(freq_seconds)
