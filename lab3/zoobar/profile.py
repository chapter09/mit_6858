from flask import g, request
from debug import *

import pypysandbox

def run_profile(user):
    try:
        pcode = user.profile.encode('ascii', 'ignore')
        pcode = pcode.replace('\r\n', '\n')
        token = request.cookies.get("PyZoobarLogin").split("#")[1]

        return pypysandbox.run(user.username, pcode,
                               [ 'ZOOBAR_SELF=' + user.username,
                                 'ZOOBAR_VISITOR=' + g.user.person.username,
                                 'SELF_TOKEN=' + token])
    except Exception, e:
        return 'Exception: ' + str(e)
