from fileInfo import *
import pandas as pd
import re
from staticHelper import *
from otautil import *


class filePolicy:

    def __init__(self, abspath):
        assert (abspath is not None)
        assert (os.path.isdir(abspath))
        if not abspath.endswith("/"):
            self.abspath = abspath + "/"
        else:
            self.abspath = abspath
        self.abnoralImgZipIntervalTime = 60 * 10
        self.imgabnoralIntervalTime = 60 * 2
        #设置最低的复制速度5M/s
        self.abbormalspeed = 5

    def imgFilter(self, filepath):
        if re.match(r'.*.(img|bin)', filepath) and os.path.isfile(filepath):
            return True
        else:
            return False

    def zipFilter(self, filepath):
        if re.match(r'.*.(zip)', filepath) and os.path.isfile(filepath):
            return True
        else:
            return False

    def getAllFileInfo(self, sortmode=SortMode.SORT_NONE):
        fileinfos = []
        if not os.path.exists(self.abspath):
            return None
        filelist = os.listdir(self.abspath)
        for filename in filelist:
            fileinfos.append(fileInfo(self.abspath + filename).Instance())
        if len(fileinfos) == 0:
            return None

        if sortmode == SortMode.SORT_FILENAME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.filename.upper())
            return newfileinfos
        elif sortmode == SortMode.SORT_FILESIZE:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.filesize)
            return newfileinfos
        elif sortmode == SortMode.SORT_CREATETIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.ctime)
            return newfileinfos
        elif sortmode == SortMode.SORT_ACCESSTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.atime)
            return newfileinfos
        elif sortmode == SortMode.SORT_MODIFYTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.mtime)
            return newfileinfos
        elif sortmode == SortMode.SORT_ZIPTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.ziptime)
            return newfileinfos
        else:
            return fileinfos

    def getAllSpecifyFileInfo(self, filefilterMethod, sortmode=SortMode.SORT_NONE, dirpath: str = None):
        assert (filefilterMethod is not None)
        fileinfos = []
        if dirpath is None:
            dirpath = self.abspath
        if not dirpath.endswith("/"):
            dirpath += "/"
        if not os.path.exists(dirpath):
            return None
        filelist = os.listdir(dirpath)
        for filename in filelist:
            if filefilterMethod(dirpath+filename):
                fileinfos.append(fileInfo(dirpath + filename).Instance())
        if len(fileinfos) == 0:
            return None
        if sortmode == SortMode.SORT_FILENAME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.filename.upper())
            return newfileinfos
        elif sortmode == SortMode.SORT_FILESIZE:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.filesize)
            return newfileinfos
        elif sortmode == SortMode.SORT_CREATETIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.ctime)
            return newfileinfos
        elif sortmode == SortMode.SORT_ACCESSTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.atime)
            return newfileinfos
        elif sortmode == SortMode.SORT_MODIFYTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.mtime)
            return newfileinfos
        elif sortmode == SortMode.SORT_ZIPTIME:
            newfileinfos = sorted(fileinfos, key=lambda finfo: finfo.ziptime)
            return newfileinfos
        else:
            return fileinfos

    def trainFileInfo(self, pandafileindex):
        fileinfos = self.getAllSpecifyFileInfo(self.imgFilter)
        assert (len(fileinfos) > 0)
        pandadata = self.getPandaData(fileinfos)
        sepcifypddata = []
        if pandafileindex == PandaFileInfoIndex.ACCESSTIM:
            sepcifypddata = pandadata[fileInfo.getPandaFileAcessTimeIndex()]
        elif pandafileindex == PandaFileInfoIndex.CREATTIME:
            sepcifypddata = pandadata[fileInfo.getPandaFileCratetimeIndex()]
        elif pandafileindex == PandaFileInfoIndex.MODIFYTIME:
            sepcifypddata = pandadata[fileInfo.getPandaFileModifyTimeIndex()]
        else:
            raise Exception("trainFileInfo : unkown panda data index")

    def getImgFileData(self, sortmode=SortMode.SORT_NONE):
        if sortmode == SortMode.SORT_CREATETIME:
            fileinfos = self.getAllSpecifyFileInfo(self.imgFilter, SortMode.SORT_CREATETIME)
        elif sortmode == SortMode.SORT_ACCESSTIME:
            fileinfos = self.getAllSpecifyFileInfo(self.imgFilter, SortMode.SORT_ACCESSTIME)
        else:
            fileinfos = self.getAllSpecifyFileInfo(self.imgFilter, SortMode.SORT_MODIFYTIME)

        if fileinfos:
            pandadata = self.getPandaData(fileinfos)
            #没什么用
            if sortmode == SortMode.SORT_CREATETIME:
                maxtime = pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.5) + (pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.25)) * 2.5
                mintime = pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.5) - (pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.25)) * 2.5
                timeinterval = fileinfos[len(fileinfos)-1].ctime - fileinfos[0].ctime
                for finfo in fileinfos:
                    if timeinterval < self.imgabnoralIntervalTime:
                        finfo.setFileNormal()
                    else:
                        if finfo.ctime > maxtime or finfo.ctime < mintime:
                            finfo.setFileAbnormal()
                        else:
                            finfo.setFileNormal()
            #没什么用
            elif sortmode == SortMode.SORT_ACCESSTIME:
                maxtime = pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.5) + (pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.25)) * 2.5
                mintime = pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.5) - (pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileAcessTimeIndex()].quantile(0.25)) * 2.5
                timeinterval = fileinfos[len(fileinfos)-1].atime - fileinfos[0].atime
                for finfo in fileinfos:
                    if timeinterval < self.imgabnoralIntervalTime:
                        finfo.setFileNormal()
                    else:
                        if finfo.atime > maxtime or finfo.atime < mintime:
                            finfo.setFileAbnormal()
                        else:
                            finfo.setFileNormal()
            else:
                maxtime = pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.5) + (pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.25)) * 2.5
                mintime = pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.5) - (pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.75) - pandadata[fileInfo.getPandaFileModifyTimeIndex()].quantile(0.25)) * 2.5
                timeinterval = fileinfos[len(fileinfos)-1].mtime - fileinfos[0].mtime
                starttime = fileinfos[0].mtime
                speed = 0
                for finfo in fileinfos:
                    if timeinterval < self.imgabnoralIntervalTime:
                        finfo.setFileNormal()
                    else:
                        timeint = finfo.mtime - starttime
                        starttime = finfo.mtime
                        if timeint != 0:
                            speed = finfo.filesize*1.0/(timeint * 1024 * 1024)
                        #print("timeint="+str(timeint)+",speed="+str(speed))
                        if maxtime > finfo.mtime > mintime:
                            finfo.setFileNormal()
                        else:
                            if timeint != 0 and speed > self.abbormalspeed:
                                finfo.setFileNormal()
                            else:
                                finfo.setFileAbnormal()

            return fileinfos
        else:
            return None

    def getZipFileData(self, otadirpath, sortmode=SortMode.SORT_ZIPTIME):
        if sortmode == SortMode.SORT_ZIPTIME:
            fileinfos = self.getAllSpecifyFileInfo(self.zipFilter, SortMode.SORT_ZIPTIME, otadirpath)
        elif sortmode == SortMode.SORT_CREATETIME:
            fileinfos = self.getAllSpecifyFileInfo(self.zipFilter, SortMode.SORT_CREATETIME, otadirpath)
        elif sortmode == SortMode.SORT_ACCESSTIME:
            fileinfos = self.getAllSpecifyFileInfo(self.zipFilter, SortMode.SORT_ACCESSTIME, otadirpath)
        else:
            fileinfos = self.getAllSpecifyFileInfo(self.zipFilter, SortMode.SORT_MODIFYTIME, otadirpath)

        if fileinfos and len(fileinfos) > 0:
            rightOtaZipnum = 0
            for finfo in fileinfos:
                if self.isOtaPackageNormal(finfo):
                    finfo.setFileNormal()
                    rightOtaZipnum += 1
                else:
                    finfo.setFileAbnormal()
            return fileinfos, rightOtaZipnum
        else:
            return None, 0

    def getVersionCircaTime(self):
        fileinfos = self.getAllSpecifyFileInfo(self.imgFilter, SortMode.SORT_MODIFYTIME)
        if fileinfos:
            pandadata = self.getPandaData(fileinfos)
            return pandadata[fileInfo.getPandaFileCratetimeIndex()].quantile(0.5)
        else:
            return None

    def isOtaPackageNormal(self, finfo: fileInfo, condition=OtaFileChangeCondition.ZIP_TIME):
        circatime = self.getVersionCircaTime()
        if condition == OtaFileChangeCondition.ZIP_TIME:
            if circatime and (abs(finfo.ziptime - circatime) < self.abnoralImgZipIntervalTime):
                return True
            else:
                return False
        elif condition == OtaFileChangeCondition.FILE_TIME:
            if circatime and (abs(finfo.mtime - circatime) < self.abnoralImgZipIntervalTime):
                return True
            else:
                return False
        else:
            return False

    def getPandaData(self, fileinfos):
        filenames = []
        filesizes = []
        filectimes = []
        fileatimes = []
        filemtimes = []
        for i in fileinfos:
            filenames.append(i.filename)
            filesizes.append(i.filesize)
            filectimes.append(i.ctime)
            filemtimes.append(i.mtime)
            fileatimes.append(i.atime)
        pandadata = {fileInfo.getPandaFileNameIndex(): filenames, fileInfo.getPandaFileSizeIndex(): filesizes,
                     fileInfo.getPandaFileAcessTimeIndex(): fileatimes,
                     fileInfo.getPandaFileCratetimeIndex(): filectimes,
                     fileInfo.getPandaFileModifyTimeIndex(): filemtimes}
        return pd.DataFrame(pandadata)
