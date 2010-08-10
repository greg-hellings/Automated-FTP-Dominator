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
from publisher.publisher import publish
from threading import Thread, Event

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
	domainateParent = None
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.dominateParent = parent
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
		
		self.connect(self.listWidget, QtCore.SIGNAL('itemSelectionChanged()'), lambda: self.emit(QtCore.SIGNAL('completeChanged()')))
		
		# Register fields for access from other pages with the field() method
		self.registerField("config", self.configBox, 'currentText')
		self.registerField("sites", self.listWidget, 'selectedItems', QtCore.SIGNAL('itemSelectionChanged()'))
		
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
	
	def validatePage(self):
		'''Override the base class's method.  Since the field() arguments isn't working, from what I can tell,
		I will do things this way rather than wrestle with that for an indeterminate amount of further time.'''
		# Since the QVariant bullshit in PyQt4 doesn't work the way the C++ examples do, I'm going to
		# say "fuck it" and just do things my way
		self.dominateParent.domConfig = self.configBox
		self.dominateParent.domSites  = self.listWidget
		
		return True
	
	def isComplete(self):
		if len(self.listWidget.selectedItems()) > 0: return True
		else: return False

class LittleLineEdit(QtGui.QLineEdit):
	show = True
	def __init__(self):
		QtGui.QLineEdit.__init__(self)
		
		self.setMinimumWidth(250)
	
	# Listens for when the user clicks and allows them to select
	# a directory which will be uploaded
	def mousePressEvent(self, event):
		QtGui.QLineEdit.mousePressEvent(self, event)
		
		value = QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory to upload')
		self.setText(value)
		
class SecondPage(QtGui.QWizardPage):
	'''The second page, which asks for any additional path data into which we should be
	uploading to as well as the source directory/file which should be uploaded.'''
	dominateParent = None
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.dominateParent = parent
		
		#self.setCommitPage(True)
		self.setSubTitle('Use this page to select which file/folder you wish to upload to the remote locations.  Additionally, you can provide ' +
		'extra path information which will be appended to each of the URLs you selected in the previous screen.')
		self.setTitle('File and Path Selection')

		grid = QtGui.QGridLayout()
		grid.setColumnStretch(0, 1)
		grid.setColumnStretch(6, 1)
		# Line to ask people for additional path elements
		additionalLabel = QtGui.QLabel('Additional path element (optional)')
		self.additional = QtGui.QLineEdit('')
		# Layout the above items
		grid.addWidget(additionalLabel, 0, 1)
		grid.addWidget(self.additional, 0, 2)
		
		# Line to ask people for file path to upload
		sourceLabel     = QtGui.QLabel('Select source file/directory')
		self.source     = LittleLineEdit()
		self.source.setReadOnly(True)
		# Layout the above items
		grid.addWidget(sourceLabel, 1, 1)
		grid.addWidget(self.source, 1, 2)
		
		# Need a layout, don't we?
		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addStretch(1)
		mainLayout.addLayout(grid)
		mainLayout.addStretch(1)
		
		self.setLayout(mainLayout)
		
		# The fields that we will want to access in the future
		self.registerField('additional-path-elements', self.additional)
		self.registerField('source*', self.source)
	def validatePage(self):
		'''See the class SecondPage::validatePage(self) if you want more information'''
		self.dominateParent.domAdditional = str(self.additional.text())
		self.dominateParent.domSource = str(self.source.text())
		
		x = QtGui.QMessageBox.question(self, 'Confirm', 'Beware that if you proceed, the upload will proceed inexorably toward its conclusion.', 2, 0, 1)
		
		return x == 1 # Tests to be sure that the OK button was clicked
		

