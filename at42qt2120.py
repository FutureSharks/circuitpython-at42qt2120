"""
`at42qt2120`
====================================================

AT42QT2120 capacitive touch controller IC.

See usage in the examples/at42_simpletest.py file.

Implementation Notes
--------------------

**Hardware:**

* AT42QT2120 IC: https://www.microchip.com/wwwproducts/en/AT42QT2120

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time

import adafruit_bus_device.i2c_device as i2c_device
from micropython import const

__version__ = "0.1"
__repo__ = "https://github.com/FutureSharks/circuitpython-at42qt2120"

# Register addresses.  Unused registers commented out to save memory.
AT42QT2120_FIRMWARE_VERSION = const(0x1)
AT42QT2120_I2CADDR_DEFAULT  = const(0x1C)
AT42QT2120_RESET            = const(7)
AT42QT2120_KEY_STATUS_A     = const(3)
AT42QT2120_KEY_STATUS_B     = const(4)
AT42QT2120_SLIDER_POSITION  = const(5)


class AT42QT2120:
    """Driver for the AT42QT2120 capacitive touch sensor."""

    def __init__(self, i2c, change_pin, address=AT42QT2120_I2CADDR_DEFAULT):
        self._i2c = i2c_device.I2CDevice(i2c, address)
        self._buffer = bytearray(2)
        self._change_pin = change_pin
        #self.reset()

    def _write_register_byte(self, register, value):
        # Write a byte value to the specifier register address.
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_register_bytes(self, register, result, length=None):
        # Read the specified register address and fill the specified result byte
        # array with result bytes.  Make sure result buffer is the desired size
        # of data to read.
        if length is None:
            length = len(result)
        with self._i2c:
            self._i2c.write(bytes([register]), stop=False)
            self._i2c.readinto(result, start=0, end=length)

    def reset(self):
        """Reset the AT42QT2120 into a default state ready to detect touch inputs.
        """
        # Write to the reset register.
        self._write_register_byte(AT42QT2120_RESET, 0x63)
        time.sleep(0.001) # This 1ms delay here probably isn't necessary but can't hurt.

    def get_firmware_version(self):
        """
        """
        self._read_register_bytes(AT42QT2120_FIRMWARE_VERSION, self._buffer)
        return self._buffer

    def get_slider_position(self):
        self._read_register_bytes(AT42QT2120_SLIDER_POSITION, self._buffer)
        return self._buffer

    def get_key_status_a(self):
        self._read_register_bytes(AT42QT2120_KEY_STATUS_A, self._buffer)
        return self._buffer

    def get_key_status_b(self):
        self._read_register_bytes(AT42QT2120_KEY_STATUS_B, self._buffer)
        return self._buffer

    def change_detected(self):
        '''
        '''
        if self._change_pin.value:
            return False
        else:
            return True
