#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import socket
import traceback
import os.path
from datetime import datetime


def submit(path, value, timestamp=datetime.now()):
    unix_ts = timestamp.strftime("%s") # XXX

    for sub in (submit_graphite, submit_append_file):
        sub(path, value, unix_ts)


def submit_append_file(path, value, timestamp):
    filename = "/home/seri/var/weight.log"

    with open(filename, "a") as f:
        simple_file_submit(path, value, timestamp, f)

def simple_file_submit(path, raw_value, timestamp, f=sys.stdout):
    try:
        value = float(raw_value)
    except:
        value = '"{}"'.format(raw_value)
    print(path, value, timestamp, file=f)

def submit_graphite(path, value, timestamp):
    server = ("10.23.1.3", 2003)

    try:
        sock = socket.socket()
        sock.connect(server)
        sock.send("%s %s %s\n" % (path, value, timestamp))
        sock.close()
    except Exception:
        print(traceback.format_exc())
