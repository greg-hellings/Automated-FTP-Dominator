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

class DomEditEntryDialog(QtGui.QDialog):
	_original = None
	_name = None
	_value = None
	def __init__(self, parent, entry):
		QtGui.QDialog.__init__(self, parent)
		
		if entry != None:
			self._original = entry
			edit = True
		else:
			self._original = {'name' : '', 'user' : '', 'pw' : '', 'destination' : ''}
			edit = False
		
		grid = QtGui.QGridLayout()
		
		nameLabel	= QtGui.QLabel('Name: ')
		self._nameBox	= QtGui.QLineEdit(self._original['name'])
		if edit:
			self._nameBox.setReadOnly(True)
		
		urlLabel	= QtGui.QLabel('URL: ')
		self._urlBox	= QtGui.QLineEdit(self._original['destination'])
		
		userLabel	= QtGui.QLabel('Username:')
		self._userBox	= QtGui.QLineEdit(self._original['user'])
		
		passLabel	= QtGui.QLabel('Password:')
		self._passBox	= QtGui.QLineEdit(self._original['pw'])
		
		# Add the things to the Grid layout
		grid.addWidget(nameLabel, 0, 0)
		grid.addWidget(self._nameBox, 0, 1, 1, 2)
		grid.addWidget(urlLabel, 1, 0)
		grid.addWidget(self._urlBox, 1, 1, 1, 2)
		grid.addWidget(userLabel, 2, 0)
		grid.addWidget(self._userBox, 2, 1, 1, 2)
		grid.addWidget(passLabel, 3, 0)
		grid.addWidget(self._passBox, 3, 1, 1, 2)
		
		# Add the OK/Cancel buttons
		ok = QtGui.QPushButton('OK')
		cancel = QtGui.QPushButton('Cancel')
		grid.addWidget(ok, 4, 1)
		grid.addWidget(cancel, 4, 2)
		
		# Connect the buttons to the proper slots on the Dialog
		self.connect(ok, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('accept()'))
		self.connect(cancel, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('reject()'))
		
		self.setLayout(grid)
		
		self.setModal(True)
		
		self.show()
	
	#def closeEvent(self, event):
	def done(self, event):
		self._name = self._nameBox.text()
		self._value = self._urlBox.text()
		self._user = self._userBox.text()
		self._pass = self._passBox.text()
		
		#event.accept()
		QtGui.QDialog.done(self, event)
	
	def getSiteName(self):
		if self._name and self._name.trimmed() == '':
			return None
		else:
			return self._name
	
	def getSiteURL(self):
		if self._value and self._value.trimmed() == '':
			return None
		else:
			return self._value
	
	def getUser(self):
		if self._user and self._user.trimmed() == '':
			return None
		else:
			return self._user
	
	def getPassword(self):
		if self._pass and self._pass.trimmed() == '':
			return None
		else:
			return self._pass