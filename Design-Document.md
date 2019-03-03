# Battery Notify Design Document

Last updated: 2019-03-03

## Overview

This app reminds you to charge the battery when it runs down to 40%. The app will notifie you to stop charging when the battery has reached 60%.

Note: this app is a practice project. It might not work correctly (or run at all). This design document itself is also a practice piece.

## Context

To maintain maximum battery life, it's best to keep it charged between 40%-60%. Never keep it completely full or empty. This introduces stresses to the battery and makes it degrade faster. See this ArsTechnica article on [the best way to use a lithium-ion battery, redux](https://arstechnica.com/gadgets/2014/04/ask-ars-the-best-way-to-use-a-lithium-ion-battery-redux/).

Most laptops with Windows preinstalled have some kind of firmware utility that can either stop charging when the battery reaches 80%, or limit the charging range to extend the battery's life. For most laptops, this utility stops working if you shutdown the computer or dual boot into Linux (i.e., stop running Windows).

## Goals and non-goals

#### Will do
- Remind the user to plug in or unplug the laptop charger when the battery reaches predefined minimum or maximum threshold.

#### Won't do
- Automatically start/stop charging when the thresholds are reached. This is probably firmware-level stuff. My code-fu isn't remotely there yet.

## Milestones
1. Poll and print the battery status on-demand.
1. Access system notification to display a pop up on-demand.
1. Run as a service.
1. Display a system notification to start/stop charging the battery.

## Technical architecture
1. User disconnects the computer from charger and turns it on.
1. User logs into Ubuntu.
1. User launches this app. It continues to run in the background.
1. User uses the computer for an extended period of time, draining the battery. Battery status reaches 40%. On this event, the app calls system notification stack and displays a reminder to start charging the laptop. e.g., "Battery at 40%, plug in the charger."
1. User continue to use the laptop and let it charge. The battery reaches 60%.
1. On this event, the app calls system notification stack and displays a reminder to stop charging the laptop. e.g., "Battery at 60%, unplug the laptop."

## Testing, monitoring, and alerting app status
TBA

## Open questions
- How will this work on different operating systems?

