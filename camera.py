import tkinter as tk
import cv2
from threading import Thread, Lock
import time
import numpy as np

cameras = {0: None, 1: None}
selected_cam = None
camera_active = False
program_running = True
lock = Lock()
capture_thread = None

def toggle_camera(camNumber):
    global camera_active, selected_cam

    with lock:
        if selected_cam == camNumber and camera_active:
            camera_active = False
        else:
            selected_cam = camNumber
            if not camera_active:
                camera_active = True
                print(f"Camera {selected_cam} activated.")

def initialize_cameras():
    global cameras
    for idx in [1, 0]:  # Initialize cameras in a loop
        cameras[idx] = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cameras[idx].isOpened():
            cameras[idx].set(cv2.CAP_PROP_FRAME_WIDTH, 720)
            cameras[idx].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        else:
            print(f"Error: Could not open webcam {idx}.")

def webcam_capture():
    global selected_cam, camera_active, program_running

    while program_running:
        if camera_active:
            ret, frame = cameras[selected_cam].read()
            if not ret:
                print(f"Error: Could not read frame from webcam {selected_cam}.")
                continue
            cv2.imshow('Webcam Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            if cv2.getWindowProperty('Webcam Feed', cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow('Webcam Feed')
            time.sleep(0.1)  # Sleep only when no camera is active

    cv2.destroyAllWindows()
    for cam in cameras.values():
        cam.release()

def start_webcam_capture_thread():
    global capture_thread
    capture_thread = Thread(target=webcam_capture, daemon=True)
    capture_thread.start()

def on_button_click(camNumber):
    toggle_camera(camNumber)

def close_program():
    global program_running, root
    program_running = False
    root.destroy()

if __name__ == "__main__":
    initialize_cameras()
    start_webcam_capture_thread()

    root = tk.Tk()
    root.title("Webcam Activation")

    left_button = tk.Button(root, text="Left Camera", command=lambda: on_button_click(1))
    right_button = tk.Button(root, text="Right Camera", command=lambda: on_button_click(0))
    # close_button = tk.Button(root, text="Close Program", command=close_program)

    left_button.pack(side=tk.LEFT)
    right_button.pack(side=tk.RIGHT)
    # close_button.pack(side=tk.BOTTOM)

    root.mainloop()

    if capture_thread.is_alive():
        capture_thread.join()
