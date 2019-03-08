from sys import exit
from time import sleep
from subprocess import run

CHARGING_STATUS = '/sys/class/power_supply/ADP1/online'
BATTERY_CAPACITY = '/sys/class/power_supply/CMB0/capacity'

def read_stats():
    try:
        # Read charger & battery status
        with open(CHARGING_STATUS, 'r') as a:
            charging = bool(int(a.readline()))
            print(f'Plugged in: {charging}')
        with open(BATTERY_CAPACITY, 'r') as b:
            bat_pct = int(b.readline())
            print(f'Capacity: {bat_pct}')
        return {'charging': charging, 'bat_pct': bat_pct}
    except Exception as e:
        # Exit on error
        exit(f'Error reading power stats: {str(e)}')

# Run continuously
while True:
    # Get power stats
    stats = read_stats()

    # Determine when to notify start/stop charging.
    # Check whether charging:
    if stats['charging']:
        print('Battery is charging.\n')
        # Check battery percentage
        if stats['bat_pct'] >= 60:
            # Show notification pop up
            run(['notify-send', 'Battery above 60%, stop charging!'])
    else:
        print('Battery is discharging.\n')
        # Check battery percentage
        if stats['bat_pct'] <= 40:
            # Show notification pop up
            run(['notify-send', 'Battery below 40%, start charging!'])

    # Sleep 5 minutes
    sleep(300)
