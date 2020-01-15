import leds
import random
import time
import math
from threading import Thread

class Looper(Thread):
  __stop__ = False

  def __init__(self, method):
    Thread.__init__(self)
    self.Method = method

  def run(self):
    while True:
      print('%s | Running Thread for %s' % (self.getName(), self.Method))
      self.Method()
      if self.__stop__:
        break

  def stop(self):
    print('%s | Stopping Thread for %s' % (self.getName(), self.Method))
    self.__stop__ = True


THREAD = False

class Handler(object):
  def __invalid(self):
    print("No method for %s" % self.method_name)

  def __colorsBetween(self, color1, color2, steps=200):
    colors = []
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    rd, gd, bd = (r2 - r1)/steps, (g2 - g1)/steps, (b2 - b1)/steps

    for step in range(steps):
      r1 += rd
      g1 += gd
      b1 += bd
      colors.append((int(r1), int(g1), int(b1)))

    return colors

  def __fadeColors(self, currentColor, targetColor):
    print('Fade from %s to %s' % (currentColor, targetColor))
    colors = self.__colorsBetween(currentColor, targetColor, 240)
    colors.insert(0, currentColor)
    colors.append(targetColor)
    for color in colors:
      print(color)
      leds.changeColor(color)
      leds.show()
      time.sleep(int(self.data['speed']) / 6000)

  def __init__(self, method_name, data):
    global THREAD
    self.data = data
    self.method_name = method_name
    method = getattr(self, method_name, self.__invalid)
    print('__init__ - %s - %s' % (data, THREAD))

    if (data['change'] is not True and data['loop'] and THREAD is False):
      print("Loop Handler called")
      THREAD = Looper(method)
      THREAD.start()
    elif (data['change'] is not True and data['loop'] is not True):
      print("Singular Handler called")
      if (THREAD):
        THREAD.stop()
        THREAD = False
      return method()

  def color(self):
    leds.changeColor([int(self.data['g']), int(self.data['r']), int(self.data['b'])])
    leds.show()

  def off(self):
    leds.blank()
    leds.show()

  def change(self):
    leds.changeBrightness(int(self.data['brightness']))

  def random(self):
    for i in range(leds.count):
      color = self.data['colors'][random.randint(0, (len(self.data['colors']) - 1))]
      leds.changeColor((int(color[0]), int(color[1]), int(color[2])), i)
    leds.show()

  def fade(self):
    colors = self.data['colors']
    if len(colors) == 1:
      colors.append((0,0,0))

    for i in range(len(colors)):
      next_index = i+1 if len(colors) != i+1 else 0
      self.__fadeColors(colors[i], colors[next_index])


  # def star_fade(self):
  #   blue = (0,0,255)
  #   green = (0,0,0)
  #   self.fade(blue, green)
  #   # self.fade(green, blue)
  #   for i in range(leds.COUNT):
  #     if random.randint(0, 5) ==3:
  #       color = self.data['colors'][random.randint(0, (len(self.data['colors']) - 1))]
  #       leds.setColor('pixel', (int(color[0]), int(color[1]), int(color[2])), i)
  #     else:
  #       leds.blankPixel(i)
  #   # leds.show()


# def rainbow_cycle():
#     for j in range(255):
#         if (MODE != 'rainbow'):
#             blank()
#             break
#         for i in range(num_pixels):
#             if (MODE != 'rainbow'):
#                 break
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         s.sleep()

# def scroll(direction):
#     if (direction == 'lr'):
#         for column_number, column in list(enumerate(pin_map[0])):
#             if (direction != 'lr'):
#                 blank()
#                 break
#             blank_columns(column_number)
#             show_column(column_number)
#     elif (direction == 'rl'):
#         for column_number, column in reversed(list(enumerate(pin_map[0]))):
#             if (direction != 'lr'):
#                 blank()
#                 break
#             blank_columns(column_number)
#             show_column(column_number)
#     elif (direction == 'tb'):
#         for row_number, row in reversed(list(enumerate(pin_map))):
#             if (direction != 'tb'):
#                 blank()
#                 break
#             blank_rows(row_number)
#             show_row(row_number)
#     elif (direction == 'bt'):
#         for row_number, row in list(enumerate(pin_map)):
#             if (direction != 'bt'):
#                 blank()
#                 break
#             blank_rows(row_number)
#             show_row(row_number)


# snake_count = 1
# def snake():
#     global snake_count
#     for row_number, row in list(enumerate(pin_map)):
#         for column in pin_map[row_number]:
#             if (snake_count == 1):
#                 pixels[column - 1] = (255, 0 ,0)
#             elif (snake_count == 2):
#                 pixels[column - 1] = (0, 255 ,0)
#             else:
#                 pixels[column - 1] = (0, 0 ,255)
#             pixels.show()
#             s.sleep()
#     snake_count = snake_count + 1
#     if (snake_count > 3):
#         snake_count = 1

