import tkinter as tk 

fontSize = 20
currentNum = 0
imagecount = 0

def WindowSetup():
        # creates window
    root = tk.Tk()

    # basic window info
    root.geometry("512x512")
    root.title("AI Dataset Collection")
    root.resizable(False, False)

    # label 
    helpLabel = tk.Label(root, text = "r = reset, s = save", font = ('Arial', fontSize))
    helpLabel.pack()

    currentNumLabel = tk.Label(root, text = "Current number: " + str(currentNum), font = ('Arial', 10))
    currentNumLabel.pack()

    # input buttom frame 
    inputButtomFrame = tk.Frame(root)
    inputButtomFrame.columnconfigure(0,weight=1) 
    inputButtomFrame.columnconfigure(1,weight=1)
    inputButtomFrame.columnconfigure(2,weight=1)
    inputButtomFrame.columnconfigure(3,weight=1)
    inputButtomFrame.columnconfigure(4,weight=1)

    # buttons
    button0 = tk.Button(inputButtomFrame, text = "0", font = ("Arial", fontSize), command= lambda: setCurrentNum(0))
    button0.grid(row = 0, column= 0)

    button1 = tk.Button(inputButtomFrame, text = "1", font = ("Arial", fontSize), command= lambda: setCurrentNum(1))
    button1.grid(row = 0, column= 1)

    button2 = tk.Button(inputButtomFrame, text = "2", font = ("Arial", fontSize), command= lambda: setCurrentNum(2))
    button2.grid(row = 0, column= 2)

    button3 = tk.Button(inputButtomFrame, text = "3", font = ("Arial", fontSize), command= lambda: setCurrentNum(3))
    button3.grid(row = 0, column= 3)

    button4 = tk.Button(inputButtomFrame, text = "4", font = ("Arial", fontSize), command= lambda: setCurrentNum(4))
    button4.grid(row = 0, column= 4)

    button5 = tk.Button(inputButtomFrame, text = "5", font = ("Arial", fontSize), command= lambda: setCurrentNum(5))
    button5.grid(row = 1, column= 0)

    button6 = tk.Button(inputButtomFrame, text = "6", font = ("Arial", fontSize), command= lambda: setCurrentNum(6))
    button6.grid(row = 1, column= 1)

    button7 = tk.Button(inputButtomFrame, text = "7", font = ("Arial", fontSize), command= lambda: setCurrentNum(7))
    button7.grid(row = 1, column= 2)

    button8 = tk.Button(inputButtomFrame, text = "8", font = ("Arial", fontSize), command= lambda: setCurrentNum(8))
    button8.grid(row = 1, column= 3)

    button9 = tk.Button(inputButtomFrame, text = "9", font = ("Arial", fontSize), command= lambda: setCurrentNum(9))
    button9.grid(row = 1, column= 4)

    inputButtomFrame.pack()

    numInDirectoryButton = tk.Label(root, text = "Images in directory: "+ str(imagecount), font = ("Arial", 10))
    numInDirectoryButton.pack()

    drawingCanvas = tk.Canvas(root, width = 256, height= 256, bg = "white", highlightbackground= "black")
    drawingCanvas.pack()

    signatureLabel = tk.Label(root, text = "Made by Aron Szucs", font = ("Lucida Calligraphy", 10), )
    signatureLabel.pack(side = "bottom")
    
    root.mainloop()
    
def setCurrentNum(num):
    global currentNum
    currentNum = num

WindowSetup()
