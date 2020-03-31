#!/usr/bin/env python
from MountServer import MountServer
from VersionChooseConsol import VersionChooseConsol
from VersionChooseServer import VersionChooseServer
from localpullFile import *
from filePolicy import *
from pathHelper import pathHelper
from staticHelper import *

'''
localpullFile=localPullFile()
has_mount=localpullFile.doMount()
if has_mount:
	print("mount")
else:
	print("mount error")
'''


'''
filepolicy=filePolicy("/mnt/server")
allfile=filepolicy.getAllFileInfo()
print(fileInfo.getTitle())
for i in allfile:
	print(i.toString())
'''

'''
fPolicy = filePolicy("/mnt/server/a708_sp7731c_32u_m/customer/JIAFENGTAI-D1-A706/vCA570002")
optiondata = fPolicy.getPendingFileData()
for i in optiondata:
	print(i.toString())
'''

'''
print(pathHelper.isVersionOtaFilePath("/mnt/server/JLink_OTA/k960n_mt6580_32_n/vXA380006/k960n_mt6580_32_n-ota-vXA380006_20190416.zip"))
path = "/mnt/server/a708_sp7731c_32u_m/customer/JIAFENGTAI-D1-A706/vCA570002"
if pathHelper.isVersionPath(path):
	phelper = pathHelper()
	phelper.analyzePath(path)
	print(phelper.getLocalOtaProjectDirName())
	print(phelper.getLocalOtaVersionPtah())
	print(phelper.getLocalServerOtaFilePath())
'''

'''
versionCosol = VersionChooseServer()
#versionCosol.listRootDir()
print(versionCosol.getRelativeDir("/mnt/server/.."))
'''


versionconsol = VersionChooseConsol()
versionconsol.doRun()

'''
otazipfile = zipfile.ZipFile("/mnt/server/JLink_OTA/a706_sp7731c_32g_m/vCB290301/a706_sp7731c_32g_m-ota-vCB290301_20190515.zip")
otazipinfo = otazipfile.getinfo("ota.zip")
print("%d-%d-%d %d:%d:%d" % (otazipinfo.date_time[0], otazipinfo.date_time[1], otazipinfo.date_time[2], otazipinfo.date_time[3], otazipinfo.date_time[4], otazipinfo.date_time[5]))
'''


