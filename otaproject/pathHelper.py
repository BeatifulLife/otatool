import os

import staticHelper
from filePolicy import filePolicy
from staticHelper import *
from autoOtainfo import *
import re


class pathHelper:

	project_map = {
		"a708": autoOtainfo.SprLocalPAth+"A708-L",
		"K102": autoOtainfo.MtkLocalPath+"K102-L",
		"K116": autoOtainfo.MtkLocalPath+"K116-L",
		"K707": autoOtainfo.MtkLocalPath+"K707-L",
		"K801": autoOtainfo.MtkLocalPath+"K707-L",
		"K805": autoOtainfo.MtkLocalPath+"K805-L",
		"K960": autoOtainfo.MtkLocalPath+"K960-L",
		"S960": autoOtainfo.MtkLocalPath+"S960-L",
		"ZH960": autoOtainfo.MtkLocalPath+"ZH960-K"}

	baselineName = 'baseline'
	customerName = 'customer'
	dailyName = 'daily_version'
	smtName = 'smt'
	SPR_PROJECT = ["A", "B", "C", "E", "P", "R"]

	def __init__(self):
		self.projectName = ''
		self.buildTypeName = ''
		self.buildType = BuildType.CUSTOMTYPE
		self.customName = ''
		self.versionName = ''
		self.isMtkProject = True

	def analyzePath(self, pathStr):
		assert(pathStr is not None)
		self.isMtkProject = True
		num, groups = pathHelper.isVersionPath(pathStr)
		if groups is None:
			print(""+pathStr+",Not Match")
			return False
		else:
			if num == staticHelper.VersionPathType.VERSION_CUSTOM_PATHNUM:
				##Customer
				##a708_sp7731c_32u_m/customer/AIMASEN-D3-A706/vCA350300
				self.customName = groups.group(3)
				self.versionName = groups.group(4)
			elif num == staticHelper.VersionPathType.VERSION_BASELINE_PATHNUM:
				##Maybe Baseline
				#c398_sp8830_32_kk/baseline/vVB00000B
				self.customName = "master"
				self.versionName = groups.group(3)
			else:
				raise Exception("patStr analyze Error ", pathStr)

			self.projectName = groups.group(1)
			self.buildTypeName = groups.group(2)

			if self.buildTypeName.upper() == pathHelper.customerName.upper():
				self.buildType = BuildType.CUSTOMTYPE
			elif self.buildTypeName.upper() == pathHelper.baselineName.upper():
				self.buildType = BuildType.BASELINETYPE
			elif self.buildTypeName.upper() == pathHelper.smtName.upper():
				self.buildType = BuildType.SMTTYPE
			elif self.buildTypeName.upper() == pathHelper.dailyName.upper():
				self.buildType = BuildType.DAILYTYPE
			for i in pathHelper.SPR_PROJECT:
				if self.projectName.upper().startswith(i):
					self.isMtkProject = False
					break
			return True

	##/mnt/Custom_MTK/W960-N/BEISHIDA-D1-W107/w960_mt6737m_35_n/vND200002
	def getLocalOtaVersionPtah(self):
		assert(self.projectName != '')
		assert(self.buildTypeName != '')
		assert(self.customName != '')
		assert(self.versionName != '')
		localotapath = autoOtainfo.MtkLocalPath
		if not self.isMtkProject:
			localotapath = autoOtainfo.SprLocalPAth
		localotabversionpath = localotapath+self.getLocalOtaProjectDirName()+"/" + self.customName + "/" + self.projectName + "/" + self.versionName
		#localotadeltapath = localotapath+self.getLocalOtaProjectDirName()+"/" + self.customName + "/" + self.projectName + "/delta"
		return localotabversionpath

	def getLocalServerOtaFilePath(self):
		assert(self.projectName != '')
		assert(self.buildTypeName != '')
		assert(self.customName != '')
		assert(self.versionName != '')
		temversionName = self.versionName
		if "-" in temversionName:
			temversionName = temversionName[0:temversionName.find("-")]
		if "_" in temversionName:
			temversionName = temversionName[0:temversionName.find("_")]
		localserverversionpath = autoOtainfo.LocalDir+"/JLink_OTA/"+self.projectName+"/"+temversionName+"/"
		return localserverversionpath

	def getLocalOtaProjectDirName(self):
		assert(self.projectName != '')
		groups = re.match(r'(.*)_(.*)_(.*)_(.*)', self.projectName)
		if groups:
			return groups.group(1).upper()+"-"+groups.group(4).upper()
		else:
			for project in pathHelper.project_map.keys():
				if self.projectName == project:
					return pathHelper.project_map[project]
		raise Exception("Illegal ProjectName ", self.projectName)

	@staticmethod
	def isVersionPath(pathStr):
		assert(pathStr is not None)
		if pathHelper.customerName in pathStr or pathHelper.dailyName in pathStr or pathHelper.smtName in pathStr or pathHelper.baselineName in pathStr:
			if autoOtainfo.LocalDir in pathStr:
				pathStr = pathStr[len(autoOtainfo.LocalDir)+1:]
			groups = re.match(r'(.*)/(.*)/(.*)/(v.*)', pathStr)
			if groups:
				return staticHelper.VersionPathType.VERSION_CUSTOM_PATHNUM, groups
			else:
				groups = re.match(r'(.*)/(.*)/(v.*)', pathStr)
				if groups:
					return staticHelper.VersionPathType.VERSION_BASELINE_PATHNUM, groups
				else:
					return staticHelper.VersionPathType.VERSION_NONE_PATHNUM, None
		else:
			return staticHelper.VersionPathType.VERSION_NONE_PATHNUM, None

	@staticmethod
	def isVersionOtaPath(pathStr):
		assert(pathStr is not None)
		#JLink_OTA/e706_7731e_32u_o/vGB110107
		if re.match(r'JLink_OTA/(.*)/(v.*)', pathStr) or re.compile(autoOtainfo.LocalDir+"/JLink_OTA/(.*)/(v.*)").match(pathStr):
			return True
		else:
			return False

	@staticmethod
	def isVersionOtaFilePath(pathStr):
		#JLink_OTA/e706_7731e_32u_o/vGB110107/e706_7731e_32u_o-ota-vGB110107_20190402.zip
		if re.match(r'JLink_OTA/(.*)/(v.*)/(.*).zip', pathStr) or re.compile(autoOtainfo.LocalDir+"/JLink_OTA/(.*)/(v.*)/(.*).zip").match(pathStr):
			return True
		else:
			return False




