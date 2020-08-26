import json
import redis

__client__ = redis.Redis(host='localhost', port=11211, db=0, decode_responses=True)

BRIGHTNESS = 'brightness'
SPEED = 'speed'
STATE = 'state'
COLOR = 'color'
MODE = 'mode'
USER = 'user'

def get(key):
  result = __client__.get(key)
  if (result and (key is BRIGHTNESS or key is SPEED)):
    return float(result)
  elif (result and (key is COLOR)):
    return eval(result)
  elif (result):
    return result
  else:
    return False

def put(key, data):
  __client__.set(key, str(data))