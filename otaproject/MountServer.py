from autoOtainfo import autoOtainfo
from mount import Mount
import os


class MountServer:

    @staticmethod
    def mountFileServer():
        if not MountServer.isPathMount(autoOtainfo.LocalDir):
            mount = Mount(autoOtainfo.LocalDir, autoOtainfo.Server, autoOtainfo.UserName, autoOtainfo.Password)
            return mount.doMount()
        else:
            return True

    @staticmethod
    def isPathMount(pathStr):
        return os.path.ismount(pathStr)
