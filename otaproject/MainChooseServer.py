import os

import staticHelper
from Version import Version
from pathHelper import pathHelper


class MainChooseServer:
    def __init__(self):
        self.oldversion = None
        self.newversion = None
        #仅仅是左测试包时需要修改两处版本号
        self.isAdupsFota = False
        self.isMakeTestDelta = False

    def checkOtaVersion(self):
        self.checkVersionIsComplete(self.oldversion)
        if not self.isMakeTestDelta:
            self.checkVersionIsComplete(self.newversion)

    def checkVersionIsComplete(self, version: Version):
        if version.androidversion == staticHelper.AndroidVersion.ANDROID_NONE:
            return False
        if version.projectname is None or version.projectname == '':
            return False
        if version.customname is None or version.customname == '':
            return False
        if version.serverVersionPath is not None and pathHelper.isVersionPath(version.serverVersionPath):
            if

        if version.isLocalExistsOtaFile and os.path.exists(version.localOtaFilepath):
            return True
        if os.path.exists(version.serverVersionPath):
            return True

    def checkZipfileIsSame(self, otazippath, orgotazippath):
        otazipfilesize = os.path.getsize(otazippath)
