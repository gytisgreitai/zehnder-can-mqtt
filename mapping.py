from struct import unpack

def transform_temperature(value: list) -> float:
  parts = bytes(value[0:2])
  word = unpack('<h', parts)[0]
  return float(word)/10


def transform_air_volume(value: list) -> float:
  parts = value[0:2]
  word = unpack('<h', parts)[0]
  return float(word)

def transform_any(value: list) -> float:
  word = 0
  for n in range(len(value)):
      word += value[n]<<(n*8)
  return word

def transform_away(value: list) -> bool:
    val = transform_any(value)
    if val == 7:
        return True
    if val == 1:
        return False
    return None

def transform_operating_mode(value: list) -> str:
    val = transform_any(value)
    if val == 255:
        return 'auto'
    if val == 1:
        return 'limited_manual'
    if val == 5:
        return 'unlimited_manual'
    return None

def transform_operating_mode2(value: list) -> str:
    val = transform_any(value)
    if val == 1:
        return 'unlimited_manual'
    return 'auto'


# 8415 0601 00000000 100e0000 01	Set ventilation mode: supply only for 1 hour
# 8515 0601	Set ventilation mode: balance mode
# 8415 0301 00000000 ffffffff 00	Set temperature profile: normal
# 8415 0301 00000000 ffffffff 01	Set temperature profile: cool
# 8415 0301 00000000 ffffffff 02	Set temperature profile: warm
# 8415 0201 00000000 100e0000 01	Set bypass: activated for 1 hour
# 8415 0201 00000000 100e0000 02	Set bypass: deactivated for 1 hour
# 8515 0201	Set bypass: auto
# 031d 0104 00	Set sensor ventilation: temperature passive: off
# 031d 0104 01	Set sensor ventilation: temperature passive: auto only
# 031d 0104 02	Set sensor ventilation: temperature passive: on
# 031d 0106 00	Set sensor ventilation: humidity comfort: off
# 031d 0106 01	Set sensor ventilation: humidity comfort: auto only
# 031d 0106 02	Set sensor ventilation: humidity comfort: on
# 031d 0107 00	Set sensor ventilation: humidity protection: off
# 031d 0107 01	Set sensor ventilation: humidity protection: auto
# 031d 0107 02	Set sensor ventilation: humidity protection: on
commands = {
    'ventilation_level_0':    [0x84, 0x15, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00],
    'ventilation_level_1':    [0x84, 0x15, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01],
    'ventilation_level_2':    [0x84, 0x15, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02],
    'ventilation_level_3':    [0x84, 0x15, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x03],
    'bypass_activate_1h':     [0x84, 0x15, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0e, 0x00, 0x00, 0x01],
    'bypass_deactivate_1h':   [0x84, 0x15, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0e, 0x00, 0x00, 0x02],
    'bypass_auto':            [0x84, 0x15, 0x02, 0x01],
    'air_supply_only':        [0x84, 0x15, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0e, 0x00, 0x00, 0x01],
    'air_extract_only':       [0x84, 0x15, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0e, 0x00, 0x00, 0x00],
    'ventilation_balance':    [0x84, 0x15, 0x06, 0x01],
    'temp_profile_normal':    [0x84, 0x15, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0x00],
    'temp_profile_cool':      [0x84, 0x15, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0x01],
    'temp_profile_warm':      [0x84, 0x15, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0x02],
    'boost_10_min':           [0x84, 0x15, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x58, 0x02, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00],
    'boost_20_min':           [0x84, 0x15, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0xB0, 0x04, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00],
    'boost_30_min':           [0x84, 0x15, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x08, 0x07, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00],
    'boost_60_min':           [0x84, 0x15, 0x01, 0x06, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0E, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00],
    'boost_end':              [0x85, 0x15, 0x01, 0x06],
    'auto':                   [0x85, 0x15, 0x08, 0x01],
    'manual':                 [0x84, 0x15, 0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01],
}

