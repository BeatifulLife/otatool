from mount import *


class localPullFile:
	def __init__(self):
		self.mount = Mount(autoOtainfo.LocalDir, autoOtainfo.Server, autoOtainfo.UserName, autoOtainfo.Password)
		self.hasmount = False

	def doMount(self):
		if not self.hasmount:
			self.hasmount = self.mount.doMount()
		return self.hasmount

	

