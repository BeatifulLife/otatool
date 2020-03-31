from ConsolSys import ConsolSys
from ConsolItemInfo import ConsolItemInfo
from ConsolParent import ConsolParent
from MountServer import MountServer
from VersionChooseServer import VersionChooseServer


class VersionChooseConsol(ConsolParent):
    def __init__(self):
        self.consolItemList = [
            ConsolItemInfo("P)上一层目录", "P", "listPreviousDir", 0, True),
            ConsolItemInfo("O)OTA目录", "O", "listOtaDir", 0, True),
            ConsolItemInfo("R)根目录", "R", "listRootDir", 0, True),
            ConsolItemInfo("*)或直接输入目录", "*", "listRelativeDir", 1, True)
        ]
        self.consolsys = ConsolSys(self, VersionChooseServer())

    def doInit(self):
        # 保证挂载
        MountServer.mountFileServer()
        self.consolsys.setConsolInfoList(self.consolItemList)

    def doExit(self):
        self.consolsys.clearConsolInfoList()
        #保证卸载
        pass

    def doRun(self):
        self.consolsys.doRawInput()


