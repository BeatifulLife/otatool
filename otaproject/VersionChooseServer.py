import staticHelper
from filePolicy import *
from pathHelper import pathHelper


class VersionChooseServer:
	def __init__(self):
		self.currdir = autoOtainfo.LocalDir
		if autoOtainfo.LocalDir.endswith("/"):
			self.currdir = self.currdir[0:len(self.currdir)-1]
		self.rootDirWithourseparate = self.currdir
		self.rootDirwithseparate = self.currdir + "/"
		self.curcachelist = []
		self.allcachelist = []
		self.sortmode = SortMode.SORT_NONE
		self.hasRightOtaZip = False
		self.fpolicy = None

	def setGlobalSortMode(self, sortMode):
		self.sortmode = sortMode

	def getCurList(self):
		if self.rootdir is None or self.rootdir == '':
			self.curcachelist = filePolicy(autoOtainfo.LocalDir)
		else:
			self.curcachelist = filePolicy(self.rootdir)

	def listSpecifyDir(self, dirpath, sortMode=SortMode.SORT_NONE):
		if len(self.curcachelist) > 0 and self.isCurrPathChange(dirpath):
			self.printFileInfos(self.curcachelist)
			num, groups = pathHelper.isVersionPath(dirpath)
			if groups and self.fpolicy:
				self.listVersionOtaDir(dirpath, self.fpolicy)
			return
		shouldlistmatch = False
		if not os.path.exists(dirpath):
			shouldlistmatch = True
		else:
			newpath = self.getCaseSensitivePath(dirpath)
			if newpath:
				dirpath = newpath

		temsortMode = self.sortmode
		if sortMode != SortMode.SORT_NONE:
			temsortMode = sortMode
		if shouldlistmatch:
			matchstr = dirpath[dirpath.rfind("/", 0, len(dirpath)-1)+1:]
			dirpath = dirpath[0:dirpath.rfind("/", 0, len(dirpath)-1)]

		fpolicy = filePolicy(dirpath)
		num, groups = pathHelper.isVersionPath(dirpath)
		if groups:
			fileinfos = fpolicy.getImgFileData(temsortMode)
		else:
			fileinfos = fpolicy.getAllFileInfo()
		if fileinfos:
			self.currdir = dirpath
			self.curcachelist.clear()
			#self.allcachelist.clear()
			for fileinfo in fileinfos:
				#self.allcachelist.append(fileinfo)
				if shouldlistmatch and not fileinfo.filename.upper().startswith(matchstr.upper()):
					continue
				self.curcachelist.append(fileinfo)

		if shouldlistmatch and len(self.curcachelist) == 1:
			self.listSpecifyDir(self.curcachelist[0].abspath)
		else:
			self.printFileInfos(self.curcachelist)
			if groups:
				self.fpolicy = fpolicy
				return self.listVersionOtaDir(dirpath, fpolicy)
			else:
				self.fpolicy = None
				return staticHelper.ConsolReturnValue.CONSOL_NONE

	def listVersionOtaDir(self, versiondir, fpolicy):
		pathhelp = pathHelper()
		if pathhelp.analyzePath(versiondir):
			otadir = pathhelp.getLocalServerOtaFilePath()
			fileinfos, otazipnum = fpolicy.getZipFileData(otadir)
			if not fileinfos:
				otadir = pathhelp.getLocalOtaVersionPtah()
				fileinfos, otazipnum = fpolicy.getZipFileData(otadir)
			if fileinfos:
				self.printZipfileInfos(fileinfos)
				if otazipnum == 1:
					self.hasRightOtaZip = True
					return staticHelper.ConsolReturnValue.CONSOL_NEWTITLE
				else:
					self.hasRightOtaZip = False
					return staticHelper.ConsolReturnValue.CONSOL_NONE

			else:
				print("current Version has no ota zip files!")
				return staticHelper.ConsolReturnValue.CONSOL_NONE
		else:
			print(versiondir + " is not a version path")
			return staticHelper.ConsolReturnValue.CONSOL_NONE

	def listRootDir(self, sortMode=SortMode.SORT_NONE):
		return self.listSpecifyDir(self.rootDirWithourseparate, sortMode)

	def listPreviousDir(self, sortMode=SortMode.SORT_NONE):
		if self.isCurrRootDir():
			return self.listRootDir(sortMode)
		else:
			return self.listSpecifyDir(self.getPreviousDir(), sortMode)

	def listRelativeDir(self, pathstr):
		relapath = self.getRelativeDir(pathstr)
		if relapath.startswith(self.rootDirWithourseparate):
			return self.listSpecifyDir(relapath)
		else:
			print("%s is not in version direct, change to rootdir" % relapath)
			return self.listRootDir()

	def listOtaDir(self, sortMode=SortMode.SORT_NONE):
		return self.listSpecifyDir(autoOtainfo.LocalOtaDir, sortMode)

	def printZipfileInfos(self, fileinfos: [fileInfo]):
		print(fileInfo.getZipTitle())
		if fileinfos:
			for finfo in fileinfos:
				print(finfo.toZipString())

	def printFileInfos(self, fileinfos: [fileInfo]):
		print(fileInfo.getTitle())
		if fileinfos:
			for finfo in fileinfos:
				print(finfo.toString())

	def isCurrRootDir(self, dirpath=None):
		if dirpath is None:
			dirpath = self.currdir
		if dirpath == self.rootDirWithourseparate or dirpath == self.rootDirwithseparate:
			return True
		else:
			return False

	def getPreviousDir(self, path=None):
		assert (self.currdir is not None)
		if path is None:
			path = self.currdir
		if path.startswith(self.rootDirWithourseparate) and len(path) > len(self.rootDirwithseparate):
			path = path[0:path.rfind("/", 0, len(path)-1)]
		else:
			path = self.rootDirWithourseparate
		return path

	def getRelativeDir(self, relapath: str):
		assert (relapath is not None)
		if relapath.startswith(self.rootDirWithourseparate):
			if os.path.exists(relapath):
				relapath = relapath[len(self.rootDirWithourseparate):]
				temdirstr = self.rootDirWithourseparate
			else:
				return self.currdir
		else:
			temdirstr = self.currdir

		temreladirs = relapath.split("/")
		for temdir in temreladirs:
			if temdir == "" or temdir == ".":
				continue
			elif temdir == "..":
				if self.isCurrRootDir(temdirstr):
					return self.rootDirWithourseparate
				else:
					temdirstr = self.getPreviousDir(temdirstr)
			else:
				temdirstr = temdirstr + "/" + temdir
		return temdirstr

	def isCurrPathChange(self, pathStr: str):
		assert (pathStr is
				not None)
		if pathStr.endswith("/"):
			pathStr = pathStr[0:len(pathStr)-1]
		if self.currdir == pathStr:
			return True
		else:
			return False

	#windows文件名不区分大小，需要重新列出文件名
	def getCaseSensitivePath(self, dirpath: str):
		if dirpath and dirpath.startswith(self.rootDirwithseparate):
			temdirpath = dirpath[len(self.rootDirwithseparate):]
			dirpaths = temdirpath.split("/")
			temdirpath = self.rootDirWithourseparate
			for dirp in dirpaths:
				if dirp == '':
					continue
				else:
					filelist = os.listdir(temdirpath)
					for f in filelist:
						if f.upper() == dirp.upper():
							temdirpath += "/" + f
							break
			return temdirpath
		else:
			return None


