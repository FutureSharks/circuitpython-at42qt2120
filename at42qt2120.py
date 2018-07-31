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
AT42QT2120_DETECTION_STATUS = const(2)
AT42QT2120_KEY_STATUS_A     = const(3)
AT42QT2120_KEY_STATUS_B     = const(4)
AT42QT2120_SLIDER_POSITION  = const(5)
AT42QT2120_CALIBRATE        = const(6)
AT42QT2120_RESET            = const(7)
AT42QT2120_LOW_POWER        = const(8)
AT42QT2120_SLIDER_OPTIONS   = const(14)


class AT42QT2120:
    """Driver for the AT42QT2120 capacitive touch sensor."""

    def __init__(self, i2c, change_pin, address=AT42QT2120_I2CADDR_DEFAULT):
        self._i2c = i2c_device.I2CDevice(i2c, address)
        self._1byte_buffer = bytearray(1)
        self._2byte_buffer = bytearray(2)
        self._change_pin = change_pin
        self._slider_wheel_mode_set = False

    def _write_register_byte(self, register, value):
        # Write a byte value to the specifier register address.
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_1_byte_register(self, register):
        '''
        Reads an 8 bit register
        '''
        with self._i2c:
            self._i2c.write(bytes([register]), stop=False)
            self._i2c.readinto(self._1byte_buffer, start=0, end=1)
        return self._1byte_buffer

    def _read_2_byte_register(self, register):
        '''
        Reads an 16 bit register
        '''
        with self._i2c:
            self._i2c.write(bytes([register]), stop=False)
            self._i2c.readinto(self._2byte_buffer, start=0, end=2)
        return self._2byte_buffer

    def _set_key_control(self, key, value):
        '''
        Key control registers are 28-39
        '''
        if key < 0 or key > 11:
            raise ValueError('Key must be a value 0-11.')
        register = key + 28
        self._write_register_byte(register, value)
        return True

    def reset(self):
        """
        Reset the AT42QT2120 into a default state ready to detect touch inputs.
        """
        self._write_register_byte(AT42QT2120_RESET, 0x1)
        return True

    def enable_wheel(self):
        """
        Enables the wheel mode on first 3 channels (0, 1, 2)
        """
        self._write_register_byte(AT42QT2120_SLIDER_OPTIONS, 0xC0)
        self._slider_wheel_mode_set = True
        return True

    def enable_slider(self):
        """
        Enables the slider mode on first 3 channels (0, 1, 2)
        """
        self._write_register_byte(AT42QT2120_SLIDER_OPTIONS, 0x80)
        self._slider_wheel_mode_set = True
        return True

    def get_slider_wheel_position(self):
        """
        Gets the position of the wheel or slider
        """
        if not self._slider_wheel_mode_set:
            raise ValueError('Slider or wheel mode has not been enabled')
        return self._read_1_byte_register(register=AT42QT2120_SLIDER_POSITION)

    def low_power(self, value):
        self._write_register_byte(AT42QT2120_LOW_POWER, value)
        return True

    def change_detected(self):
        if self._change_pin.value:
            return False
        else:
            return True

    def get_firmware_version(self):
        version_byte = self._read_1_byte_register(register=AT42QT2120_FIRMWARE_VERSION)[0]
        return '{0}.{1}'.format(version_byte >> 4, int(bin(version_byte)[4:8]))

    def get_detection_status(self):
        return self._read_1_byte_register(register=AT42QT2120_DETECTION_STATUS)

    def get_key_status(self):
        '''
        Returns list of key status of all keys as booleans. The index of the item
        in the list is the key number. i.e get_key_status()[3] is status of key 3
        '''
        result = self._read_2_byte_register(register=AT42QT2120_KEY_STATUS_A)
        keys_a = [bool(result[0] & (1<<n)) for n in range(8)]
        keys_b = [bool(result[1] & (1<<n)) for n in range(4)]
        keys_a.extend(keys_b)
        return keys_a

    def calibrtate(self):
        self._write_register_byte(AT42QT2120_CALIBRATE, 0x1)
        return True

    def set_touch_enabled(self, key, enabled):
        '''
        Enable or disable touch for a key. If key is disabled it will be used as
        an output.
        '''
        if enabled == True:
            value = 0
        else:
            value = 1
        real_value = '000{0}{1}{2}{3}{4}'.format(0, 0, 0, 0, value)
        self._set_key_control(key, int(real_value, 2))
        return True

    def set_key_gpo(self, key, value):
        '''
        Set a key to be output and GPO high or low.
        '''
        if value not in [0, 1]:
            raise ValueError('Value must be 1 or 0 (high or low)')
        real_value = '000{0}{1}{2}{3}{4}'.format(0, 0, 0, value, 1)
        self._set_key_control(key, int(real_value, 2))
        return True

    def get_key_control(self, key):
        '''
        Key control registers are 28-39
        '''
        if key < 0 or key > 11:
            raise ValueError('Key must be a value 0-11.')
        result = self._read_1_byte_register(register=key + 28)
        return result[0]

    def get_key_detect_threshold(self, key):
        '''
        Key Signal registers are 16-27
        '''
        if key < 0 or key > 11:
            raise ValueError('Key must be a value 0-11.')

        result = self._read_1_byte_register(register=key + 16)
        return result[0]

    def get_key_signal(self, key):
        '''
        Key Signal registers are 52-75
        '''
        if key < 0 or key > 11:
            raise ValueError('Key must be a value 0-11.')
        result = self._read_2_byte_register(register=key + 52)
        return (result[0] << 8) + result[1]
