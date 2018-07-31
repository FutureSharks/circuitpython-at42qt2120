import time
import at42qt2120
import busio
import board
from digitalio import DigitalInOut, Direction

i2c = busio.I2C(board.SCL, board.SDA)

at42_change_pin = DigitalInOut(board.D7)
at42_change_pin.direction = Direction.INPUT

at42 = at42qt2120.AT42QT2120(i2c, at42_change_pin)

time.sleep(1)

firmware_version = at42.get_firmware_version()
print('AT42QT2120 with firmware version {0}.{1}'.format(firmware_version[0], firmware_version[1]))

while True:
    # Wait until a change is detected
    if at42.change_detected():
        print('Touch detected')
        # Read key status to clear change state
        clear_status = at42.get_key_status()
        time.sleep(0.05)
