class OtaInfo:

    def __init__(self,otazipfile1=None,otazipfile2=None,otaversion=None,otakeypath=None,otaupdatepath=None,ota_mtk_spr=None):
        self.otazipfile1=otazipfile1
        self.otazipfile2=otazipfile2
        self.otaversion=otaversion
        self.otakeypath=otakeypath
        self.otaupdatepath=otaupdatepath
        self.ota_mtk_spr=ota_mtk_spr

    def setOtafile1(self,otazipfile1):
        self.otazipfile1=otazipfile1

    def setOtafile2(self,otazipfile2):
        self.otazipfile2=otazipfile2

    def setOtaversion(self,otaversion):
        self.otaversion=otaversion

    def setOtaKeypath(self,otakeypath):
        self.otakeypath=otakeypath

    def setOtaUpdatepath(self,otaupdatepath):
        self.otaupdatepath=otaupdatepath

    def setOtaMtkSpr(self,ota_mtk_spr):
        self.ota_mtk_spr=ota_mtk_spr

    def getOtafile1(self):
        return self.otazipfile1

    def getOtafile2(self):
        return self.otazipfile2

    def getOtaversion(self):
        return self.otaversion

    def getOtakeypath(self):
        return self.otakeypath

    def getOtaupdatepath(self):
        return self.otaupdatepath

    def getOtaMtkSpr(self):
        return self.ota_mtk_spr

