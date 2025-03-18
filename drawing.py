import tkinter
import numpy
from PIL import Image

window = tkinter.Tk()

currentNum = 5

# sets up the main array
array = numpy.zeros((16, 16))
array[10,10] = 5
print(array)

img = Image.fromarray(1 - array)
img.show()

# draws it 
window.mainloop()