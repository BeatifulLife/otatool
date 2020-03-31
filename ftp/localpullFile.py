from mount import *
from autoOtainfo import *

import re

class localPullFile:
	def __init__(slef):
		self.mount=Mount(Localdir,Server,Username,Password)
		self.hasmount = False

	def Mount(self):
		if not self.hasmount:
			self.hasmount=self.mount.doMount()
		return self.hasmount

	

