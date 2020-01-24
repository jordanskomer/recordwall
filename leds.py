import board
import neopixel
import cache

count = 60
previousBrightness = cache.get(cache.BRIGHTNESS)
brightness = previousBrightness if previousBrightness else 1.0
__pixels__ = neopixel.NeoPixel(board.D12, count, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB)

def __setColor(number, color=(0,0,0)):
  __pixels__[number] = color



def hsv_to_rgb(h, s, v):
  if s == 0.0: v*=255; return (int(v), int(v), int(v))
  i = int(h*6) # XXX assume int() truncates!
  f = (h*6)-i; p,q,t = 255*(v*(1-s)), 255*(v*(1-s*f)), 255*(v*(1-s*(1-f))); v*=255; i%=6
  if i == 0: return (int(v), int(t), int(p))
  if i == 1: return (int(q), int(v), int(p))
  if i == 2: return (int(p), int(v), int(t))
  if i == 3: return (int(p), int(q), int(v))
  if i == 4: return (int(t), int(p), int(v))
  if i == 5: return (int(v), int(p), int(q))

def show():
  __pixels__.show()

def turnOn():
  prevColor = cache.get(cache.COLOR)
  # @todo convert to spectrum
  changeColor((255,0,0))
  show()
  cache.put(cache.STATE, True)

def turnOff():
  blank()
  show()
  cache.put(cache.STATE, False)

def isOn():
  return cache.get(cache.STATE)

def blank(number=False):
  if number:
    __setColor(number)
  else:
    for x in range(count):
      __setColor(x)

def changeColor(rgb):
  for x in range(count):
    __setColor(x, rgb)
  cache.put(cache.COLOR, rgb)

def changeBrightness(brightness):
  __pixels__.brightness = (brightness / 100.0)
  cache.put(cache.BRIGHTNESS, brightness)
