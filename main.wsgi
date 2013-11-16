activate_this = '/Users/hari/3002/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

sys.path.append('/Users/hari/3002/hqserver')

from hqserver import app as application