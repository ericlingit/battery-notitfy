import logging
from sys import exit
from time import sleep
from subprocess import run

CHARGING_STATUS = '/sys/class/power_supply/ADP1/online'
BATTERY_CAPACITY = '/sys/class/power_supply/CMB0/capacity'
MAX = 80
MIN = 50

log = logging.getLogger()


def read_stats() -> dict:
    try:
        # Read charger & battery status
        with open(CHARGING_STATUS) as a:
            charging = bool(int(a.readline()))
            log.info(f'Plugged in: {charging}')
        with open(BATTERY_CAPACITY) as b:
            bat_pct = int(b.readline())
            log.info(f'Capacity: {bat_pct}')
        return {'charging': charging, 'bat_pct': bat_pct}
    except Exception as e:
        # Exit on error
        exit(f'Error reading power stats: {e}')

# Run continuously
while True:
    # Get power stats
    stats = read_stats()

    # Determine what to notify.
    if stats['charging']:
        log.info('Battery is charging.\n')
        # Check battery percentage
        if stats['bat_pct'] > MAX:
            # Show notification pop up
            run(['notify-send', f'Battery above {MAX}%, stop charging.'])
    else:
        log.info('Battery is discharging.\n')
        # Check battery percentage
        if stats['bat_pct'] <= MIN:
            # Show notification pop up
            run(['notify-send', f'Battery below {MIN}%, start charging.'])

    # Sleep 5 minutes
    sleep(300)
