#!/usr/bin/python
'''
Copyright 2010 - Greg Hellings

    This file is part of the Automated FTP Dominator.

    The Automated FTP Dominator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    The Automated FTP Dominator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with the Automated FTP Dominator.  If not, see
    <http://www.gnu.org/licenses/>.

'''

import sys
import os
from publisher.publisher import publish
from gui.wizard.upload import Wizard
from config import DomConfigurator
from PyQt4 import QtGui

def __main__():
	app = QtGui.QApplication(sys.argv)

	wizard = Wizard()
	wizard.show()
	# Read configuration
	#configurator = DomConfigurator()
	#config = configurator.getConfig('default')
	#where = sys.argv[1]
	# Iterate over each entry
	#for site in config:
	#	publish(site['destination'], where)
	
	sys.exit(app.exec_())

def __usage__():
	print('Usage: {} <what to upload>'.format(sys.argv[0]))
	sys.exit(0)
	
__main__()