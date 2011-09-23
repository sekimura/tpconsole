import typepad
import tpconsole as tp

tp.authenticate()
print "Hello, %s" % tp.me()['displayName']


