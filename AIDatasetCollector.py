import time
import tkinter as tk
import numpy
from PIL import Image
import os, os.path

# The AI Dataset collection class
class AIDatasetCollector:

    def __init__(self, root):

        self.imageDimensions = 16
        self.root = root
        self.fontSize = 20
        self.currentNum = 0
        self.image_count = 0
        
        self.setupWindow()
        self.createWidgets()
        self.updateImagesInDirectory()

        self.root.bind("<r>", self.reset)
        self.root.bind("<s>", self.saveImg)
        self.drawingCanvas.bind("<B1-Motion>", self.mouseDrag)

        # define array
        self.array = numpy.zeros((self.imageDimensions, self.imageDimensions))

    def setupWindow(self):
        self.root.geometry("512x512")
        self.root.title("AI Dataset Collector Program")
        self.root.resizable(False, False)

    def createWidgets(self):
        # Help Info Label
        self.helpLabel = tk.Label(self.root, text="r = reset, s = save", font=('Arial', self.fontSize))
        self.helpLabel.pack()
        
        # Current Number Label
        self.currentNumLabel = tk.Label(self.root, text="Current number: " + str(self.currentNum), font=('Arial', 10))
        self.currentNumLabel.pack()

        # Configure Columns
        self.inputButtomFrame = tk.Frame(self.root)
        for i in range(5):
            self.inputButtomFrame.columnconfigure(i, weight=1)

        # Create Buttons
        for i in range(10):
            button = tk.Button(self.inputButtomFrame, text=str(i), font=("Arial", self.fontSize), command=lambda i=i: self.setCurrentNum(i))
            button.grid(row=i // 5, column=i % 5)

        self.inputButtomFrame.pack()

        self.numInDirectoryButton = tk.Label(self.root, text="Images in directory: " + str(self.image_count), font=("Arial", 10))
        self.numInDirectoryButton.pack()

        self.drawingCanvas = tk.Canvas(self.root, width=256, height=256, bg="white", borderwidth = 0, highlightthickness= 0)
        self.drawingCanvas.pack()

        self.signatureLabel = tk.Label(self.root, text="Made by Aron Szucs", font=("Lucida Calligraphy", 10))
        self.signatureLabel.pack(side="bottom")


    def setCurrentNum(self, num):
        self.currentNum = num
        # Update the current number label
        self.currentNumLabel.config(text="Current number: " + str(self.currentNum))

    def canvasDraw(self, x, y):
        if (x >= 0 and y >= 0 and x <= self.imageDimensions and y <= self.imageDimensions):
            self.drawingCanvas.create_rectangle(x * (256 // self.imageDimensions), y * (256 // self.imageDimensions), (x * (256 // self.imageDimensions) + (256 // self.imageDimensions)), (y * (256 // self.imageDimensions) + (256 // self.imageDimensions)), fill = "black") 
            self.array[y,x] = 1

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

        # idk why this works I found it on stack overflow
        self.image_count = len(os.listdir(file_path))

        self.numInDirectoryButton.config(text="Images in directory: " + str(self.image_count))

        self.root.after(100, self.updateImagesInDirectory)

# create main window
root = tk.Tk()

# instantiate the app
app = AIDatasetCollector(root)

# start the main loop
root.mainloop()
