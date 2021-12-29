import mapping
import logging
import json

logger = logging.getLogger('comfoair-hass')

def get_friendly_name(name):
  parts = name.split('_')
  for i in range(len(parts)):
    parts[i] = parts[i].capitalize()
  return ' '.join(parts)

def publish_hass_mqtt_discovery(mqtt_client):
  logger.info("hass mqtt")
  try:
    for key in mapping.data:
      val = mapping.data[key]
      id = val.get('name')
      icon = val.get('icon')
      unit = val.get('unit')
      friendly_name = get_friendly_name(id)

      if not val.get('ok'):
        continue
      if 'timer' in id:
        continue
    
      payload = {
        "name": f"{friendly_name}",
        "state_topic": f"comfoair/status/{id}",
        "availability_topic": "comfoair/status",
        "platform": "mqtt",
        "unique_id": f"comfoair_{id}",
        "device": {
          "manufacturer": "Zehnder",
          "model": "ComfoAir Q350",
          "name": "Q350",
          "identifiers": "Q350"
        }
      }
      
      if icon is not None:
        payload['icon'] = icon
      
      if unit is not None:
        payload['unit_of_measurement'] = unit

      topic_name = f"homeassistant/sensor/comfoair/{id}/config"
      raw_payload = json.dumps(payload)
      logger.info("publishing discovery %s %s", topic_name, raw_payload)
      mqtt_client.publish(topic_name, raw_payload, 0, True)
  except e:
    logger.error(e)