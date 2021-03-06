import urllib2
import logging

from Config import config


def get(url, accept="application/json"):
    logging.debug("Get %s" % url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', "Phantom %s (https://github.com/shiftcurrency/phantom)" % config.version)
    req.add_header('Accept', accept)
    return urllib2.urlopen(req)
