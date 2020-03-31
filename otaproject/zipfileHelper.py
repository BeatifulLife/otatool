import os
import zipfile
import time


class zipfileHelper:
	def __init__(self, zipfilename):
		self.zipfilename = zipfilename
		self.zipfileInfo = self.readZip()

	def readZip(self):
		assert(os.path.extists(self.zipfilename))
		zip=zipfile.ZipFile(self.zipfilename, 'r')
		zipinfo = zip.infolist()
		zip.close()
		return zipinfo

	def getZipFileTimeStamp(self, filename):
		assert(filename is not None)
		timestamp = 0
		for zfile in self.zipfileInfo:
			if filename == zfile.filename:
				timestr = ""
				for i in range(6):
					timestr += str(zfile.date_time[i])+"-"
				timestruct = time.strptime(timestr, "%Y-%m-%d-%H-%M-%S-")
				timestamp = int(time.mktime(timestruct))
				break
		assert(timestamp > 0)
		return timestamp

