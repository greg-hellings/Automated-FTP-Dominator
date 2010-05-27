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

from PyQt4 import QtGui, QtCore
from config import DomConfigurator

# Helper class that lets us save more data along with the widgets
class MyListItem(QtGui.QListWidgetItem):
	data = None
	def __init__(self, data, parent):
		QtGui.QListWidgetItem(data['name'] + '\t' + data['destination'], parent)
		
		self.data = data

# Initial page, wherein the user selects
# the destinations
class FirstPage(QtGui.QWizardPage):
	configBox = None
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.setTitle('Welcome')
		self.setSubTitle('Select where you would like to upload this file to')
		
		self.configManager = DomConfigurator()
		layout = QtGui.QGridLayout(self)
		
		# Combo box
		configLabel = QtGui.QLabel('Choose Configuration')
		self.configBox   = QtGui.QComboBox(self)
		self.populate()
		
		self.connect(self.configBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.changeConfig)
		
		layout.addWidget(configLabel, 0, 0)
		layout.addWidget(self.configBox, 0, 1)
		
		# List
		self.listWidget  = QtGui.QListWidget(self)
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		layout.addWidget(self.listWidget, 1, 0, 1, 3)
		
		# Register fields for access from other pages with the field() method
		self.registerField("config", self.configBox)
		self.registerField("sites", self.listWidget)
		
		# Make us awesome sauce
		self.setLayout(layout)
		
		# And now fill in the suace's secret ingredients
		if len(self.configManager._list) > 0: self.changeConfig(self.configBox.currentText())
	
	def populate(self):
		'''Populates the list of configurations'''
		for config in self.configManager._list:
			self.configBox.addItem(config)
	
	def changeConfig(self, conf):
		'''Listens for a change in the configuration combo box and will
		populate the list of sites to upload to'''
		
		# First we try to get the crap from the file
		try:
			config = self.configManager.getConfig(str(conf))
		except Exception:
			QtGui.QMessageBox.critical(self, 'Error', 'Error reading the config.  Check file permissions or formatting')
			return None
		
		# Now we clear the current ones
		self.listWidget.clear()
		
		# Now we populate the ones from this thingy
		for site in config:
			MyListItem(site, self.listWidget)
		
		# Sort thingies!
		self.listWidget.sortItems()

class SecondPage(QtGui.QWizardPage):
	'''The second page, which asks for any additional path data into which we should be
	uploading to as well as the source directory/file which should be uploaded.'''
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		
		self.setCommitPage(True)

class ThirdPage(QtGui.QWizardPage):
	'''The third (final) page that should have progress bars and things like that which
	will indicate how the upload is progressing.'''
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		
class Wizard(QtGui.QWizard):
	'''The main class for this module.  Just make one, and it'll ask the
	user where to upload the files, which files and so on.'''
	def __init__(self):
		QtGui.QWizard.__init__(self, None)
		self.setWindowTitle('Upload Wizard')
		
		self.addPage(FirstPage(self))
		self.addPage(SecondPage(self))
		
		self.resize(800, 600)