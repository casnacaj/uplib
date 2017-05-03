# Helper function to switch device into deepsleep or leave it awake
# (if jumper is installed).
#
# User may use the following functions:
#
# enable_jumper(pin_in=-1, pin_out=-1)
# enable_probe_period(time)
# disable_sleep(status = True)
# sleep(sleep_time, callback=None)
#
# Copyright (c) 2017 Jan A. Humpl <jan.a.humpl@centrum.cz>
#
# Distributed under terms of the MIT license.

import machine
from machine import Pin
from machine import RTC
from machine import Timer
import utime


g_sleep_time = 60       # Wake-up period.
g_pin_in = -1           # Jumper input GPIO number.
g_pin_out = -1          # Jumper output GPIO number.
g_prevent_sleep = False # Prevent sleeping some time after reset.
g_disable_sleep = False # Disable sleeping in general.
g_callback = None       # Wake-up callback function.


# Enables 'stay awake' jumper.
# pin_in - Input GPIO number.
# pin_out - Output GPIO number.
# The jumper should be installed between pin_in and pin_out or
# between pin_in and GND in case, that pin_out = -1.
def enable_jumper(pin_in=-1, pin_out=-1):
    global g_pin_in
    global g_pin_out
    g_pin_in = pin_in
    g_pin_out = pin_out


# Returns true if the jumper is installed.
# The jumper pins must be configured first.
def is_jumper():
    global g_pin_in
    global g_pin_out
    jumper = True

    # If IN pin is not set then the jumper detection is not enabled.
    if g_pin_in < 0:
        jumper = False
    # If OUT pin is not set (just IN pin is set) then
    # IN pin connected to ground means that the jumper is installed.
    elif g_pin_out < 0:
        p_in = Pin(g_pin_in, Pin.IN, Pin.PULL_UP)
        jumper = p_in.value() == 0
    # If both IN and OUT pins are set then
    # the jumper should connect both pins.
    else:
        p_in = Pin(g_pin_in, Pin.IN)
        p_out = Pin(g_pin_out, Pin.OPEN_DRAIN)
        p_out.value(0)
        if (p_in.value() != 0):
            jumper = False
        p_out.value(1)
        if (p_in.value() != 1):
            jumper = False

    return jumper


# Enable 'probe period' after reset - for that time the device will not sleep
# so user may connect with REPL and use function disable_sleep().
def enable_probe_period(time):
    global g_prevent_sleep
    g_prevent_sleep = True
    tim = Timer(-1)
    tim.init(period=time*1000, mode=Timer.ONE_SHOT, callback=probe_timeout)


# Callback function for enabe_probe_period() timeout.
def probe_timeout():
    global g_prevent_sleep
    g_prevent_sleep = False


# Use this function from command promt to disable sleeping at all.
def disable_sleep(status = True):
    global g_disable_sleep
    g_disable_sleep = status


# Return True in case that device should stay awake (deepsleep is disabled
# for any reason).
def should_stay_awake():
    global g_prevent_sleep
    global g_disable_sleep

    stay_awake = False

    if is_jumper() | g_prevent_sleep | g_disable_sleep:
        stay_awake = True

    return stay_awake


# Turn device into deepsleep.
def deepsleep():
    print('The device will now sleep.')
    rtc = RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, g_sleep_time*1000)
    machine.deepsleep()


# Plan next cycle and return (so terminal is functional).
def snooze():
    print('The device should stay awake (jumper detected).')
    tim = Timer(-1)
    tim.init(period=g_sleep_time*1000, mode=Timer.ONE_SHOT, callback=evaluate)


# Execute and plan next cycle.
def evaluate(unused):
    global g_callback

    stay_awake = should_stay_awake()

    if g_callback != None:
        g_callback()

    if stay_awake:
        snooze()
    else:
        deepsleep()


# Call this function to switch device into deepsleep and run the callback
# function periodically.
def sleep(sleep_time, callback=None):
    global g_sleep_time
    global g_callback
    g_sleep_time = sleep_time
    g_callback = callback

    evaluate(None)
