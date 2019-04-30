import sys
sys.path.append("..")

from mapping import data


def get_friendly_name(name):
  parts = name.split('_')
  for i in range(len(parts)):
    parts[i] = parts[i].capitalize()
  return ' '.join(parts)

def get_id(name):
  return '_'.join(get_friendly_name(name).split(' '))

def get_format(name, unit):
  if 'humidity' in name:
    return '%d%%'
  if 'temperature' in name:
    return '%.0f °C'
  return '%d'

for key in data:
  val = data[key]
  name = val.get('name')
  if not val.get('ok'):
    continue
  if 'timer' in name:
    continue
  id = get_id(name)
  friendly_name = get_friendly_name(name)
  format = get_format(name, val.get('unit'))
  item = 'Number ComfoAir_{}   "{} [{}]" (gPersistEveryMin)   {{ mqtt="<[mosquitto:comfoair/status/{}:state:default]" }}'.format(id, friendly_name, format, name)
  print(item)