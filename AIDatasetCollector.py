import tkinter as tk
from tkinter import filedialog
import numpy
import time
import threading
from PIL import Image
import os, os.path
from ctypes import windll
from Model import NumberModel # From Model.py

# The AI Dataset collection class
class AIDatasetCollector:

    def __init__(self, root):

        # Dark Color Palette
        self.color_highlight = "#8cbfc2"
        self.highlight = "#FFFFFF"
        self.background = "#292929"
        self.alt_background = "#383838"
        self.active_background = "#5e5e5e"
        self.canvas_color = "#1f1f1f"
        # Light Color Palette
        self.light_color_highlight = "#6fa688"
        self.light_highlight = "Black"
        self.light_background = "White"
        self.light_alt_background = "Light Gray"
        self.light_active_background = "Light Gray"
        self.light_canvas_color = "White"
        self.light_or_dark = 0 # 0 = dark mode, 1 = light mode

        self.screen_height = root.winfo_screenheight()
        self.screen_scalar = (self.screen_height / 1080) * 2
        self.canvas_size = int(256 * self.screen_scalar)

        self.image_dimensions = 16
        self.root = root
        self.font_size = int(18 * self.screen_scalar)
        self.font_size_small = int(10 * self.screen_scalar)
        self.set_font = "Segoe UI"
        self.current_num = 0
        self.image_count = 0
        self.model_current_mode = 0 # 0 = non active, 8 = 8px, 16 = 16px, 32 = 32px, 64 = 64px, if image_dimensions =/= model_current_mode, thats bad.
        
        self.setup_window()
        self.create_widgets()
        self.update_images_in_directory()

        self.root.bind("<r>", self.reset)
        self.root.bind("<s>", self.save_img)
        self.drawing_canvas.bind("<B1-Motion>", self.mouse_drag)

        # define array
        self.array = numpy.zeros((self.image_dimensions, self.image_dimensions))

        # create model class
        self.model = NumberModel()

    def setup_window(self):
        windll.shcore.SetProcessDpiAwareness(1)
        self.window_size = int(600 * self.screen_scalar)
        self.root.geometry(str(self.window_size) + "x" + str(self.window_size))
        self.root.title("Handwritten Number AI collection and model")
        #self.root.resizable(False, False)
        self.root.iconbitmap("assets/Icon.ico")
        root.configure(bg = self.background)

    def create_widgets(self):
        # Help Info Label
        self.help_label = tk.Label(self.root, text="r = Reset Canvas, s = Save Img", font=(self.set_font, self.font_size), foreground=self.highlight, background=self.background)
        self.help_label.pack()

        # Configure Columns
        self.input_buttom_frame = tk.Frame(self.root, background=self.background)
        for i in range(7):
            self.input_buttom_frame.columnconfigure(i, weight=1)

        # Create Buttons
        self.buttons = {}

        for i in range(10):
            button = tk.Button(self.input_buttom_frame, text=str(i), font=(self.set_font, self.font_size), command=lambda t=i: self.change_number_button_color(t), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
            button.grid(row=i // 5, column=i % 5)
            self.buttons[i] = button

        self.button_8px = tk.Button(self.input_buttom_frame, text = " 8px ", font=(self.set_font, self.font_size), command=lambda: self.change_img_size(8), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_8px.grid(padx=(20,0), row=0, column=6)

        self.button_16px = tk.Button(self.input_buttom_frame, text = "16px", font=(self.set_font, self.font_size), command=lambda: self.change_img_size(16), background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_16px.grid(row=0, column=7)

        self.button_32px = tk.Button(self.input_buttom_frame, text = "32px", font=(self.set_font, self.font_size), command=lambda: self.change_img_size(32),background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_32px.grid(padx=(20,0), row=1, column=6)

        self.button_64px = tk.Button(self.input_buttom_frame, text = "64px", font=(self.set_font, self.font_size), command=lambda: self.change_img_size(64),background=self.alt_background, borderwidth=0, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.button_64px.grid(row=1, column=7)
            
        self.input_buttom_frame.pack()
        self.change_number_button_color(0) #sets the 0 to be highlighted

        # Images in directory label
        self.num_in_directory_label = tk.Label(self.root, text="Images in directory: " + str(self.image_count), font=(self.set_font, self.font_size_small), foreground="White", background=self.background)
        self.num_in_directory_label.pack(pady = 10)

        # Drawing Canvas
        self.drawing_canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg=self.canvas_color, borderwidth = 0, highlightthickness= 0, relief="sunken")
        self.drawing_canvas.pack()

        # Predicted Number Label
        self.prediction_label = tk.Label(self.root, text = "Load/Train a Model to Predict Numbers", font=(self.set_font, self.font_size), foreground=self.highlight, background=self.background)
        self.prediction_label.pack()

        # Bottom button frame w/ Train Model, Save Model, and Load Model
        self.bottom_button_frame = tk.Frame(self.root, background=self.background)
        for i in range (3):
            self.bottom_button_frame.columnconfigure(i,weight =1)

        self.train_model_button = tk.Button(self.bottom_button_frame, text= "Train Model", command=self.train_model, borderwidth=0, font=(self.set_font, self.font_size), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.train_model_button.grid(row = 0, column=0,padx=5)

        self.save_model_button = tk.Button(self.bottom_button_frame, text= "Save Model", command=self.save_model, borderwidth=0, font=(self.set_font, self.font_size), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.save_model_button.grid(row = 0, column=1, padx=5)

        self.load_model_button = tk.Button(self.bottom_button_frame, text= "Load Model", command=self.load_model, borderwidth=0, font=(self.set_font, self.font_size), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight)
        self.load_model_button.grid(row = 0, column=2, padx=5)

        self.bottom_button_frame.pack(pady=20)

        self.toggle_light_dark_button = tk.Button(self.root, text = "Switch to Light Mode", command=self.change_color_palette, padx=5, pady=5, font=(self.set_font, 10), background=self.alt_background, activebackground=self.active_background, foreground=self.highlight, activeforeground=self.highlight, borderwidth=0)
        self.toggle_light_dark_button.pack()

        self.signature_label = tk.Label(self.root, text="Made by Aron Szucs", font=(self.set_font, 10), borderwidth=0, background=self.background, foreground=self.color_highlight)
        self.signature_label.pack(side="bottom")

        self.message_label = tk.Label(self.root, text = "ERROR!", foreground=self.color_highlight, font=(self.set_font, self.font_size), background="Black")

        self.change_img_size(16) # sets 16 to be highlighted

    def canvas_draw(self, x, y):
        if (x >= 0 and y >= 0 and x <= self.image_dimensions and y <= self.image_dimensions):
            if self.array[y,x] == 0:
                self.drawing_canvas.create_rectangle(x * (self.canvas_size // self.image_dimensions),
                                                     y * (self.canvas_size // self.image_dimensions),
                                                     (x * (self.canvas_size // self.image_dimensions) + (self.canvas_size // self.image_dimensions)),
                                                     (y * (self.canvas_size // self.image_dimensions) + (self.canvas_size // self.image_dimensions)),
                                                     fill = "white") 
                self.array[y,x] = 1

                # Update prediction if model is loaded
                if self.model_current_mode != 0:
                    self.update_prediction()

    def change_number_button_color(self, num):
        self.current_num = num

        for button in self.buttons.values():
            button.config(background=self.alt_background, foreground=self.highlight) if self.light_or_dark == 0 else button.config(background=self.light_alt_background, foreground=self.light_highlight)

        self.buttons[num].config(background = self.color_highlight) if self.light_or_dark == 0 else self.buttons[num].config(background = self.light_color_highlight)

    def change_img_size(self,num): #also chhanges the color of the img size buttons
        self.button_8px.config(background=self.alt_background, foreground=self.highlight) if self.light_or_dark == 0 else self.button_8px.config(background=self.light_alt_background, foreground=self.light_highlight)
        self.button_16px.config(background=self.alt_background, foreground=self.highlight) if self.light_or_dark == 0 else self.button_16px.config(background=self.light_alt_background, foreground=self.light_highlight)
        self.button_32px.config(background=self.alt_background, foreground=self.highlight) if self.light_or_dark == 0 else self.button_32px.config(background=self.light_alt_background, foreground=self.light_highlight)
        self.button_64px.config(background=self.alt_background, foreground=self.highlight) if self.light_or_dark == 0 else self.button_64px.config(background=self.light_alt_background, foreground=self.light_highlight)
        self.image_dimensions = num
        self.reset(self)

        print(self.image_dimensions)

        if num == 8:
            self.button_8px.config(background=self.color_highlight) if self.light_or_dark == 0 else self.button_8px.config(background=self.light_color_highlight)
        elif num == 16:
            self.button_16px.config(background=self.color_highlight) if self.light_or_dark == 0 else self.button_16px.config(background=self.light_color_highlight)
        elif num == 32:
            self.button_32px.config(background=self.color_highlight) if self.light_or_dark == 0 else self.button_32px.config(background=self.light_color_highlight)
        elif num == 64:
            self.button_64px.config(background=self.color_highlight) if self.light_or_dark == 0 else self.button_64px.config(background=self.light_color_highlight)

    def change_color_palette(self):
        if self.light_or_dark == 0: # in dark mode
            self.light_or_dark = 1
            self.train_model_button.configure(background=self.light_alt_background, foreground=self.light_highlight)
            self.load_model_button.configure(background=self.light_alt_background, foreground=self.light_highlight)
            self.save_model_button.configure(background=self.light_alt_background, foreground=self.light_highlight)
            self.bottom_button_frame.configure(background=self.light_background)
            self.signature_label.configure(background=self.light_background, foreground=self.light_highlight)
            self.toggle_light_dark_button.configure(background=self.light_alt_background, foreground=self.light_highlight, text = "Switch to Dark Mode")
            self.help_label.configure(background=self.light_background, foreground=self.light_highlight)
            self.num_in_directory_label.configure(background=self.light_background, foreground=self.light_highlight)
            self.input_buttom_frame.configure(background=self.light_background)

            for btn in self.buttons:
                self.buttons[btn].configure(background=self.light_alt_background, foreground=self.light_highlight)

            self.change_img_size(self.image_dimensions)
            self.change_number_button_color(self.current_num)

            self.root.config(background=self.light_background)
            print("now light mode")
            
        else: # in light mode
            self.light_or_dark = 0
            self.train_model_button.configure(background=self.alt_background, foreground=self.highlight)
            self.load_model_button.configure(background=self.alt_background, foreground=self.highlight)
            self.save_model_button.configure(background=self.alt_background, foreground=self.highlight)
            self.bottom_button_frame.configure(background=self.background)
            self.signature_label.configure(background=self.background, foreground=self.color_highlight)
            self.toggle_light_dark_button.configure(background=self.alt_background, foreground=self.highlight, text = "Switch to Light Mode")
            self.help_label.configure(background=self.background, foreground=self.highlight)
            self.num_in_directory_label.configure(background=self.background, foreground=self.highlight)
            self.input_buttom_frame.configure(background=self.background)

            self.change_img_size(self.image_dimensions)
            self.change_number_button_color(self.current_num)

            self.root.config(background=self.background)
            print("now dark mode")

    def show_error(self, error_msg):
        self.message_label.configure(foreground="Pink", text=error_msg)
        self.message_label.place(x=300, y=300, anchor="center")
        self.message_label.after(2000, self.message_label.place_forget) #2000ms = 2s

    def update_prediction(self):
        t1 = threading.Thread(target=lambda: self.prediction_label.configure(text="Predicted number: " + str(self.model.predict_num(self.array))))
        t1.start()

    def mouse_drag(self, event):
        x, y = event.x, event.y
        t2 = threading.Thread(target=self.canvas_draw(x // (self.canvas_size // self.image_dimensions) , y // (self.canvas_size // self.image_dimensions)))
        t2.start()
        
    def reset(self, event):
        self.drawing_canvas.delete("all")
        self.array = numpy.zeros((self.image_dimensions, self.image_dimensions))

    def save_img(self, event):
        #draws image from array
        image = Image.fromarray((self.array * 255).astype(numpy.uint8))

        file_path = "dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/num" + str(self.current_num) + "count" + str(self.image_count + 1) + ".png"

        # makes dataset/ directory if not found
        if not os.path.isdir("dataset/"):
            os.mkdir("dataset")
            print("made directory dataset/")

        # makes px directory if not found
        if not os.path.isdir("dataset/" + str(self.image_dimensions) + "px/"):
            os.mkdir("dataset/" + str(self.image_dimensions) + "px/")
            print("made directory dataset/" + str(self.image_dimensions) + "px/")

        #makes imageDim directory if not found
        if not os.path.isdir("dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/"):
            os.mkdir("dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/")
            print("made directory dataset/" + str(self.image_dimensions) + "px/" + str(self.current_num) + "/")

        image.save(file_path)

        self.reset(self)

    def update_images_in_directory(self):
        file_path = "dataset/" + str(self.image_dimensions) + "px/"+ str(self.current_num) + "/"

        # unable to find path
        if not os.path.isdir(file_path):
            self.image_count = 0
        else:
            # finds the number of files in a given directory
            self.image_count = len(os.listdir(file_path))

        self.num_in_directory_label.config(text="Images in directory: " + str(self.image_count))

        self.root.after(10, self.update_images_in_directory)

    def train_model(self):
        self.model.train_model(self.image_dimensions, self)
        self.model_current_mode = self.image_dimensions
        
    def load_model(self):
        self.show_error()
        # load file
        filepath = filedialog.askopenfilename(filetypes=[(".keras", "*.keras")])
        self.model.load_model(filepath)

    def save_model(self):
        print("saved model")




# create main window
root = tk.Tk()

# instantiate the  
app = AIDatasetCollector(root)

# start the main loop
root.mainloop()

'''
    ___                        _____                      
   /   |  _________  ____     / ___/____  __  ____________
  / /| | / ___/ __ \/ __ \    \__ \/_  / / / / / ___/ ___/
 / ___ |/ /  / /_/ / / / /   ___/ / / /_/ /_/ / /__(__  ) 
/_/  |_/_/   \____/_/ /_/   /____/ /___/\__,_/\___/____/  
                                                          
'''