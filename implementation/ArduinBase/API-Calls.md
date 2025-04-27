# PositionUnit API Commands

## Servo Control

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/setServo?angle=0` | Positions the servo at 0 degrees (minimum) |
| GET | `http://192.168.178.77/setServo?angle=180` | Positions the servo at 180 degrees (maximum) |

## Stepper Motor Control

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/setMotor?position=250` | Moves the motor to absolute position 250 |
| GET | `http://192.168.178.77/setMotor?position=0` | Moves the motor back to the zero position |
| GET | `http://192.168.178.77/setMotor?steps=4096&direction=1` | Moves the motor one full rotation forward |
| GET | `http://192.168.178.77/setMotor?steps=100&direction=-1&speed=75` | Moves the motor 100 steps backward at 75% speed |

## RGB LED Control

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/color?index=0` | Sets the LED to red (preset color) |
| GET | `http://192.168.178.77/hexcolor?hex=%2300FFFF` | Sets the LED to cyan (custom color) |
| GET | `http://192.168.178.77/setBrightness?value=255` | Sets the LED brightness to maximum (255) |

## Button Status

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/getButtonState` | Retrieves the current status of the button (pressed or not) |

## Miscellaneous

| HTTP Method | URL | Description |
|-------------|-----|-------------|
| GET | `http://192.168.178.77/` | Retrieves the main page of the web interface |