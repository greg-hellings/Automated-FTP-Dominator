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
import json
from PyQt4 import QtGui
from gui.window import Config

class DomConfigurator:
	_list = []
	def __init__(self):
		self._configpath = os.path.expanduser("~/.automated-ftp-dominator/profiles")
		# Assembles a list of all the files in the configuration directory
		for file in os.listdir(self._configpath):
			if os.path.isfile(os.path.join(self._configpath, file)):
				self._list.append(file)
		
	def getConfig(self, name):
		if name in self._list:
			with open(os.path.join(self._configpath, name), 'r') as f:
				return json.load(f)
		else:
			return None
			
	def saveConfig(self, name, data):
		name = str(name)
		with open(os.path.join(self._configpath, name), 'w') as f:
			json.dump(data, f)
		# Save the name of it
		if name not in self._list:
			self._list.append(name)
		


# This is the entry point if this configuration script is going to be the main
# thing running on the system.  Otherwise, we will not be running this function
# and will instead just be a module which could be imported and used to configure
# a site list.
def __main__():
	app = QtGui.QApplication(sys.argv)
	
	# Create a basic configuration window
	configurator = DomConfigurator()
	config = Config(configurator)
	config.show()
	
	sys.exit(app.exec_())

if sys.argv[0] == './config.py':
	__main__()