import serial
from time import sleep
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('comfoair-can')

class CN1FAddr:
  def __init__(self, SrcAddr, DstAddr, Address, MultiMsg, A8000, A10000, SeqNr):
    self.SrcAddr = SrcAddr
    self.DstAddr = DstAddr
    self.Address = Address
    self.MultiMsg = MultiMsg
    self.A8000 = A8000
    self.A10000 = A10000
    self.SeqNr = SeqNr

  def id(self):
    addr = 0x0
    addr |= self.SrcAddr << 0
    addr |= self.DstAddr << 6

    addr |= self.Address <<12
    addr |= self.MultiMsg<<14
    addr |= self.A8000   <<15
    addr |= self.A10000  <<16
    addr |= self.SeqNr   <<17
    addr |= 0x1F         <<24

    return addr
  def hex(self):
    return hex(self.id())[2:]

  def bytes(self):
    return bytes.fromhex(self.hex())

class CANInterface:

  START_BYTE_1 = 0x55
  START_BYTE_2 = 0XAA

  COMFOAIR_ADDRESS = 1

  send_sequence_nr = 0

  def __init__(self, device, baudrate):
    self.device = device
    self.baudrate = baudrate
  
  def open(self):
    self.sp = serial.Serial(self.device, self.baudrate)  
    self._send_magic_init_packet()

  def read(self, callback):
    frame = bytearray()
    while True:
      if self.sp.in_waiting != 0:
        new_byte = self._get_single_byte()
        if new_byte == self.START_BYTE_1:
          next_byte = self._get_single_byte()
          if next_byte == self.START_BYTE_2:
              id = frame[1:5]
              data =frame[5:]
              id_hex = str() + format(int.from_bytes(id, byteorder='little'), '#10X')
              pdid = (int(id_hex, 16)>>14)&0x7ff
              frame = bytearray()
              callback(pdid, data)
          else:
              frame.append(new_byte)
              frame.append(next_byte)
        else:
          frame.append(new_byte)
      else:
        sleep(1)

  def send(self, data):
    num_bytes = len(data)
    can_id = CN1FAddr(0x11, self.COMFOAIR_ADDRESS, 1, num_bytes>8, 0, 1, self.send_sequence_nr)
    self.send_sequence_nr = (self.send_sequence_nr + 1)&0x3
    if len(data) > 8:
      datagrams = int(len(data)/7)
      if len(data) == datagrams*7:
          datagrams -= 1
      for n in range(datagrams):
          self._write_to_can(can_id.bytes(), [n]+data[n*7:n*7+7])
      n+=1
      restlen = len(data)-n*7
      self._write_to_can(can_id.bytes(), [n|0x80]+data[n*7:n*7+restlen])
    else:
      self._write_to_can(can_id.bytes(), data)
  
  #----- private
  def _get_single_byte(self):
    return int.from_bytes(self.sp.read(size=1),  byteorder='little')

  
  def _write_to_can(self, id, data):
    num_bytes=len(data)
    send_buf = bytearray([0xAA,0xE0|num_bytes,])
    for byte in reversed(id):
        send_buf.append(byte)
    for byte in data:
        send_buf.append(byte)
    send_buf.append(0x55)
    self.sp.write(send_buf)


  def _send_magic_init_packet(self):
    send_buf = bytearray()
    send_buf.append(0xAA)
    send_buf.append(0x55)
    #Pack mystery byte
    send_buf.append(0x12)
    #Pack byte indicating CAN bus speed
    send_buf.append(0x09)
    #Pack frame type byte
    #use extended
    send_buf.append(0x02)
    #Filter not supported
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)
    #Mask not supported
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)
    #Hardcode mode to Normal? Set to 0x01 to get loopback mode
    send_buf.append(0x00)
    #Send magic byte (may have to be 0x01?)
    send_buf.append(0x01)
    #Send more magic bytes
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)
    send_buf.append(0x00)

    #Calculate checksum
    checksum = 0
    for idx in range(0,18):
        checksum += int(send_buf[idx])
    checksum = checksum % 255

    send_buf.append(checksum)
    self.sp.write(send_buf)
    logger.info('init config done')

  