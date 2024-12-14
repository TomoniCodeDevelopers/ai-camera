#
# Test code for Huskylens driver (runs on ESP32-C3)
#
import machine
from huskylens_lib import HuskyLens

uart1 = machine.UART(1)
uart1.init(baudrate=9600, bits=8, parity=None, stop=1, tx=21, rx=20)

husky = HuskyLens(uart1)
#husky.send_CMD_REQ_ALGO('FACE_RECOG')
husky.send_CMD_REQ_ALGO('COLOR_RECOG')
#husky.send_CMD_REQ_ALGO('TAG_RECOG')
#husky.send_CMD_REQ_ALGO('LINE_TRACK')
#husky.send_CMD_REQ_ALGO('TAG_RECOG')

while True:
   print(husky.read_block())



