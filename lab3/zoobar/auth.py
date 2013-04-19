from flask import g
import hashlib
import random
from unixclient import call
from debug import *

from zoodb import *

class User(object):
    def __init__(self):
        self.person = None

    def checkLogin(self, username, password):
        person = g.persondb.query(Person).get(username)
        if not person:
            return None

        msg = 'checklogin@#'\
            + username + "@#"\
            + password
        resp = call("authsvc/sock", msg).strip()
        log("---auth----- Response = %s" % resp)

        if resp == "true":
            return self.loginCookie(person)
        else:
            return None

    def addRegistration(self, username, password):
        person = g.persondb.query(Person).get(username)
        if person:
            return None
        newperson = Person()
        newperson.username = username
        g.persondb.add(newperson)
        msg = 'register@#'\
            + username + '@#'\
            + password
        cookie = call('authsvc/sock', msg).strip()
        log("---auth----- msg: %s Response = %s" % (msg, cookie))

        msg = 'new@#' + username
        resp = call('blnssvc/sock', msg).strip()
        log("---auth----- msg: %s Response = %s" % (msg,resp))

        self.person = newperson
        balancedb = balance_setup()
        newperson.zoobars = balancedb.query(Balance).get(newperson.username).zoobars

        return cookie

    def loginCookie(self, person):
        self.person = person
        msg = 'logincookie@#'\
            + person.username
        resp = call('authsvc/sock', msg).strip()
        log("---auth----- msg: %s Response = %s" % (msg, resp))

        balancedb = balance_setup()
        person.zoobars = balancedb.query(Balance).get(person.username).zoobars
        return "%s#%s" % (person.username, resp)

    def logout(self):
        self.person = None

    def checkCookie(self, cookie):
        if not cookie:
            return

        (username, token) = cookie.rsplit("#", 1)
        person = g.persondb.query(Person).get(username)
        balancedb = balance_setup()
        person.zoobars = balancedb.query(Balance).get(username).zoobars

        msg = 'checkcookie@#'\
            + username + "@#"\
            + token + "@#"
        resp = call('authsvc/sock', msg).strip()

        if resp:
            self.person = person
