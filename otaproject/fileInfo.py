from fileHelper import fileHelper
from otautil import *


class fileInfo:
	def __init__(self, abspath, filesize=0, atime=0, mtime=0, ctime=0):
		self.abspath = abspath
		self.filename = self.getFileName()
		self.isDir = False
		self.filesize = filesize
		self.atime = atime
		self.mtime = mtime
		self.ctime = ctime
		self.Gsize = 1024*1024*1024
		self.Msize = 1024*1024
		self.Ksize = 1204
		self.ziptime = 0
		self.isabnormal = False

	def getFileName(self):
		assert(self.abspath is not None)
		rind = self.abspath.rfind("/")
		if rind != -1:
			return self.abspath[rind+1:]
		else:
			raise Exception("getFileName: Error path,", self.abspath)
			return ''

	def getZipTime(self, name="ota.zip"):
		return otautil.getZipfileStamp(self.abspath, name)

	def setFileAbnormal(self):
		self.isabnormal = True

	def setFileNormal(self):
		self.isabnormal = False

	def Instance(self):
		self.isDir = os.path.isdir(self.abspath)
		self.filesize = fileHelper.getFileSize(self.abspath)
		self.atime = fileHelper.getFileAccessTimeStamp(self.abspath)
		self.ctime = fileHelper.getFileCreateTimeStamp(self.abspath)
		self.mtime = fileHelper.getFileModfifyTimeStamp(self.abspath)
		self.ziptime = self.getZipTime()
		return self

	def toString(self):
		return fileInfo.getStringFormatstr(self.isabnormal) % (self.abspath.ljust(100, " "), str(self.isDir), self.getAdaptSize(),
												otautil.TransToCurTime(self.ctime), otautil.TransToCurTime(self.atime), otautil.TransToCurTime(self.mtime))

	def toZipString(self):
		return fileInfo.getZipStringFormatstr(self.isabnormal) % (self.abspath.ljust(100, " "), self.getAdaptSize(), otautil.TransToCurTime(self.getZipTime()))

	def getAdaptSize(self):
		if self.filesize > self.Gsize:
			return str(round(self.filesize*1.0/self.Gsize, 2))+"GB"
		elif self.filesize > self.Msize:
			return str(round(self.filesize*1.0/self.Msize, 2))+"MB"
		else:
			return str(round(self.filesize*1.0/self.Ksize, 2))+"KB"

	@staticmethod
	def getZipTitle():
		return fileInfo.getZipTitleStringFormatstr() % ('OtaFileName'.ljust(100, " "), 'FileSize', 'FileTime')

	@staticmethod
	def getTitle():
		return fileInfo.getTitleStringFormatstr() % (
			'FileName'.ljust(100, " "), 'isDir', 'FileSize', 'CreateTime', 'AcessTime', 'ModifyTime')

	@staticmethod
	def getStringFormatstr(isAbnormal=False):
		if isAbnormal:
			return '\033[0;31m%s%+20s%+15s%+30s%+30s%+30s\033[0m'
		else:
			return '\033[0;32m%s%+20s%+15s%+30s%+30s%+30s\033[0m'

	@staticmethod
	def getTitleStringFormatstr():
		return '\033[1;35m%s%+20s%+15s%+25s%+30s%+35s\033[0m'

	@staticmethod
	def getZipTitleStringFormatstr():
		return '\033[1;35m%s%+35s%+55s\033[0m'

	@staticmethod
	def getZipStringFormatstr(isAbnormal=False):
		if isAbnormal:
			return "\033[0;31m%s%+35s%+60s\033[0m"
		else:
			return "\033[0;32m%s%+35s%+60s\033[0m"

	@staticmethod
	def getPandaFileNameIndex():
		return 'filename'

	@staticmethod
	def getPandaFileSizeIndex():
		return 'filesize'

	@staticmethod
	def getPandaFileCratetimeIndex():
		return 'creattime'

	@staticmethod
	def getPandaFileAcessTimeIndex():
		return 'accesstime'

	@staticmethod
	def getPandaFileModifyTimeIndex():
		return 'modifytime'

