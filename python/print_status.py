import pytoshload.ramcode as rc
import pytoshload.toshload as tl
import time
import serial

ser = serial.Serial('COM4', 9600, timeout=0.5)

def reset_function(boot_mode=True):
    #RTS/DTR logic levels "backwards" - watch out!!
    ser.rts = True
    if boot_mode:
        ser.dtr = True
    else:
        ser.dtr = False
    time.sleep(0.1)
    ser.rts = False
    time.sleep(1)

ser.flush()

bl = tl.LowLevelBootloader(ser, reset_function)
print(bl.cmd_productinfo())
print(bl.cmd_get_crc())

#Reset normal mode
reset_function(False)