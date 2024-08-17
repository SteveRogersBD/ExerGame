import tkinter as tk
from PIL import Image, ImageTk
from ImgeProcess import ImageProcess as IP
import cv2 as cv
import threading


frame_width=250
frame_height=250
def update_frame():
    global frame, running
    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.resize(frame, (frame_width, frame_height))
        result_frame=hand_det.process_image(frame)

        # Convert the frame to a PIL Image
        frame_pil = Image.fromarray(result_frame)
        frame_tk = ImageTk.PhotoImage(frame_pil)

        # Update the label with the new frame
        cam_label.configure(image=frame_tk)
        cam_label.image = frame_tk

        # Allow the GUI to update
        main_window.update_idletasks()

def startWebCam():
    global cap, running
    running = True
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open camera!")
        return

    # Start the thread to update frames
    threading.Thread(target=update_frame, daemon=True).start()

def on_close():
    global running
    running = False
    cap.release()
    main_window.destroy()

height, width = 600, 1200
main_window = tk.Tk()
main_window.title("Exergame")
main_window.geometry(f"{width}x{height}")

# Creating and adding the bg image
bg_image = Image.open('background.jpeg')
bg_image = bg_image.resize((width, height), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

main_canvas = tk.Canvas(main_window, width=width, height=height)
main_canvas.pack(fill="both", expand=True)

main_canvas.create_image((0, 0), image=bg_image, anchor="nw")

# Adding the welcome text in the main canvas
welcome_text = tk.Label(main_window,
                        text="Welcome to Exergame",
                        font=("Helvetica", 20),
                        bg="blue",
                        fg="red",
                        padx=20,
                        pady=20)
main_canvas.create_window((width // 2, height // 2), window=welcome_text)

# Adding the clap text in the main canvas
clap_text = tk.Label(main_window,
                     text='Clap to get started',
                     font=("Helvetica", 20),
                     bg="red",
                     fg="blue",
                     padx=20,
                     pady=20)
main_canvas.create_window((width // 2, height // 2 + 200), window=clap_text)

# Creating a label for the webcam video
cam_label = tk.Label(main_window)
main_canvas.create_window(0, 0, anchor="nw", window=cam_label)

# Create objects of image process class
hand_det = IP(0.5, 0.5)

# Start the webcam
startWebCam()

# Ensure the webcam thread stops when the window is closed
main_window.protocol("WM_DELETE_WINDOW", on_close)

main_window.mainloop()
