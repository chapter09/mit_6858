#!/usr/bin/python

from unixclient import call



msg = 'modify@#' \
    + "test1" + "@#" \
    + str(2)
resp = call("/jail/blnssvc/sock", msg)
print "Response = ", resp

