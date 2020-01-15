import board
import neopixel

count = 60
__pixels__ = neopixel.NeoPixel(board.D12, count, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)

def __setColor(number, color=[0,0,0]):
  __pixels__[number] = color

def show():
  __pixels__.show()

def blank(number=False):
  if number:
    __setColor(number)
  else:
    for x in range(count):
      __setColor(x)

def changeColor(color, number=False):
  if number:
    __setColor(number, color)
  else:
    for x in range(count):
      __setColor(x, color)

def changeBrightness(brightness):
  __pixels__.brightness = brightness/100
