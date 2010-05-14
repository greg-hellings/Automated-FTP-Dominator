#!/usr/bin/python

from PyQt4 import QtGui
import sys

def __main__():
  app = QtGui.QApplication(sys.argv)
  #configurator = DomConfigurator()
  #configurator.showConfig()
  window = QtGui.QWidget()
  window.setGeometry(100, 150, 600, 400)
  window.setWindowTitle('Configure')
  window.show()

  sys.exit(app.exec_())

__main__()
