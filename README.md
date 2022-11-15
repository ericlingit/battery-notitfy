# Battery Notify

Update: TLP's [battery care](https://linrunner.de/tlp/settings/battery.html) feature automatically starts and stops charging the battery for you. It [supports](https://linrunner.de/tlp/settings/bc-vendors.html#lg) LG Gram laptops as of v1.4. This renders battery-notify obsolete, as it was a stop-gap measure until a permanent solution appears.

## Purpose

battery-notify displays a notification to remind the user to start or stop charging the laptop battery when its level goes below 50% or above 80%.

## Context

To prolong battery life, it's best to keep it charged between 50%-80%. Keeping it completely full (or empty) stresses the battery, and degrades it faster. See this ArsTechnica article on [the best way to use a lithium-ion battery, redux](https://arstechnica.com/gadgets/2014/04/ask-ars-the-best-way-to-use-a-lithium-ion-battery-redux/).

Most laptops with Windows preinstalled have an utility that can stop charging when the battery reaches 80% to extend the battery's life. This utility stops working if you dual boot into Linux.

## Goals

Will do

- Remind the user to start or top charging the laptop when the battery level reaches predefined levels.
- Work with LG Gram 13 (model number 13Z980-U.AAW5U1; released in 2018) laptop running Ubuntu 18.04 or 20.04.

Won't do

- Automatically start/stop charging when the thresholds are reached.
- Work with other laptop brands/models.

## Technical architecture

The current charge state and the battery level are read from the following two files:

- `/sys/class/power_supply/ADP1/online`
    - `online` is a text file that stores a value (0 - 2). It represents the state of power supply (VBUS):
        - 0: Unplugged
        - 1: Plugged in: Fixed Voltage Supply
        - 2: Plugged in: Programmable Voltage Supply
- `/sys/class/power_supply/CMB0/capacity`
    - `capacity` is a text file that stores a value (0 - 100). It represents the current battery charge level. On other systems, the battery stats may be listed under a `BAT0` directory.

Reference: https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power

battery-notify reads the values from the two files and sends a notification using Ubuntu's `notify-send` utility. Message content depends on the charge state and the battery's level. battery-notify then goes to sleep for 5 minutes, and then repeat the above actions.

## battery-notify installation and usage guide

1. `git clone https://github.com/ericlingit/battery-notitfy.git`
1. `cd battery-notify/battery_notify`
1. `chmod +x battery-notify.sh`
1. `sudo cp battery_notify.py /usr/local/src`
1. `sudo cp battery-notify.sh /usr/local/bin/battery-notify`
1. Add `battery-notify` to startup application settings (see screenshot)
1. Logout and log back in for the change to take effect

![img](./startup-app-setting.png)
