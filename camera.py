import tkinter as tk
import cv2
from threading import Thread
import time

# Global variables
cameras = {0: None, 1: None}
selected_cam = None
stop_threads = False

def initialize_cameras():
    global cameras
    # Initialize both cameras
    cameras[1] = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cameras[0] = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    for cam_number, cam in cameras.items():
        if not cam.isOpened():
            print(f"Error: Could not open webcam {cam_number}.")
        else:
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def webcam_capture():
    global selected_cam, stop_threads

    while not stop_threads:
        if selected_cam is not None:
            ret, frame = cameras[selected_cam].read()
            if not ret:
                print(f"Error: Could not read frame from webcam {selected_cam}.")
                break

            cv2.imshow(f'Webcam Feed', frame)

            # Break the display loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        else:
            # Sleep briefly to prevent this loop from consuming too much CPU when no camera is selected
            time.sleep(0.1)

def on_button_click(camNumber):
    global selected_cam
    selected_cam = camNumber

# Initialize camera resources
initialize_cameras()

# Start the webcam capture thread
capture_thread = Thread(target=webcam_capture, daemon=True)
capture_thread.start()

# Create the main window
root = tk.Tk()
root.title("Webcam Activation")

# Create and place buttons using lambda to defer the execution
left_button = tk.Button(root, text="Left Camera", command=lambda: on_button_click(1))
right_button = tk.Button(root, text="Right Camera", command=lambda: on_button_click(0))

left_button.pack(side=tk.LEFT)
right_button.pack(side=tk.RIGHT)

# Start the GUI event loop
root.mainloop()

# Cleanup
stop_threads = True
capture_thread.join()
for cam in cameras.values():
    cam.release()
cv2.destroyAllWindows()
