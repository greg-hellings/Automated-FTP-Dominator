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
# A single function which has knowledge of the
# different types of transport layers this program
# will support and can handle them all in one fell
# swoop

from urlparse import urlparse
from ftppublisher import DomFTP

def publish(destination, source):
	parsed = urlparse(destination['destination'])
	
	if parsed.scheme == 'ftp':
		trans = DomFTP(destination)
		return trans.publish(source)
	else:
		print('Unknown transport scheme')
		return (False, 'Unknown transport scheme')

# This doesn't work since the change to not using straight URLs
#import sys
#if sys.argv[0] == './publisher.py':
#	if len(sys.argv) != 3:
#		print('Usage: ./publish.py [url] [file]')
#	else:
#		if publish(sys.argv[1], sys.argv[2]): print('Test successful')
#		else: print('Test failed. Check error messages')