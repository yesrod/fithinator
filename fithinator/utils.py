import sys
from datetime import datetime

def debug_msg(c, message):
    if c.debug:
        print("%s %s::%s: %s" % (datetime.now().isoformat(' '), c.__class__.__name__, sys._getframe(1).f_code.co_name, message))
