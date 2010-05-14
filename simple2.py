#!/usr/bin/python

from PyQt4 import QtGui
import sys

class DomConfigurator:
  def showConfig(self):
    window = QtGui.QWidget()
    window.setGeometry(100, 150, 600, 400)
    window.setWindowTitle('Configure')
    window.show()

def __main__():
  app = QtGui.QApplication(sys.argv)
  configurator = DomConfigurator()
  configurator.showConfig()

  sys.exit(app.exec_())

__main__()

