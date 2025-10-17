#!/usr/bin/env python3

import cv2
import depthai as dai
import os
import time
from datetime import datetime

# === USER CONFIG ===
ROTATE_180 = False     # Set to True if camera is upside down
TARGET_FPS = 10       # Desired save rate (frames per second)
# ===================

# Create a new folder for this run
RUN_DIR = "./captures/" + datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(RUN_DIR, exist_ok=True)
print(f"[INFO] Saving images to: {RUN_DIR}")

# Create pipeline
with dai.Pipeline() as pipeline:
    # Define source and output
    cam = pipeline.create(dai.node.Camera).build()
    videoQueue = cam.requestOutput((1280, 720)).createOutputQueue()  # use 720p for better aspect

    # Connect to device and start pipeline
    pipeline.start()

    # FPS limiter
    target_frame_time = 1.0 / TARGET_FPS
    last_time = 0

    while pipeline.isRunning():
        videoIn = videoQueue.get()
        assert isinstance(videoIn, dai.ImgFrame)
        frame = videoIn.getCvFrame()

        # Optional rotation
        if ROTATE_180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Show preview
        cv2.imshow("video", frame)

        # FPS limiter for saving
        now = time.time()
        if now - last_time >= target_frame_time:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(RUN_DIR, f"{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            last_time = now

        if cv2.waitKey(1) == ord("q"):
            break
