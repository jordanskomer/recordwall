import leds
import cache

class Intent(object):
  def __invalid(requestId, userId, data):
    return {}
  # https://developers.google.com/assistant/smarthome/develop/process-intents#sync-response
  def SYNC(requestId, userId, data):
    return {
      'requestId': requestId,
      'payload': {
        'agentUserId': userId,
        'devices': [
          {
            'id': 1,
            'type': 'action.devices.types.LIGHT',
            'traits': [
              'action.devices.traits.Brightness',
              'action.devices.traits.ColorSetting',
              'action.devices.traits.LightEffects',
              'action.devices.traits.OnOff'
            ],
            'name': {
              'defaultNames': [
                'Record Wall'
              ],
              'name': 'Record Wall'
            },
            "attributes": {
              "colorModel": "hsv",
              "supportedEffects": [
                "colorLoop",
                "sleep",
                "wake"
              ]
            },
            'willReportState': False
          }
        ]
      }
    }

  def QUERY(requestId, userId, data):
    return {
      'requestId': requestId,
      'payload': {
        'devices': {
          '1': {
            'status': 'SUCCESS',
            'online': True,
            'on': cache.get(cache.STATE),
            'brightness': cache.get(cache.BRIGHTNESS),
            'spectrumRgb': cache.get(cache.COLOR)
          }
        }
      }
    }

  def EXECUTE(requestId, userId, data):
    print('EXECUTE: State: %s Brightness: %s Color: %s Mode: %s' % (
      cache.get(cache.STATE),
      cache.get(cache.BRIGHTNESS),
      cache.get(cache.COLOR),
      cache.get(cache.MODE)
    ))
    for command in data['inputs'][0]['payload']['commands']:
      for execute in command['execution']:
        if ('OnOff' in execute['command']):
          if execute['params']['on']:
            leds.turnOn()
          else:
            leds.turnOff()
        elif ('BrightnessAbsolute' in execute['command']):
          leds.changeBrightness(int(execute['params']['brightness']))
        elif ('ColorAbsolute' in execute['command']):
          rgb = leds.hsv_to_rgb(
            execute['params']['color']['spectrumHSV']['hue'] / 360.0,
            execute['params']['color']['spectrumHSV']['saturation'],
            execute['params']['color']['spectrumHSV']['value']
          )
          print(rgb)
          leds.changeColor(rgb)
        print('Ran %s' % execute['command'])
        leds.show()
    print('EXECUTE: State: %s Brightness: %s Color: %s Mode: %s' % (
      cache.get(cache.STATE),
      cache.get(cache.BRIGHTNESS),
      cache.get(cache.COLOR),
      cache.get(cache.MODE)
    ))
    return {
      'requestId': requestId,
      'payload': {
        'commands': [
          {
            'ids': [
              '1'
            ],
            'status': 'SUCCESS',
            'states': {
              'online': True,
              'on': cache.get(cache.STATE),
              'brightness': cache.get(cache.BRIGHTNESS),
              'spectrumRgb': cache.get(cache.COLOR)
            }
          }
        ]
      }
    }


  def __new__(cls, intent_type, request_id, data):
    method = getattr(cls, intent_type, cls.__invalid)
    return method(request_id, '12345', data)