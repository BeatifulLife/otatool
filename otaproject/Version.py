import MtkUpdate
import SprUpdate
import staticHelper


class Version:
	def __init__(self, localVersionPath, localVersionDeltaPath, serverVersionPath, localOtaFilepath, localAndroidVersion, shouldReplaceCustom=False):
		self.localVersionPath = localVersionPath
		self.localVersionDeltaPath = localVersionDeltaPath
		self.serverVersionPath = serverVersionPath
		self.isLocalExistsOtaFile = False
		self.localOtaFilepath = localOtaFilepath
		self.shouldReplaceCustom = shouldReplaceCustom
		self.shouldRecopytoServer = False
		self.serverCustomFilePath = ''
		self.customname = ''
		self.projectname = ''
		self.androidversion = staticHelper.AndroidVersion.ANDROID_NONE
		self.MtkUpdate = None
		self.SprUpdate = None

	def setMtkUpdate(self, mtkupdate: MtkUpdate):
		self.MtkUpdate = mtkupdate

	def setSprUpdate(self, sprupdate: SprUpdate):
		self.SprUpdate = sprupdate


