# DHT22 wheater sensor advanced read function.
#
# Copyright (c) 2017 Jan A. Humpl <jan.a.humpl@centrum.cz>
#
# Distributed under terms of the MIT license.

import dht
import machine
import utime


def measure(pin):
    status = True
    t = 0
    h = 0
    try:
        d = dht.DHT22(machine.Pin(pin))
        d.measure()
        # The DHT22 returns previous result. The old value may be invalid.
        # So we need to read the value again. The delay betweed two reads must
        # be at leas two seconds.
        utime.sleep(3)
        d.measure()
        t = d.temperature()
        h = d.humidity()
        print('Temperature: ', t, 'C, Humidity: ', h, '%')
    except:
        status = False
        print('DHT22 reading error.')
    return status, t, h