data = {
  16: {
      "name": "away_indicator",
      "ok" : True,
      "unit": "",
      "icon": "mdi:m³home-export-outline",
      "transformation": transform_away
  }, 
  17: {
      "name": "z_unknown_NwoNode",
      "ok" : False,
      "unit": "",
      "transformation": transform_any
  },
  18: {
      "name": "z_unknown_NwoNode",
      "ok" : False,
      "unit": "",
      "transformation": transform_any
  },
  49: {
      "name": "operating_mode",
      "ok" : True,
      "unit": "",
      "icon": "mdi:m³brightness-auto",
      "transformation": transform_operating_mode
  },
  56: {
      "name": "operating_mode2",
      "ok" : True,
      "unit": "",
      "icon": "mdi:m³brightness-auto",
      "transformation": transform_operating_mode2
  },
  65: {
      "name": "ventilation_level",
      "ok" : True,
      "unit": "",
      "icon": "mdi:fan",
      "transformation": lambda x: int(x[0])
  },
  66: {
      "name": "bypass_state",
      "ok" : True,
      "unit": "",
      "icon": "mdi:m³gate-open", 
      "transformation": lambda x: ['auto', 'open', 'close'][int(x[0])]
  },
  67: {
      "name": "temperature_profile",
      "ok" : True,
      "unit": "", 
      "icon": "mdi:thermometer-lines",
      "transformation": lambda x: ['normal', 'cold', 'warm'][int(x[0])]
  },
  81: {
      "name": "timer_1",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  82: {
      "name": "timer_2",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  83: {
      "name": "timer_3",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  84: {
      "name": "timer_4",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  85: {
      "name": "timer_5",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  86: {
      "name": "timer_6",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  87: {
      "name": "timer_7",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  88: {
      "name": "timer_8",
      "ok" : True,
      "unit": "s",
      "transformation": transform_any
  },
  96: {
      "name": "bypass ??? ValveMsg",
      "ok" : False,
      "unit": "unknown",
      "transformation": transform_any
  },
  97: {
      "name": "bypass_b_status",
      "ok" : True,
      "icon": "mdi:gate-open",
      "unit": "",
      "transformation": transform_air_volume
  },
  98: {
      "name": "bypass_a_status",
      "ok" : True,
      "icon": "mdi:gate-open", 
      "unit": "",
      "transformation": transform_air_volume
  },
  115: {
      "name": "fan_exhaust_enabled",
      "ok" : True,
      "unit": "",
      "icon": "mdi:fan-chevron-down",
      "transformation": transform_any
  },
  116: {
      "name": "fan_supply_enabled",
      "ok" : True,
      "unit": "",
      "icon": "mdi:fan-chevron-up",
      "transformation": transform_any
  },
  117: {
      "name": "fan_exhaust_duty",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:fan-chevron-down",
      "transformation": lambda x: float(x[0])
  },
  118: {
      "name": "fan_supply_duty",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:fan-chevron-up",
      "transformation": lambda x: float(x[0])
  },
  119: {
      "name": "fan_exhaust_flow",
      "ok" : True,
      "unit": "m³",
      "icon": "mdi:fan",
      "transformation": transform_air_volume
  },
  120: {
      "name": "fan_supply_flow",
      "ok" : True,
      "unit": "m³",
      "icon": "mdi:fan",
      "transformation": transform_air_volume
  },
  121: {
      "name": "fan_exhaust_speed",
      "ok" : True,
      "unit": "rpm",
      "icon": "mdi:speedometer",
      "transformation": transform_air_volume
  },
  122: {
      "name": "fan_supply_speed",
      "ok" : True,
      "unit": "rpm",
      "icon": "mdi:speedometer",
      "transformation": transform_air_volume
  },
  128: {
      "name": "power_consumption_ventilation",
      "ok" : True,
      "unit": "W",
      "icon": "mdi:power-socket-eu",
      "transformation": lambda x: float(x[0])
  },
  129: {
      "name": "power_consumption_year_to_date",
      "ok" : True,
      "unit": "kWh",
      "mdi": "mdi:power-plug",
      "transformation": transform_air_volume
  },
  130: {
      "name": "power_consumption_total_from_start",
      "ok" : True,
      "unit": "kWh",
      "mdi": "mdi:power-plug",
      "transformation": transform_air_volume
  },
  144: {
      "name": "power_consumption_preheater_year_to_date",
      "ok" : True,
      "unit": "kWh",
      "mdi": "mdi:power-plug",
      "transformation": transform_any
  },
  145: {
      "name": "power_consumption_preheater_from_start",
      "ok" : True,
      "unit": "kWh",
      "mdi": "mdi:power-plug",
      "transformation": transform_any
  },
  146: {
      "name": "power_consumption_preheater_current",
      "ok" : True,
      "unit": "W",
      "mdi": "mdi:power-plug",
      "transformation": transform_any
  },
  192: {
      "name": "days_until_next_filter_change",
      "ok" : True,
      "unit": "days",
      "mdi": "mdi:air-filter",
      "transformation": transform_any
  },
  208: {
      "name": "z_Unknown_TempHumConf",
      "ok" : False,
      "unit": "",
      "transformation": transform_any
  },
  209: {
      "name" : "rmot",
      "ok" : True,
      "unit":"°C",
      "icon": "mdi:thermometer-alert",
      "transformation":transform_temperature
  },
  210: {
      "name": "z_Unknown_TempHumConf",
      "ok" : False,
      "unit": "",
      "transformation": transform_any
  },
  211: {
      "name": "z_Unknown_TempHumConf",
      "ok" : False,
      "unit": "",
      "transformation": transform_any
  },
  212: {
      "name": "target_temperature",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer-lines",
      "transformation": transform_temperature
  },
  213: {
      "name": "power_avoided_heating_actual",
      "ok" : True,
      "unit": "W",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_any
  },
  214: {
      "name": "power_avoided_heating_year_to_date",
      "ok" : True,
      "unit": "kWh",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_air_volume
  },
  215: {
      "name": "power_avoided_heating_from_start",
      "ok" : True,
      "unit": "kWh",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_air_volume
  },
  216: {
      "name": "power_avoided_cooling_actual",
      "ok" : True,
      "unit": "W",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_any
  },
  217: {
      "name": "power_avoided_cooling_year_to_date",
      "ok" : True,
      "unit": "kWh",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_air_volume
  },
  218: {
      "name": "power_avoided_cooling_from_start",
      "ok" : True,
      "unit": "kWh",
      "icon": "mdi:power-plug-off-outline",
      "transformation": transform_air_volume
  },
  219: {
      "name": "power_preheater_target",
      "ok" : True,
      "unit": "W",
      "icon": "mdi:power-plug",
      "transformation": transform_any
  },
  220: {
      "name": "air_supply_temperature_before_preheater",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer",
      "transformation": transform_temperature
  },
  221: {
      "name": "air_supply_temperature",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer",
      "transformation": transform_temperature
  },
  222: {
      "name": "z_Unknown_TempHumConf",
      "unit": "",
      "transformation": transform_any
  },
  224: {
      "name": "z_Unknown_VentConf",
      "unit": "",
      "transformation": transform_any
  },
  225: {
      "name": "z_Unknown_VentConf",
      "unit": "",
      "transformation": transform_any
  },
  226: {
      "name": "z_Unknown_VentConf",
      "unit": "",
      "transformation": transform_any
  },
  227: {
      "name": "bypass_open_percentage",
      "ok" : True,
      "unit": "%",
      "transformation": lambda x: float(x[0])
  },
  228: {
      "name": "frost_disbalance",
      "ok" : True,
      "unit": "%",
      "transformation": lambda x: float(x[0])
  },
  229: {
      "name": "z_Unknown_VentConf",
      "unit": "",
      "transformation": transform_any
  },
  230: {
      "name": "z_Unknown_VentConf",
      "unit": "",
      "transformation": transform_any
  },

  256: {
      "name": "z_Unknown_NodeConf",
      "unit": "unknown",
      "transformation": transform_any
  },
  257: {
      "name": "z_Unknown_NodeConf",
      "unit": "unknown",
      "transformation": transform_any
  },

  273: {
      "name": "temperature_unknown",
      "unit": "°C",
      "ok": False,
      "transformation": transform_temperature
  },
  274: {
      "name": "air_extract_temperature",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:home-thermometer-outline",
      "transformation": transform_temperature
  },
  275: {
      "name": "air_exhaust_temperature",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:home-thermometer-outline",
      "transformation": transform_temperature
  },
  276: {
      "name": "air_outdoor_temperature_before_preheater",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer",
      "transformation": transform_temperature
  },
  277: {
      "name": "air_outdoor_temperature",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer",
      "transformation": transform_temperature
  },
  278: {
      "name": "air_supply_temperature_2",
      "ok" : True,
      "unit": "°C",
      "icon": "mdi:thermometer",
      "transformation": transform_temperature
  },
  289: {
      "name": "z_unknown_HumSens",
      "unit": "",
      "transformation": transform_any
  },
  290: {
      "name": "air_extract_humidity",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:water-percent",
      "transformation": lambda x: float(x[0])
  },
  291: {
      "name": "air_exhaust_humidity", 
      "ok" : True,
      "unit": "%",
      "icon": "mdi:water-percent",
      "transformation": lambda x: float(x[0]) 
  }, 
  292: {
      "name": "air_outdoor_humidity_before_preheater",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:water-percent",
      "transformation": lambda x: float(x[0])
  },
  293: {
      "name": "air_outdoor_humidity",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:water-percent",
      "transformation": lambda x: float(x[0])
  },
  294: {
      "name": "air_supply_humidity",
      "ok" : True,
      "unit": "%",
      "icon": "mdi:water-percent",
      "transformation": lambda x: float(x[0])
  },

  305: {
      "name": "pressure_exhaust",
      "ok" : True,
      "unit": "Pa",
      "icon": "mdi:package-down",
      "transformation": transform_any
  },
  306: {
      "name": "pressure_supply",
      "ok" : True,
      "unit": "Pa",
      "icon": "mdi:package-down",
      "transformation": transform_any
  },

  369: {
      "name": "z_Unknown_AnalogInput",
      "unit": "V?",
      "transformation": transform_any
  },
  370: {
      "name": "z_Unknown_AnalogInput",
      "unit": "V?",
      "transformation": transform_any
  },
  371: {
      "name": "z_Unknown_AnalogInput",
      "unit": "V?",
      "transformation": transform_any
  },
  372: {
      "name": "z_Unknown_AnalogInput",
      "unit": "V?",
      "transformation": transform_any
  },
  400: {
      "name": "z_Unknown_PostHeater_ActualPower",
      "unit": "W",
      "transformation": transform_any
  },
  401: {
      "name": "z_Unknown_PostHeater_ThisYear",
      "unit": "kWh",
      "transformation": transform_any
  },
  402: {
      "name": "z_Unknown_PostHeater_Total",
      "unit": "kWh",
      "transformation": transform_any
  },
#00398041 unknown 0 0 0 0 0 0 0 0
}
