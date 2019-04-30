import paho.mqtt.client as mqtt
import logging
import sys

from USBCAN import CANInterface
import mapping
from time import sleep

def on_mqtt_connect(client, userdata, flags, rc):
  logger.info('ubscribing to comfoair/action')
  client.subscribe('comfoair/action')

def on_mqtt_message(client, userdata, msg):
  action =str(msg.payload.decode('utf-8'))
  logger.info('got mqtt message %s %s', msg.topic, action)
  if action in mapping.commands:
    command = mapping.commands[action]
    logger.info('action ok, executing: %s', action)
    try:
      for i in range(3):
        can.send(command)
        sleep(2)
    except Exception as e:
      logger.error('failed in send %s', e)
  else:
    logger.error('action not found %s', action)

def process_can_message(pdid, data):
  if pdid in mapping.data:
    pdid_config = mapping.data[pdid]
    value =  pdid_config.get('transformation')(data)
    if pdid_config.get('ok'):
      name = pdid_config.get('name')
      mqtt_client.publish('comfoair/status/' + name, value)
    else:
      logger.info('not ok, not pushing %s %s', pdid, value)
  elif pdid != 0:
    logger.info('pid not found %s %s', pdid, data)

logger = logging.getLogger('comfoair-main')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger.info('starting up')
mqtt_client = mqtt.Client()
mqtt_client.connect('192.168.3.4', 1883, 60)
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message
mqtt_client.loop_start()

can = CANInterface('/dev/ttyUSB0', 2000000)
can.open()
can.read(process_can_message)
