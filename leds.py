import board
import neopixel
import cache

count = 60
previousBrightness = cache.get(cache.BRIGHTNESS)
brightness = previousBrightness if previousBrightness else 1.0
__pixels__ = neopixel.NeoPixel(board.D12, count, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB)

def __setColor__(number, color=(0,0,0)):
  __pixels__[number] = color


def __HSVtoRGB__(h, s, v):
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
  print('Turning on...')
  # Grab color from cache
  prevColor = cache.get(cache.COLOR)
  changeColor(prevColor if prevColor else (0.33,1,1))
  show()
  cache.put(cache.STATE, True)

def turnOff():
  print('Turning off...')
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
      __setColor__(x)

def changeColor(colorTuple, isHSV = False):
  rgb = __HSVtoRGB__(*colorTuple) if isHSV else colorTuple
  for x in range(count):
    __setColor__(x, rgb)
  cache.put(cache.COLOR, rgb)

def changeBrightness(brightness):
  __pixels__.brightness = (brightness / 100.0)
  cache.put(cache.BRIGHTNESS, brightness)
