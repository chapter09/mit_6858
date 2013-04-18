#!/usr/bin/python

import sys
import time

from zoodb import *
from debug import *

req = sys.stdin.read()
msgs = req.split("@#")
transfer = Transfer()
transfer.sender = msgs[0]
transfer.recipient = msgs[1]
transfer.amount = msgs[2]
transfer.time = time.asctime()
db = transfer_setup()
db.add(transfer)
db.commit()

print "You said:", msgs[0], " xxx ", msgs[1], " xxx ", msgs[2]
