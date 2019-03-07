from sys import exit
from subprocess import run

CHARGING_STATUS = '/sys/class/power_supply/ADP1/online'
BATTERY_CAPACITY = '/sys/class/power_supply/CMB0/capacity'

try:
    # Read charger & battery status
    with open(CHARGING_STATUS, 'r') as a:
        charging = bool(int(a.readline()))
        print(f'Plugged in: {charging}')
    with open(BATTERY_CAPACITY, 'r') as b:
        bat_pct = int(b.readline())
        print(f'Capacity: {bat_pct}')
except Exception as e:
    # Exit on error
    print(e)
    exit()

# Determine when to notify start/stop charging.
# Check whether charging:
if charging:
    print('Battery is charging.')
    # Check battery percentage
    if bat_pct >= 60:
        print("Battery above 60%, stop charging!")
else:
    print('Battery is discharging.')
    # Check battery percentage
    if bat_pct <= 40:
        print("Battery below 40%, start charging!")

### Use notify-send to display a notification pop up.
run(['notify-send', 'hello world'])

