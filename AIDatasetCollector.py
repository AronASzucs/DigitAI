import time
import tkinter as tk
import tkinter.font as tkFont
import numpy
from PIL import Image
import os, os.path
from ctypes import windll

# The AI Dataset collection class
class AIDatasetCollector:

    def __init__(self, root):

        self.imageDimensions = 16
        self.root = root
        self.fontSize = 20
        self.currentNum = 0
        self.image_count = 0
        self.LightOrDark = 0 # 0 = dark mode, 1 = light mode
        
        self.setupWindow()
        self.createWidgets()
        self.updateImagesInDirectory()

        self.root.bind("<r>", self.reset)
        self.root.bind("<s>", self.saveImg)
        self.drawingCanvas.bind("<B1-Motion>", self.mouseDrag)

        # define array
        self.array = numpy.zeros((self.imageDimensions, self.imageDimensions))

    def setupWindow(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.root.geometry("512x512")
        self.root.title("Handwritten Number AI collection and model")
        #self.root.resizable(False, False)
        self.root.iconbitmap("assets/Icon.ico")
        root.configure(bg = "#292929")

    def createWidgets(self):
        # Help Info Label
        self.helpLabel = tk.Label(self.root, text="r = Reset, s = Save", font=tkFont.Font(family="assets/Lexend.ttf", size=20), foreground="#FFFFFF", background="#292929")
        self.helpLabel.pack()

        # Configure Columns
        self.inputButtomFrame = tk.Frame(self.root)
        for i in range(5):
            self.inputButtomFrame.columnconfigure(i, weight=1)

        # Create Buttons
        self.buttons = {}

        for i in range(10):
            button = tk.Button(self.inputButtomFrame, text=str(i), font=("Arial", self.fontSize), command=lambda i=i: self.change_number_button_color(i), background="#383838", borderwidth=0, activebackground="#5e5e5e", foreground="White", activeforeground="White")
            button.grid(row=i // 5, column=i % 5)
            self.buttons[i] = button

        self.inputButtomFrame.pack()

        self.numInDirectoryButton = tk.Label(self.root, text="Images in directory: " + str(self.image_count), font=("Arial", 10), foreground="White", background="#292929")
        self.numInDirectoryButton.pack()

        self.drawingCanvas = tk.Canvas(self.root, width=256, height=256, bg="#1f1f1f", borderwidth = 0, highlightthickness= 0, relief="sunken")
        self.drawingCanvas.pack()

        self.trainModelButton = tk.Button(self.root, text= "Train Model", borderwidth=0, font=("Arial", self.fontSize), background="#383838", activebackground="#5e5e5e", foreground="White", activeforeground="White")
        self.trainModelButton.pack(pady = 10)

        self.toggleLightDarkButton = tk.Button(self.root, text = "Switch to Light Mode", background="#383838", activebackground="#5e5e5e", foreground="White", borderwidth=0, padx=5, pady=5)
        self.toggleLightDarkButton.pack()

        self.signatureLabel = tk.Label(self.root, text="Made by Aron Szucs", font=("Lucida Calligraphy", 10), borderwidth=0)
        self.signatureLabel.pack(side="bottom")

    def canvasDraw(self, x, y):
        if (x >= 0 and y >= 0 and x <= self.imageDimensions and y <= self.imageDimensions):
            self.drawingCanvas.create_rectangle(x * (256 // self.imageDimensions), y * (256 // self.imageDimensions), (x * (256 // self.imageDimensions) + (256 // self.imageDimensions)), (y * (256 // self.imageDimensions) + (256 // self.imageDimensions)), fill = "black") 
            self.array[y,x] = 1

    def change_number_button_color(self, num):
        self.currentNum = num

        for button in self.buttons.values():
            button.config(background="#383838")

        self.buttons[num].config(background = "#8cbfc2")

    def mouseDrag(self, event):
        x, y = event.x, event.y
        self.canvasDraw(x // (256 // self.imageDimensions) , y // (256 // self.imageDimensions))
        print (str(x // (256 // self.imageDimensions)) + " " + str(y // (256 // self.imageDimensions)))

    def reset(self, event):
        time.sleep(0.1)
        self.drawingCanvas.delete("all")
        self.array = numpy.zeros((self.imageDimensions, self.imageDimensions))

    def saveImg(self, event):
        image = Image.fromarray((self.array * 255).astype(numpy.uint8))

        file_path = "dataset/" + str(self.currentNum) + "/num" + str(self.currentNum) + "count" + str(self.image_count) + ".png"
        image.save(file_path)

        self.reset(self)

    def updateImagesInDirectory(self):
        file_path = "dataset/" + str(self.currentNum) + "/"

        # finds the number of files in a given directory
        # found on stack ovecanvasrflow
        self.image_count = len(os.listdir(file_path))

        self.numInDirectoryButton.config(text="Images in directory: " + str(self.image_count))

        self.root.after(100, self.updateImagesInDirectory)

    def trainModel():
        print("TBD")

# create main window
root = tk.Tk()

# instantiate the app
app = AIDatasetCollector(root)

# start the main loop
root.mainloop()
