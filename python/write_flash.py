import pytoshload.ramcode as rc
import pytoshload.toshload as tl
import time
import serial

ser = serial.Serial('COM4', 19200, timeout=0.5)

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

f = open("DE92-02439D FW PATCHED.bin", "rb")
#f = open("DE92-02439D FW.bin", "rb")
data = f.read()
f.close()

raise IOError("WARNING: About to ERASE firmware. Make sure you have new firmware first then uncomment this file")

bl = tl.LowLevelBootloader(ser, reset_function)
print(bl.cmd_productinfo())
bl.cmd_erase()

bl = tl.LowLevelBootloader(ser, reset_function)
print(bl.cmd_productinfo())
rd = rc.B_F16_RAM1000_ROM10000_TLCS900L1["data"]
rd[0x23] = 0xA2 # INTES1
rd[0x37] = 0xA2 # INTES1
rd[0x2E] = 0x2D # MicroDMA for INTTX1
bl.cmd_ram_transfer(rd, rc.B_F16_RAM1000_ROM10000_TLCS900L1["start_address"])
rl = tl.RamCodeProtocol(ser)
time.sleep(0.1)
print(rl.cmd_id())
rl.cmd_program(0x10000, data)

print(len(data))
reset_function(False)
