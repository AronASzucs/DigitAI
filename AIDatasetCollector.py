import tkinter as tk
import tkinter.font as tkFont
import numpy
from PIL import Image
import os, os.path
from ctypes import windll

# The AI Dataset collection class
class AIDatasetCollector:

    def __init__(self, root):

        # Dark Color Palette
        self.colorhighlight = "#8cbfc2"
        self.highlight = "#FFFFFF"
        self.background = "#292929"
        self.altbackground = "#383838"
        self.activebackground = "#5e5e5e"
        self.canvas_color = "#1f1f1f"

        # Light Color Palette
        self.light_colorhighlight = "Black"
        self.light_highlight = "Black"
        self.light_background = "White"
        self.light_altbackground = "Gray"
        self.light_activebackground = "Light Gray"
        self.light_canvas_color = "White"

        self.LightOrDark = 0 # 0 = dark mode, 1 = light mode

        self.imageDimensions = 16
        self.root = root
        self.fontSize = 18
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
        windll.shcore.SetProcessDpiAwareness(1)
        self.root.geometry("512x512")
        self.root.title("Handwritten Number AI collection and model")
        self.root.resizable(False, False)
        self.root.iconbitmap("assets/Icon.ico")
        root.configure(bg = "#292929")

    def createWidgets(self):
        # Help Info Label
        self.helpLabel = tk.Label(self.root, text="r = Reset, s = Save", font=tkFont.Font(family="assets/Lexend.ttf", size=20), foreground=self.highlight, background=self.background)
        self.helpLabel.pack()

        # Configure Columns
        self.inputButtomFrame = tk.Frame(self.root, background=self.altbackground)
        for i in range(7):
            self.inputButtomFrame.columnconfigure(i, weight=1)

        # Create Buttons
        self.buttons = {}

        for i in range(10):
            button = tk.Button(self.inputButtomFrame, text=str(i), font=("Arial", self.fontSize), command=lambda t=i: self.change_number_button_color(t), background=self.altbackground, borderwidth=0, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
            button.grid(row=i // 5, column=i % 5)
            self.buttons[i] = button

        self.button_8px = tk.Button(self.inputButtomFrame, text = "8px", font=("Arial", self.fontSize), command=lambda: self.change_px_button_color(8), background=self.altbackground, borderwidth=0, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
        self.button_8px.grid(row=0, column=6)

        self.button_16px = tk.Button(self.inputButtomFrame, text = "16px", font=("Arial", self.fontSize), command=lambda: self.change_px_button_color(16), background=self.altbackground, borderwidth=0, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
        self.button_16px.grid(row=0, column=7)

        self.button_32px = tk.Button(self.inputButtomFrame, text = "32px", font=("Arial", self.fontSize), command=lambda: self.change_px_button_color(32),background=self.altbackground, borderwidth=0, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
        self.button_32px.grid(row=1, column=6)

        self.button_64px = tk.Button(self.inputButtomFrame, text = "64px", font=("Arial", self.fontSize), command=lambda: self.change_px_button_color(64),background=self.altbackground, borderwidth=0, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
        self.button_64px.grid(row=1, column=7)
            
        self.inputButtomFrame.pack()
        self.change_number_button_color(0) #sets the 0 to be highlighted
        self.change_px_button_color(16) # sets 16 to be highlighted

        self.numInDirectoryButton = tk.Label(self.root, text="Images in directory: " + str(self.image_count), font=("Arial", 10), foreground="White", background=self.background)
        self.numInDirectoryButton.pack()

        self.drawingCanvas = tk.Canvas(self.root, width=256, height=256, bg=self.canvas_color, borderwidth = 0, highlightthickness= 0, relief="sunken")
        self.drawingCanvas.pack()

        self.trainModelButton = tk.Button(self.root, text= "Train Model", borderwidth=0, font=("Arial", self.fontSize), background=self.altbackground, activebackground=self.activebackground, foreground=self.highlight, activeforeground=self.highlight)
        self.trainModelButton.pack(pady = 10)

        self.toggleLightDarkButton = tk.Button(self.root, text = "Switch to Light Mode", command =self.changeColorPalette, background=self.altbackground, activebackground=self.activebackground, foreground=self.highlight, borderwidth=0, padx=5, pady=5)
        self.toggleLightDarkButton.pack()

        self.signatureLabel = tk.Label(self.root, text="Made by Aron Szucs", font=("Lucida Calligraphy", 10), borderwidth=0, background=self.background, foreground=self.highlight)
        self.signatureLabel.pack(side="bottom")

    def canvasDraw(self, x, y):
        if (x >= 0 and y >= 0 and x <= self.imageDimensions and y <= self.imageDimensions):
            self.drawingCanvas.create_rectangle(x * (256 // self.imageDimensions), y * (256 // self.imageDimensions), (x * (256 // self.imageDimensions) + (256 // self.imageDimensions)), (y * (256 // self.imageDimensions) + (256 // self.imageDimensions)), fill = "white") 
            self.array[y,x] = 1

    def change_number_button_color(self, num):
        self.currentNum = num

        for button in self.buttons.values():
            button.config(background=self.altbackground)

        self.buttons[num].config(background = self.colorhighlight)

    def change_px_button_color(self,num):
        self.button_8px.config(background=self.altbackground)
        self.button_16px.config(background=self.altbackground)
        self.button_32px.config(background=self.altbackground)
        self.button_64px.config(background=self.altbackground)
        self.imageDimensions = num
        self.array = numpy.zeros((self.imageDimensions, self.imageDimensions))

        print(self.imageDimensions)

        if num == 8:
            self.button_8px.config(background=self.colorhighlight)
        elif num == 16:
            self.button_16px.config(background=self.colorhighlight)
        elif num == 32:
            self.button_32px.config(background=self.colorhighlight)
        elif num == 64:
            self.button_64px.config(background=self.colorhighlight)

    def changeColorPalette(self):

        if self.LightOrDark == 0:
            self.trainModelButton.configure(background=self.light_altbackground, highlightcolor=self.light_highlight)
            self.root.config(background=self.light_background)
            print("now light mode")
            self.LightOrDark = 1
        else:
            self.trainModelButton.configure(background=self.altbackground)
            self.root.config(background=self.background)
            print("now dark mode")
            self.LightOrDark = 0

    def mouseDrag(self, event):
        x, y = event.x, event.y
        self.canvasDraw(x // (256 // self.imageDimensions) , y // (256 // self.imageDimensions))
        print (str(x // (256 // self.imageDimensions)) + " " + str(y // (256 // self.imageDimensions)))

    def reset(self, event):
        self.drawingCanvas.delete("all")
        self.array = numpy.zeros((self.imageDimensions, self.imageDimensions))

    def saveImg(self, event):
        #draws image from array
        image = Image.fromarray((self.array * 255).astype(numpy.uint8))

        file_path = "dataset/" + str(self.imageDimensions) + "px/" + str(self.currentNum) + "/num" + str(self.currentNum) + "count" + str(self.image_count + 1) + ".png"

        # makes dataset/ directory if not found
        if not os.path.isdir("dataset/"):
            os.mkdir("dataset")
            print("made directory dataset/")

        # makes px directory if not found
        if not os.path.isdir("dataset/" + str(self.imageDimensions) + "px/"):
            os.mkdir("dataset/" + str(self.imageDimensions) + "px/")
            print("made directory dataset/" + str(self.imageDimensions) + "px/")

        #makes imageDim directory if not found
        if not os.path.isdir("dataset/" + str(self.imageDimensions) + "px/" + str(self.currentNum) + "/"):
            os.mkdir("dataset/" + str(self.imageDimensions) + "px/" + str(self.currentNum) + "/")
            print("made directory dataset/" + str(self.imageDimensions) + "px/" + str(self.currentNum) + "/")

        image.save(file_path)

        self.reset(self)

    def updateImagesInDirectory(self):
        file_path = "dataset/" + str(self.imageDimensions) + "px/"+ str(self.currentNum) + "/"

        # unable to find path
        if not os.path.isdir(file_path):
            self.image_count = 0
        else:
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
