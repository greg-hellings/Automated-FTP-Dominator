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
from gui.dialogs.DomEditEntry import DomEditEntryDialog

class Config(QtGui.QMainWindow):
	changes = None
	configObject = None
	_configname = 'default'
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
		#self.siteList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		
		# Main vertical layout
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(conf_hbox)
		vbox.addWidget(self.siteList)
		#vbox.addStretch(1)		# This allows us to not occupy the entire vertical space of the window.
		vbox.addLayout(save)
		centralWidget = QtGui.QWidget(self)
		centralWidget.setLayout(vbox)
		self.setCentralWidget(centralWidget)
		
		if len(self._config._list) > 0: self.activateConfig(self.conf_list.currentText())
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
		self.connect(self.conf_list, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.activateConfig)
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
		# The + and - buttons
		addButton = QtGui.QPushButton(QtGui.QIcon('icons/add_16x16.png'), 'Add Entry')
		self.connect(addButton, QtCore.SIGNAL('clicked()'), self.addEntry)
		editButton = QtGui.QPushButton(QtGui.QIcon('icons/edit_16x16.png'), 'Edit Entry')
		self.connect(editButton, QtCore.SIGNAL('clicked()'), self.editEntry)
		delButton = QtGui.QPushButton(QtGui.QIcon('icons/delete_16x16.png'), 'Delete Entry')
		self.connect(delButton, QtCore.SIGNAL('clicked()'), self.delEntry)
		hbox.addWidget(addButton)
		hbox.addWidget(editButton)
		hbox.addWidget(delButton)
		
		# Now the save button
		hbox.addStretch(1)
		saveButton = QtGui.QPushButton('Save Changes')
		self.connect(saveButton, QtCore.SIGNAL('clicked()'), self.saveConfig)
		hbox.addWidget(saveButton)
		
		return hbox

	# Listens for changes in the active configuration and will update the UI to reflect that
	def activateConfig(self, config):
		# Confirm that we want to discard the changes
		if not self._confirmDiscardChanges():
			return None
		
		# Having attained that permission, let us proceed onward with great haste
		try:
			self.configObject = self._config.getConfig(str(config))
		except Exception:
			QtGui.QMessageBox.critical(self, 'Error', 'Error opening config file.')
			self.configObject = None
		self.siteList.clear()
		if self.configObject != None:
			for entry in self.configObject:
				QtGui.QListWidgetItem(entry['name'] + '\t' + entry['destination'], self.siteList)
		else:
			self.configObject = []
		# We don't have changes anymore
		self.changes = False
		self._configname = config

	###############################################################################################################################
	################################################### Listeners #################################################################
	###############################################################################################################################
	# Slot where the new button signal is connected
	def newConfig(self):
		# Confirm that it's OK for us to discard changes
		if not self._confirmDiscardChanges(): return None
		name, ok = QtGui.QInputDialog.getText(self, 'New Config', 'Name of new configuration', QtGui.QLineEdit.Normal, 'default')
		name = name.simplified()
		if ok and name != '':
			self._configname = name
			self.configObject = []
			self.conf_list.addItem(name)

	def saveConfig(self):
		self._config.saveConfig(self._configname, self.configObject)
		QtGui.QMessageBox.information(self, 'Saved', 'Configuration saved')
		self.changes = False
	
	# Displays a dialog that will allow the user to
	# create a new element in the current configuration
	def addEntry(self):
		dialog = DomEditEntryDialog(self, None)
		value = dialog.exec_()
		
		# Only if the user really pushed the 'OK' or 'Enter' button/key
		if value == QtGui.QDialog.Accepted:
			name = dialog.getSiteName()
			value = dialog.getSiteURL()
			user = dialog.getUser()
			pw   = dialog.getPassword()
			# Makes sure it doesn't duplicate the name of another site
			duplicate = False
			for element in self.configObject:
				if element['name'] == name: duplicate = True
			# Only proceed if we are in a valid place
			if not duplicate:
				self.configObject.append({'name' : str(name), 'destination' : str(value), 'user' : str(user), 'pw' : str(pw)})
				# Displays in the dialog
				QtGui.QListWidgetItem(name + '\t' + value, self.siteList)
				# Flag the current entry as changed
				self.changes = True
			else:
				print 'Duplicate detected'
				QtGui.QMessageBox.warning(self, 'Duplicate Detected', 'That entry already exists, ignoring.')
		else:
			print 'Rejecting'
	
	def delEntry(self):
		item = self.siteList.takeItem(self.siteList.currentRow())
		text = str(item.text())
		name, trash, url = text.partition('\t')
		# Remove from our list
		for obj in self.configObject:
			if obj['name'] == name: self.configObject.remove(obj)
		# Make sure we know there are changes pending
		self.changes = True
	
	def editEntry(self):
		# Find out which one we're on
		item = self.siteList.currentItem()
		name, trash, url = str(item.text()).partition('\t')
		entry = None
		for obj in self.configObject:
			if obj['name'] == name: entry = obj
		# Create & show the dialog
		dialog = DomEditEntryDialog(self, entry)
		value = dialog.exec_()
		
		# Process answers
		if value == QtGui.QDialog.Accepted:
			# Iterate over the configs
			for obj in self.configObject:
				if obj['name'] == name:
					idx = self.configObject.index(obj)
					self.configObject[idx]['name'] = str(dialog.getSiteName())
					self.configObject[idx]['destination'] = str(dialog.getSiteURL())
					self.configObject[idx]['user'] = str(dialog.getUser())
					self.configObject[idx]['pw'] = str(dialog.getPassword())
					item.setText(self.configObject[idx]['name'] + '\t' + self.configObject[idx]['destination'])
					break
	
	#########################################################################################################################################
	##################################################### Other Helper Functions ############################################################
	#########################################################################################################################################
	def _confirmDiscardChanges(self):
		# This is the first execution
		if self.changes == None:
			self.changes = False
			return True
		elif self.changes == True:
			# Ask the user if they wish to discard the changes
			ok = QtGui.QMessageBox.question(self, 'Confirm Discard', 'Are you sure you wish to discard unsaved changes?', 'Yes', 'No')
			if ok == 0:
				return True
			else:
				return False
		else:
			# There are no changes, we can proceed
			return True