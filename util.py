import sys
import time


def is_windows():
    return sys.platform == 'win32'


def exit_printing_error(msg):
    print(msg)
    sys.exit(1)

if is_windows():
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time
