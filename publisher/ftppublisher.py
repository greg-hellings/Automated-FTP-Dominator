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
# This is the publisher for an FTP stream
#
# You create the publisher by initializing the class
# below.  Give it a URL and a source file, and it
# will get itself setup.  When you're done with all of
# that, then call transmit() and it will perform its
# tasks.

from abstract import DomAbstractPublisher
# Seems better to do this import out here, only once, rather than many times
import ftplib
import os
import sys
import time

class DomFTP(DomAbstractPublisher):
	_source = None
	# Our initial few little thingies to get ourself setup
	def __init__(self, destination):
		self._parse(destination['destination'])
		self.user = destination['user']
		self.passwd = destination['pw']
		self.base = self.path
		self._url = destination['destination']
	
	def publish(self, source):
		start_timer = time.clock()
		# Open the connection to the remote machine
		try:
			ftp = ftplib.FTP(self.host, self.user, self.passwd)
		except ftplib.error_temp:
			print('There was a temporary error from server ' + self.host)
			ftp.close()
			return (False, 'Temporary error ' + self.host)
		except Exception as e:
			print('An unexpected error was returned by ' + self.host)
			print('Message was: %s' % (e,))
			#ftp.close()
			return (False, 'Unexpected error ' + self.host)

		# First we need to change into the remote directory
		try:
			ftp.cwd(self.path)
		except Exception as e:
			print('Unable to change remote directories on ' + self.host)
			ftp.close()
			return (False, 'Invalid directory ' + self.host)
		
		# Begin user output
		#print 'Uploading to {0}://{1}{2}'.format(self.scheme, self.host, self.path),
		# Now we figure out if we're dealing with a single file
		if os.path.isdir(source):
			# Get the full path to where we're going
			path = os.path.realpath(source)
			# Get the directory name
			base, newsource = os.path.split(path)
			# Change into the directory locally
			self._whereami = os.getcwd()
			os.chdir(base)
			# Check for the existence of the directory remotely and create if it's not there
			remote = ftp.nlst()
			if newsource not in remote:
				ftp.mkd(newsource)
			# Now walk the directory
			for root, dirs, files in os.walk(newsource):
				# Create any child directories we need to
				remote = ftp.nlst(root)
				for d in dirs:
					if d not in remote: ftp.mkd(root + '/' + d)
				# Upload any files we need to upload
				for f in files:
					self._publish(os.path.join(root, f), ftp)
					#print('Uploading ' + f + ' from ' + root)
			# Change back to the original directory
			os.chdir(self._whereami)
		else:
			self._publish(source, ftp)
		
		#print('  Complete!')
		ftp.close()
		end_timer = time.clock()
		if end_timer - start_timer < 1:
			time.sleep(1)
		return (True, 'Success')

	def _publish(self, source, ftp):
		''' Despite the distinct similarities between this method and the one above in their
		interfaces, this method should only be used by the internal system.  This one will
		only handle a single file at a time.  The method above is what you want that will handle
		whole directories and directory structures... or at least that is the hope.'''

		# Now try to open the local file
		f = None
		try:
			mode = self._mode(source)
			f = open(source, mode)
		except Exception:
			print('Unable to open local file in ' + mode)
			return False
		
		# If the connection was successful, let us try to upload the file
		try:
			cmd = 'STOR ' + source
			if mode == 'rb':
				ftp.storbinary(cmd, f)
			else:
				ftp.storlines(cmd, f)
		except Exception as e:
			print('Unexpected error while transferring a file to ' + self.host)
			print(e)
			return False
		
		#sys.stdout.write('.') 	# A little something-something to keep the people happy with progress and feedback.  One . per file transferred
		#sys.stdout.flush()
		f.close()	# Take care of dangling file pointers
		return True
