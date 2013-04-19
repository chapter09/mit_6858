from flask import g, render_template, request
import time

from login import requirelogin
from zoodb import *
from debug import *
from unixclient import call

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            recipient = g.persondb.query(Person)\
                .get(request.form['recipient'])
            if cmp(recipient.username, g.user.person.username) == 0:
                raise ValueError()
            #zoobars > 0 and be digit
            if not request.form['zoobars'].isdigit():
                raise ValueError()
            zoobars = int(request.form['zoobars'])

            balancedb = g.balancedb.query(Balance)
            recipient_blns_obj = balancedb.get(recipient.username)
            sender_blns_obj = balancedb.get(g.user.person.username)

            sender_balance = sender_blns_obj.zoobars - zoobars
            recipient_balance = recipient_blns_obj.zoobars + zoobars
            
            #recipient_balance 
            if sender_balance < 0 or recipient_balance < 0:
                raise ValueError()
           
            #sender_balance_obj.zoobars = sender_balance
            #recipient_balance_obj.zoobars = recipient_balance
           
            token = request.cookies.get("PyZoobarLogin").split("#")[1]
            #log("token is:%s"%token)            
            msg = 'modify@#' \
                + g.user.person.username + "@#" \
                + str(sender_balance) + "@#" \
                + token
            resp = call("blnssvc/sock", msg).strip()
            log("-------- msg: %s Response = %s" % (msg,resp))
            if not resp:
               raise ValueError()
            
            msg = 'modify@#' \
                + recipient.username + "@#" \
                + str(recipient_balance) + "@#" \
                + token
            resp = call("blnssvc/sock", msg).strip()
            log("-------- Response = %s" % resp )
           
            balancedb = balance_setup()
            log("test %d"% balancedb.query(Balance)\
                .get(g.user.person.username).zoobars)
            log("test %d"% balancedb.query(Balance)\
                .get(recipient.username).zoobars)
            #transfer = Transfer()
            #transfer.sender = g.user.person.username
            #transfer.recipient = recipient.username
            #transfer.amount = zoobars
            #transfer.time = time.asctime()
            #g.transferdb.add(transfer)
            
            msg = g.user.person.username + "@#" \
                + recipient.username + "@#" \
                + str(zoobars)

            resp = call("logsvc/sock", msg).strip()
            log("-------- Response = %s" % resp )
           
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError) as e:
        log("Transfer exception: %s" % str(e))
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
