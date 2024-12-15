#
# Test code for Huskylens driver (runs on ESP32-C3)
#
import machine
from huskylens_lib import Algo
from huskylens_lib import HuskyLens

uart1 = machine.UART(1)
uart1.init(baudrate=9600, bits=8, parity=None, stop=1, tx=21, rx=20)

husky = HuskyLens(uart1)
husky.send_CMD_REQ_ALGO(Algo.COLOR_RECOGNITION)

while True:
   print(husky.read_block())


# Valid Recognition Algorithm
#husky.send_CMD_REQ_ALGO(Algo.FACE_RECOGNITION)
#husky.send_CMD_REQ_ALGO(Algo.OBJECT_TRACKING)
#husky.send_CMD_REQ_ALGO(Algo.OBJECT_RECOGNITION)
#husky.send_CMD_REQ_ALGO(Algo.LINE_TRACKING)
#husky.send_CMD_REQ_ALGO(Algo.COLOR_RECOGNITION)
#husky.send_CMD_REQ_ALGO(Algo.TAG_RECOGNITION)
#husky.send_CMD_REQ_ALGO(Algo.OBJECT_CLASSIFICATION)

