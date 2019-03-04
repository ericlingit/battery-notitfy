# Battery Notify Design Document

Last updated: 2019-03-03

## Overview

This app reminds you to charge the battery when it runs down to 40%. The app will notifie you to stop charging when the battery has reached 60%.

Note: this app is a practice project. It might not work correctly (or run at all). This design document itself is also a practice piece.

## Context

To maintain maximum battery life, it's best to keep it charged between 40%-60%. Never keep it completely full or empty. This stresses the battery and makes it degrade faster. See this ArsTechnica article on [the best way to use a lithium-ion battery, redux](https://arstechnica.com/gadgets/2014/04/ask-ars-the-best-way-to-use-a-lithium-ion-battery-redux/).

Most laptops with Windows preinstalled have some kind of firmware utility that can either stop charging when the battery reaches 80%, or limit the charging range to extend the battery's life. For most laptops, this utility stops working if you shutdown the computer or dual boot into Linux (i.e., stop running Windows).

## Goals and non-goals

#### Will do
- Remind the user to plug in or unplug the laptop charger when the battery reaches predefined minimum or maximum threshold.
- Work with my model of LG Gram laptop.

#### Won't do
- Automatically start/stop charging when the thresholds are reached. This is probably firmware-level stuff. My code-fu isn't remotely there yet.
- Work with other laptop brands/models.

## Milestones
- [x] Poll and print the battery status on-demand.
- [x] Determine when to notify start/stop charging.
- [ ] Access system notification to display a pop up on-demand.
- [ ] Run as a service.
- [ ] Display a system notification to start/stop charging the battery.

## Technical Architecture (WIP)

- Target operating system: Ubuntu 18.04 x64
- Target hardware: 2018 LG Gram
- Programming language: python 3.7

Source of battery stats:

`/sys/class/power_supply/CMB0/capacity`

`capacity` contains a value (0 - 100) that represents the current battery capacity percentage. On other systems, the battery stats may be listed under a `BAT0` directory.

Source of AC adapter state:

`/sys/class/power_supply/ADP1/online`

`online` contains a value (0 - 2) that represents the state of power supply (VBUS):

- 0: Unplugged
- 1: Plugged in: Fixed Voltage Supply
- 2: Plugged in: Programmable Voltage Supply

Reference: https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power

#### Usage Scenario

1. User disconnects the laptop from charger and powers it on.
1. User logs into Ubuntu.
1. User launches Battery Notify. It continues to run in the background to check following stats:
    - whether the laptop is plugged in
    - the current battery capacity reading.
1. Battery runs down to 40%. On this event, the app calls system notification stack to display a reminder to start charging the laptop. e.g., "Battery at 40%, plug in the charger."
    - The easiest way to [display a notification popup](https://askubuntu.com/a/616996) is to utilize ubuntu's [`notify-send`](https://manpages.ubuntu.com/manpages/xenial/man1/notify-send.1.html) command. Try running this in a terminal: `notify-send abcxyz`. To call it from a python app, import the `subprocess` module.
    - Another way is to `pip install python3-notify2` and use that. [Docs](https://pypi.org/project/notify2/).
1. User connects the laptop to AC charger and continues to use the laptop. The battery reaches 60%.
1. On this event, the app calls system notification stack to display a reminder to stop charging the laptop. e.g., "Battery at 60%, unplug the laptop."

#### Psudo code

```
# On start: read battery & AC adapter status
bat_pct = open('/sys/class/power_supply/CMB0/capacity', 'r').readline()
ac_stat = open('/sys/class/power_supply/ADP1/online', 'r').readline()

# Run continuously (not sure if proper to use a while loop)
while True:
    # Check whether charging
    if ac_stat:
        # Check battery percentage
        if bat_pct >= 60%:
            notify("Stop charging!")
    else:
        # Check battery percentage
        if bat_pct <= 40%:
            notify("Start charging!")
    sleep(60)
```

## Testing, monitoring, and alerting app status
TBA

## Open questions
- How will this work on different operating systems?
- What if the laptop is indeed charging, but the battery somehow continues to drain?
