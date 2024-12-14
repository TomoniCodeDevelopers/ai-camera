#
#  Huskylens Python Driver 1.1 (2024/12/13)
#  (on LEGO SPIKE FLASH)
#
#  known bug: [('info', 1, 3, '0x2760'), ('block', 1, 174, 143, 24, 26), None]
#

import machine
import utime

CMD_REQ_KNOCK = bytes((0x55,0xAA,0x11,0x00,0x2C,0x3C))
CMD_REQ_BLKS_ARWS = bytes((0x55, 0xAA, 0x11, 0x00, 0x20, 0x30))
CMD_REQ_BLOCKS = bytes((0x55, 0xAA, 0x11, 0x00, 0x21, 0x31))
CMD_REQ_ARROWS = bytes((0x55, 0xAA, 0x11, 0x00, 0x22, 0x32))

COMMAND_POS=4
COMMAND_RETURN_INFO = 0x29
COMMAND_RETURN_BLOCK = 0x2A
COMMAND_RETURN_ARROW = 0x2B

def send_CMD_REQ_ALGO(uart, type):
    cmd_pre_part = (0x55, 0xAA, 0x11, 0x02, 0x2D)
    if type == 'FACE_RECOG':
        algo_defs = (0x00,0x0)
    elif type == 'OBJ_TRACK':
        algo_defs = (0x01,0x00)
    elif type == 'OBJ_RECOG':
        algo_defs = (0x02,0x00)
    elif type == 'LINE_TRACK':
        algo_defs = (0x03,0x00)
    elif type == 'COLOR_RECOG':
        algo_defs = (0x04,0x00)
    elif type == 'TAG_RECOG':
        algo_defs = (0x05,0x00)
    elif type == 'OBJ_CLSSIFY':
        algo_defs = (0x06,0x00)

    cmd = cmd_pre_part + algo_defs
    parity = sum(cmd) & 0xff
    cmd = cmd + (parity,)
    uart.write(bytes(cmd))

def read_tag(uart):
    buf = bytearray(100)
    uart.write(CMD_REQ_BLOCKS)
    utime.sleep(0.1)
    size = uart.read(buf)
    ret_val = []
    if size > 0 :
        val = parse_return_data(buf)
        ret_val.append(val)
    if size >= 16:
        val = parse_return_data(buf[16:])
        ret_val.append(val)
    if size >= 32:
        val = parse_return_data(buf[32:])
        ret_val.append(val)
    return ret_val

def parse_return_data(data):
    command = data[COMMAND_POS]
    if command == 0x29:
        return parse_return_info(data[5:])
    elif command == 0x2A:
        return parse_return_block(data[5:])
    elif command == 0x2B:
        return parse_return_arrow(data[5:])
    else:
        print('command??',command)

def parse_return_block(data):
    x_center = ( data[1] << 8 ) + data[0]
    y_center = ( data[3] << 8 ) + data[2]
    width = ( data[5] << 8 ) + data[4]
    height = ( data[7] << 8 ) + data[6]
    id = ( data[9] << 8 ) + data[8]
    #print('show return block',end=' ')
    #print(id, x_center, y_center, width, height)
    return ('block', id, x_center, y_center, width, height)

def parse_return_arrow(data):
    x_origin = ( data[1] << 8 ) + data[0]
    y_origin = ( data[3] << 8 ) + data[2]
    x_target = ( data[5] << 8 ) + data[4]
    y_target = ( data[7] << 8 ) + data[6]
    id = ( data[9] << 8 ) + data[8]
    #print('show return arrow',end=' ')
    #print(id, x_origin, y_origin, x_target, y_target)
    return ('arrow', id, x_origin, y_origin, x_target, y_target)

def parse_return_info(data):
    n_of_blk_arw = (data[1] << 8 ) + data[0]
    n_of_id = (data[3] << 8 ) + data[2]
    fr_no = (data[5] << 8 ) + data[4]
    #print('show return info',end=' ')
    #print(n_of_blk_arw, n_of_id, hex(fr_no))
    return('info', n_of_blk_arw, n_of_id, hex(fr_no))

def send_CMD_REQ_KNOCK(uart):
    uart.write(CMD_REQ_KNOCK)

def send_CMD_REQ_BLOCKS(uart):
    uart.write(CMD_REQ_BLOCKS)

def send_CMD_REQ_ARROWS(uart):
    uart.write(CMD_REQ_ARROWS)