class ThirdPage(QtGui.QWizardPage):
	'''The third (final) page that should have progress bars and things like that which
	will indicate how the upload is progressing.'''
	dominateParent = None
	finished = False
	def __init__(self, parent):
		QtGui.QWizardPage.__init__(self, parent)
		self.dominateParent = parent
		
		grid = QtGui.QGridLayout()
		
		# Debugging output for now
		#grid.addWidget(QtGui.QLabel('Destinations selected'), 0, 0)
		#self.siteLabel = QtGui.QLabel()
		#grid.addWidget(self.siteLabel, 0, 1)
		
		# Configuration
		#grid.addWidget(QtGui.QLabel('Config selected'), 1, 0)
		#self.configLabel = QtGui.QLabel()
		#grid.addWidget(self.configLabel, 1, 1)
		
		# Additional Path stuffs
		#grid.addWidget(QtGui.QLabel('additional-path-elements'), 2, 0)
		#self.additionalLabel = QtGui.QLabel()
		#grid.addWidget(self.additionalLabel, 2, 1)
		
		# Source directory/file
		#grid.addWidget(QtGui.QLabel('source'), 3, 0)
		#self.sourceLabel = QtGui.QLabel()
		#grid.addWidget(self.sourceLabel, 3, 1)
		
		# Progress Bar
		self.progressBar = QtGui.QProgressBar()
		grid.addWidget(self.progressBar, 4, 0)
		
		# Again button
		againButton = QtGui.QPushButton('Again!')
		grid.addWidget(againButton, 5, 0)
		self.connect(againButton, QtCore.SIGNAL('clicked(bool)'), self.again)
		
		grid.addWidget(QtGui.QLabel('I will now be uploading.  Please be patient, especially if you are uploading a large directory'), 0, 0)
		
		self.setLayout(grid)
		
	def initializePage(self):
		'''Sets the values of the page to be relevant to what we're doing here.  This will probably include the
		calls that will do the uploading and so on and so forth.'''
		self.event = Event()
		osites = self.dominateParent.domSites.selectedItems()
		self.sites = []
		for site in osites:
			name, trash, url = str(site.text()).partition('\t')
			self.sites.append(name)
		self.config = self.field('config').toString()
		self.additional = self.field('additional-path-elements').toString()
		self.source = str(self.field('source').toString())
		
		self.progressBar.setMaximum(len(self.sites))
		self.progressBar.setValue(0)
			
		thread = Worker(self, self.sites, self.config, self.additional, self.source)
		self.connect(thread, QtCore.SIGNAL('updateProgress()'), self.updateProgress)
		thread.start()
		pass
	
	def isComplete(self):
		return self.finished
	
	def updateProgress(self):
		self.progressBar.setValue(self.progressBar.value() + 1)
		
	def again(self, wtf):
		self.progressBar.setValue(0)
		
		thread = Worker(self, self.sites, self.config, self.additional, self.source)
		self.connect(thread, QtCore.SIGNAL('updateProgress()'), self.updateProgress)
		thread.start()
		

class Worker(QtCore.QThread):
	parent = None
	def __init__(self, parent, sites, config, additional, source):
		QtCore.QThread.__init__(self, parent)
		self.parent = parent
		self.exiting = False
		
		self.sites = sites
		self.config = config
		self.additional = additional
		self.source = source

	def __del__(self):
		self.exiting = True
		self.wait()
	
	def run(self):
		# Get our configurations
		configManager = DomConfigurator()
		configObject  = configManager.getConfig(str(self.config))
		
		for destination in configObject:
			if str(destination['name']) in self.sites:
				destination['destination'] = str(destination['destination'].rstrip('/') + '/' + self.additional)
				flag, message = publish(destination, self.source)
				print 'Flag: %s, Message: %s' % (flag, message)
				self.emit(QtCore.SIGNAL('updateProgress()'))
			else:
				print 'Skipping ' + destination['name']
		
		self.parent.finished = True
		self.parent.emit(QtCore.SIGNAL('completeChanged()'))
		
		
class Wizard(QtGui.QWizard):
	domConfig     = None
	domSites      = None
	domAdditional = None
	domSource     = None
	'''The main class for this module.  Just make one, and it'll ask the
	user where to upload the files, which files and so on.'''
	def __init__(self):
		QtGui.QWizard.__init__(self, None)
		self.setWindowTitle('Upload Wizard')
		
		self.addPage(FirstPage(self))
		self.addPage(SecondPage(self))
		self.addPage(ThirdPage(self))
		
		self.resize(800, 600)