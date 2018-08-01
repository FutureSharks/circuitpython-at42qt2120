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

# Enable slider mode on channels 0-2
at42.enable_slider()

while True:
    # Print slider position
    # See page 25 of datasheet for details of how the contacts should be shaped
    print(at42.get_slider_wheel_position())
