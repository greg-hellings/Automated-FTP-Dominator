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
		
		self._original = entry
		
		grid = QtGui.QGridLayout()
		
		nameLabel	= QtGui.QLabel('Name: ')
		self._nameBox	= QtGui.QLineEdit()
		
		urlLabel	= QtGui.QLabel('URL: ')
		self._urlBox	= QtGui.QLineEdit()
		
		# Add the things to the Grid layout
		grid.addWidget(nameLabel, 0, 0)
		grid.addWidget(self._nameBox, 0, 1, 1, 2)
		grid.addWidget(urlLabel, 1, 0)
		grid.addWidget(self._urlBox, 1, 1, 1, 2)
		
		# Add the OK/Cancel buttons
		ok = QtGui.QPushButton('OK')
		cancel = QtGui.QPushButton('Cancel')
		grid.addWidget(ok, 2, 1)
		grid.addWidget(cancel, 2, 2)
		
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