# Network utilities.
#
# Copyright (c) 2017 Jan A. Humpl <jan.a.humpl@centrum.cz>
#
# Distributed under terms of the MIT license.

import socket
import network


def wget(host, path):
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def wait_for_network():
    if_cli = network.WLAN(network.STA_IF)
    start = utime.ticks_ms()
    while (not if_cli.isconnected()) & \
          (utime.ticks_diff(utime.ticks_ms(), start) < WAIT_MS):
        pass
    if if_cli.isconnected():
        print('Network is connected: ', if_cli.ifconfig())
        status = True
    else:
        print('No network.')
        status = False
    return status
