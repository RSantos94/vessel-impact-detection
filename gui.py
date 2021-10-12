import tkinter as tk
import cv2
from PIL import Image, ImageTk

class MainWindow():
    def __init__(self, window, cap):


        self.window = window
        self.cap = cap
        self.width = 960
        self.height = 540
        self.interval = 20 # Interval in ms to get the latest frame
        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)

        BS_KNN = cv2.createBackgroundSubtractorKNN()
        # Update image on canvas
        while cap.isOpened():
            success, self.img = cap.read()

            self.fgKnn = BS_KNN.apply(self.img)

            self.fgKnnRs = cv2.resize(self.fgKnn, (960, 540))

            imgS = cv2.resize(self.img, (960, 540))

            self.fg = cv2.copyTo(imgS,self.fgKnnRs)

            self.update_image()
    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)
if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root, cv2.VideoCapture('video_files/forgroundKNN.avi'))
    root.mainloop()