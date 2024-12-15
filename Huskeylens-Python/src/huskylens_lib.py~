#
#  Huskylens Python Driver 1.5 (2024/12/15)
#  file: huskylens_lib.py
#  (only test on ESP32-C3, version='v1.23.0 on 2024-06-02')
#
#  change log
#  version 1.2(2024/12/14)
#     * bug fix  (func: read_block())
#       Fixed the size calculation error of the return array from Huskylens.
#     * Feature Addition  (func: read_ block())
#       Differentiate between the LEGO-specific and general-purpose UART 
#       read functions 
#
#  version 1.3(2024/12/14)
#     * Refactoring: Consolidate functions into a class
#     * rename the file  Huskylens.py -> huskylens_lib.py
#
#  version 1.4(2024/12/14)
#     * Refactoring: Handle abnormal return values from Huskylens
#                     via uart communication
#
#  version 1.5(2024/12/15)
#     * Refactoring: Changed the recognition algorithm specification 
#                    from string type to Enum type ().
#
#

import utime
import uos

from enum import Enum
class Algo(Enum):
    FACE_RECOGNITION = 1
    OBJECT_TRACKING = 2
    OBJECT_RECOGNITION = 3
    LINE_TRACKING = 4
    COLOR_RECOGNITION = 5
    TAG_RECOGNITION = 6
    OBJECT_CLASSIFICATION = 7


CMD_REQ_KNOCK = bytes((0x55,0xAA,0x11,0x00,0x2C,0x3C))
CMD_REQ_BLKS_ARWS = bytes((0x55, 0xAA, 0x11, 0x00, 0x20, 0x30))
CMD_REQ_BLOCKS = bytes((0x55, 0xAA, 0x11, 0x00, 0x21, 0x31))
CMD_REQ_ARROWS = bytes((0x55, 0xAA, 0x11, 0x00, 0x22, 0x32))

COMMAND_POS = 4
COMMAND_RETURN_HEADER = 0x55
COMMAND_RETURN_INFO = 0x29
COMMAND_RETURN_BLOCK = 0x2A
COMMAND_RETURN_ARROW = 0x2B
COMMAND_RETURN_OK = 0x2E
COMMAND_RETURN_IS_PRO = 0x3B
COMMAND_RETURN_BUSY = 0x3D
COMMAND_RETURN_NEED_PRO = 0x3E


class HuskyLens:

    def __init__(self, uart):  
        self.machine = uos.uname().machine
        self.uart = uart

    #
    # methods for send command
    #
    def send_CMD_REQ_ALGO(self, type):
        cmd_pre_part = (0x55, 0xAA, 0x11, 0x02, 0x2D)
        if type == Algo.FACE_RECOGNITION:
            algo_defs = (0x00,0x0)
        elif type == Algo.OBJECT_TRACKING:
            algo_defs = (0x01,0x00)
        elif type == Algo.OBJECT_RECOGNITION:
            algo_defs = (0x02,0x00)
        elif type == Algo.LINE_TRACKING:
            algo_defs = (0x03,0x00)
        elif type == Algo.COLOR_RECOGNITION:
            algo_defs = (0x04,0x00)
        elif type == Algo.TAG_RECOGNITION:
            algo_defs = (0x05,0x00)
        elif type == Algo.OBJECT_CLASSIFICATION:
            algo_defs = (0x06,0x00)
        else:
            print('Error unknown ALGO:',type)
            return None
    
        cmd = cmd_pre_part + algo_defs
        parity = sum(cmd) & 0xff
        cmd = cmd + (parity,)
        self.uart.write(bytes(cmd))
    
    def send_CMD_REQ_KNOCK(self):
        self.uart.write(CMD_REQ_KNOCK)
    
    def send_CMD_REQ_BLOCKS(self):
        self.uart.write(CMD_REQ_BLOCKS)
    
    def send_CMD_REQ_ARROWS(self):
        self.uart.write(CMD_REQ_ARROWS)
    

    #
    # methods for receive data
    #
    def read_tag(self):
        return self.read_block()
    
    def read_block(self):
        buf = bytearray(100)
        ret_val = []
        self.uart.write(CMD_REQ_BLOCKS)
        utime.sleep(0.1)
    
        # check current uPy(general MPU) or LEGO Special uPy
        if 'ESP' in self.machine:
            # for MicroPython(general MPU eg; ESP)
            read_size = self.uart.readinto(buf)
        else:   # must be changed this check stmt
            # for MicroPython(LEGO)
            read_size = self.uart.read(buf)

        # check received data
        if read_size == 0:
            return ret_val    # return []
        if buf[0] != COMMAND_RETURN_HEADER:
            return ret_val    # return []    # illegal data

        parse_pos = 0
        while parse_pos < read_size:
            (val, data_size) = self.parse_return_data(buf[parse_pos:])
            if val[0] == 'block':
                ret_val.append(val)
            if data_size:
               parse_pos += data_size
            else:
               break  # parse Error
        return ret_val
    
    def parse_return_data(self, data):
        data_size = None
        if len(data) < (COMMAND_POS + 1):
            return (('unknown',), data_size)
        command = data[COMMAND_POS]
        if command == COMMAND_RETURN_INFO:
            data_size = 16
            return (self.parse_return_info(data[5:]), data_size)
        elif command == COMMAND_RETURN_BLOCK:
            data_size = 16
            return (self.parse_return_block(data[5:]), data_size)
        elif command == COMMAND_RETURN_ARROW:
            data_size = 16
            return (self.parse_return_arrow(data[5:]), data_size)
        elif command == COMMAND_RETURN_OK:
            data_size = 6
            print('command OK',hex(command))
            return (('ok',), data_size)
        elif command == COMMAND_RETURN_BUSY:
            data_size = 6
            print('Camera is busy')
            return (('busy',), data_size)
        else:
            data_size = None
            print('command??',hex(command))
            return (('unknown',), data_size)
    
    def parse_return_info(self, data):
        n_of_blk_arw = (data[1] << 8 ) + data[0]
        n_of_id = (data[3] << 8 ) + data[2]
        fr_no = (data[5] << 8 ) + data[4]
        return ('info', n_of_blk_arw, n_of_id, hex(fr_no))
    
    def parse_return_block(self, data):
        x_center = ( data[1] << 8 ) + data[0]
        y_center = ( data[3] << 8 ) + data[2]
        width = ( data[5] << 8 ) + data[4]
        height = ( data[7] << 8 ) + data[6]
        id = ( data[9] << 8 ) + data[8]
        return ('block', id, x_center, y_center, width, height)
    
    def parse_return_arrow(self, data):
        x_origin = ( data[1] << 8 ) + data[0]
        y_origin = ( data[3] << 8 ) + data[2]
        x_target = ( data[5] << 8 ) + data[4]
        y_target = ( data[7] << 8 ) + data[6]
        id = ( data[9] << 8 ) + data[8]
        return ('arrow', id, x_origin, y_origin, x_target, y_target)
    
    
#
#
#

# test only..
# >>> platform.platform()
# 'MicroPython-1.23.0-riscv-IDFv5.0.4-with-newlib4.1.0'
# >>> uos.uname()
# (sysname='esp32', nodename='esp32', release='1.23.0', version='v1.23.0 on 2024-06-02', machine='ESP32C3 module with ESP32C3')
#
#
