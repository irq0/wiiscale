#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
import select

import xwiimote

def dev_is_balanceboard(dev):
    time.sleep(2) # if we check the devtype to early it is reported as 'unknown' :(

    iface = xwiimote.iface(dev)
    return iface.get_devtype() == 'balanceboard'

def wait_for_balanceboard():
    print("Waiting for balanceboard to connect..")
    mon = xwiimote.monitor(True, False)
    dev = None

    while True:
        mon.get_fd(True) # blocks
        connected = mon.poll()

        if connected == None:
            continue
        elif dev_is_balanceboard(connected):
            print("Found balanceboard:", connected)
            dev = connected
            break
        else:
            print("Found non-balanceboard device:", connected)
            print("Waiting..")

    return dev


def print_bboard_measurements(tl, tr, bl, br):
        print("┌","─" * 10, "┬", "─" * 10, "┐", sep="")
        print("│{:^10}│{:^10}│".format(tl, tr))
        print("│"," " * 10, "│", " " * 10, "│", sep="")
        print("│"," " * 10, "│", " " * 10, "│", sep="")
        print("│{:^10}│{:^10}│".format(bl, br))
        print("└","─" * 10, "┴", "─" * 10, "┘", sep="")
        print("{:^24}".format(sum((tl,tr,br,bl))))

        print()
        print()



def event_loop(iface):
    p = select.epoll.fromfd(iface.get_fd())

    while True:
        p.poll() # blocks

        event = xwiimote.event()
        iface.dispatch(event)

        tl = event.get_abs(2)[0]
        tr = event.get_abs(0)[0]
        br = event.get_abs(3)[0]
        bl = event.get_abs(1)[0]
        sm = sum((tl, tr, br, bl))

        print_bboard_measurements(tl, tr, br, bl)

def main():

    if len(sys.argv) == 2:
        device = sys.argv[1]
    else:
        device = wait_for_balanceboard()

    iface = xwiimote.iface(device)
    iface.open(xwiimote.IFACE_BALANCE_BOARD)

    try:
        event_loop(iface)
    except KeyboardInterrupt:
        print("Bye!")

if __name__ == '__main__':
    main()
