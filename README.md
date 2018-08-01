# CircuitPython library for AT42QT2120

![AT42QT2120](../master/images/ic.png?raw=true)

![circuitpython](../master/images/circuitpython.ico?raw=true) CircuitPython library for the AT42QT2120 IC, a capacitive touch controller with 12 buttons.

Product page: https://www.microchip.com/wwwproducts/en/AT42QT2120

### Examples

```python
at42 = at42qt2120.AT42QT2120(i2c, at42_change_pin)

# Detect of any keys are touched
if at42.change_detected():
    print('Touch detected')

# Enable slider or wheel mode. Position is between 0-255
at42.enable_slider()
print(at42.get_slider_wheel_position())

# Get detection signal from key 3. Result is between 0-65535
at42.get_key_signal(3)
```
