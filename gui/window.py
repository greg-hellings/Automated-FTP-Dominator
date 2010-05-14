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

class Config(QtGui.QMainWindow):
	_newconfig = {}
	def __init__(self, config):
		QtGui.QMainWindow.__init__(self, None)
		self._config = config
		
		self.setGeometry(100, 150, 600, 400)
		self.setWindowTitle('Configure Destinations')
		
		# Let's make ourselves a nice little layout
		conf_hbox  = self.getChooser(self)
		
		# Let's make the menubar
		menubar = self.makeMenubar()
		self.setMenuBar(menubar)
		
		# Save changes?
		save = self.makeSaveButton()
		
		self.siteList = QtGui.QListWidget()
		
		# Main vertical layout
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(conf_hbox)
		vbox.addWidget(self.siteList)
		#vbox.addStretch(1)		# This allows us to not occupy the entire vertical space of the window.
		vbox.addLayout(save)
		centralWidget = QtGui.QWidget(self)
		centralWidget.setLayout(vbox)
		self.setCentralWidget(centralWidget)
		
		if len(self._config._list) > 0: self.activateConfig(self._config._list[0])
		else: self.newConfig()

	#################################################################################################################################
	#################################################### UI Helpers #################################################################
	#################################################################################################################################
	
	# Makes the top line chooser/new box
	def getChooser(self, widget):
		conf_hbox = QtGui.QHBoxLayout()
		conf_hbox.addWidget(QtGui.QLabel('Select Configuration'))
		# First we create the label with all the configurations currently available
		self.conf_list = QtGui.QComboBox(widget)
		for this_config in self._config._list:
			self.conf_list.addItem(this_config)
		conf_hbox.addWidget(self.conf_list)
		self.connect(self.conf_list, QtCore.SIGNAL('activated(const QString&)'), self.activateConfig)
		# Populate the first config available

		# And an "Add New" box
		self.conf_newbutton = QtGui.QPushButton('New')
		widget.connect(self.conf_newbutton, QtCore.SIGNAL('clicked()'), self.newConfig) #self, QtCore.SLOT('newConfig()'))
		conf_hbox.addWidget(self.conf_newbutton)
		conf_hbox.addStretch(1)		# This makes the line not take up the entire width of the application

		return conf_hbox

	# Creates a menu bar and returns it to the caller - sadly they only look right if we're working with a QMainWindow
	def makeMenubar(self):
		# Make a new menubar
		menubar = QtGui.QMenuBar()

		# First menu entry - File, as always
		file = menubar.addMenu('&File')

		# Last file entry - as always
		file.addSeparator()
		exit = QtGui.QAction('E&xit', self)
		exit.setShortcut('Ctrl+Q')
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		file.addAction(exit)
		
		return menubar

	# Returns a layout that contains a "Save Contents" button
	def makeSaveButton(self):
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)
		saveButton = QtGui.QPushButton('Save Changes')
		hbox.addWidget(saveButton)
		
		return hbox

	# Listens for changes in the active configuration and will update the UI to reflect that
	def activateConfig(self, config):
		# TODO: Make display thingie
		configObject = self._config.getConfig(config)
		self.siteList.reset()
		for entry in configObject:
			#print entry
			QtGui.QListWidgetItem(entry['name'] + '\t' + entry['destination'], self.siteList)

	###############################################################################################################################
	################################################### Listeners #################################################################
	###############################################################################################################################
	# Slot where the new button signal is connected
	def newConfig(self):
		name, ok = QtGui.QInputDialog.getText(self, 'New Config', 'Name of new configuration', QtGui.QLineEdit.Normal, 'default')
		name = name.simplified()
		if ok and name != '':
			self._newconfig['name'] = name
			self._newconfig['data'] = []
			self.conf_list.addItem(name)

	def saveConfig(self):
		# TODO: Process and save
		pass