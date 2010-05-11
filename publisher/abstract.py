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
# This is the abstract base of publisher types.  They are
# required to handle the details of doing the publishing
# of the files themselves, but this will handle some of the
# more mundane details of parsing URLs and the like

class DomAbstractPublisher:
	def _parse(self, url):
		from urllib.parse import urlparse
		
		parsed = urlparse(url)
		self.scheme = parsed.scheme
		self.path   = parsed.path.rstrip('/')
		self.host   = parsed.hostname
		self.user   = parsed.username
		self.passwd = parsed.password
	
	def _mode(self, fname):
		import os
		ext = os.path.splitext(fname)[1]
		#if ext in (".php", ".tpl", "", ".html", ".htaccess", ".py"):
		#	return 'r'
		#else:
		return 'rb'