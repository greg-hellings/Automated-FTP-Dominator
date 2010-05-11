#!/usr/bin/python3.1
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

import json
import sys
import os
from publisher.publisher import publish

def get_config():
	path = os.path.expanduser("~/.automated-ftp-dominator/profiles/default")
	with open(path, 'r') as f:
		return json.load(f)

def __main__():
	# Read configuration
	config = get_config()
	where = sys.argv[1]
	# Iterate over each entry
	for site in config:
		publish(site['destination'], where)

def __usage__():
	print('Usage: {} <what to upload>'.format(sys.argv[0]))
	sys.exit(0)
	
if len(sys.argv) == 2:
	__main__()
else:
	__usage__()