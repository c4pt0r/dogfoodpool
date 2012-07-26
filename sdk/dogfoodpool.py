#encoding=utf-8
import os
import urllib
import urllib2

G_SERVER = None
G_PORT = None
G_URL = None
# product name
G_PN = None

def setup_system(host, pn):
    global G_SERVER, G_PORT, G_URL, G_PN
    G_SERVER = host[0]
    G_PORT = host[1]
    G_URL = 'http://' + host[0] + ':' + host[1]
    G_PN = pn

def do_action(action):
    fp = urllib2.urlopen('%s/action/%s/%s' % (G_URL, pn, action))
    return fp.read()

def is_in_whitelist(uname):
    fp = urllib2.urlopen('%s/%s/whitelist?u=' % (G_URL, pn,uname))
    return fp.read()
