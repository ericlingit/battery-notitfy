# Battery Notify

## Overview

This script displays a notification to remind you to plug or unplug the charger when the battery level goes below 50% or above 60%.

## Context

To maintain maximum battery life, it's best to keep it charged between 50%-80%. Keep it completely full (or empty) stresses the battery, and makes it degrade faster. See this ArsTechnica article on [the best way to use a lithium-ion battery, redux](https://arstechnica.com/gadgets/2014/04/ask-ars-the-best-way-to-use-a-lithium-ion-battery-redux/).

Most laptops with Windows preinstalled have some kind of firmware utility that can either stop charging when the battery reaches 80%, or limit the charging range to extend the battery's life. This utility stops working if you dual boot into Linux.

## Goals and non-goals

#### Will do
- Remind the user to plug in or unplug the laptop charger when the battery reaches predefined minimum or maximum threshold.
- Work with my model of LG Gram laptop.

#### Won't do
- Automatically start/stop charging when the thresholds are reached. This is probably firmware-level stuff. My code-fu isn't remotely there yet.
- Work with other laptop brands/models.

## Milestones
- [x] Poll and print the battery status.
- [x] Determine when to notify start/stop charging.
- [x] Display a system notification.
- [x] Run continuously
- [x] Autostart (`systemd`)

## Technical Architecture (WIP)
- Target operating system: Ubuntu 18.04 x64
- Target hardware: 2018 LG Gram
- Programming language: python 3.7

Source of battery stats:

`/sys/class/power_supply/CMB0/capacity`

`capacity` is a text file that contains a value (0 - 100). It represents the current battery charge level. On other systems, the battery stats may be listed under a `BAT0` directory.

Source of AC adapter state:

`/sys/class/power_supply/ADP1/online`

`online` is a text file that contains a value (0 - 2). It represents the state of power supply (VBUS):

- 0: Unplugged
- 1: Plugged in: Fixed Voltage Supply
- 2: Plugged in: Programmable Voltage Supply

Reference: https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power

#### Usage Scenario

1. User disconnects the laptop from charger and powers it on.
1. User logs into Ubuntu.
1. System launches Battery Notify in the background. It checks the following stats continuously every 5 minutes:
    - whether the laptop is plugged in
    - the current battery capacity reading
1. Battery runs down to 40%. On this event, the app calls system notification stack to display a reminder to start charging the laptop. e.g., "Battery at 40%, plug in the charger."
    - The easiest way to [display a notification popup](https://askubuntu.com/a/616996) is to utilize ubuntu's [`notify-send`](https://manpages.ubuntu.com/manpages/xenial/man1/notify-send.1.html) command. Try running this in a terminal: `notify-send abcxyz`. To call it from a python app, import the `subprocess` module.
    - Another way is to `pip install python3-notify2` and use that. [Docs](https://pypi.org/project/notify2/).
1. User connects the laptop to a charger to charge the laptop while using it. The battery reaches 60%. On this event, the app calls system notification stack to display a reminder to stop charging the laptop. e.g., "Battery at 60%, unplug the charger."


## Installation
1. `chmod +x battery-notify.sh`
1. `sudo cp battery_notify.py /usr/local/src`
1. `sudo cp battery-notify.sh /usr/local/bin/`
1. `sudo cp battery-notify.service /etc/systemd/system/`
1. `sudo systemctl enable battery-notify.service`
