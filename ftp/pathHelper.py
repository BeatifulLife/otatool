from staticHelper import *
from autoOtainfo import *

class pathHelper:

	def __init__(self,pathStr):
		self.pathStr=pathStr
		self.projectName=''
		self.buildTypeName=''
		self.buildType=BuildType.CUSTOMTYPE
		self.customName=''
		self.versionName=''
		self.isMtkProject=True
		self.SPR_PROJECT=["A","B","C","E","P","R"]
		self.project_map={"a708":spr_custom+"A708-L",
             "K102":mtk_custom+"K102-L",
             "K116":mtk_custom+"K116-L",
             "K707":mtk_custom+"K707-L",
             "K801":mtk_custom+"K707-L",
             "K805":mtk_custom+"K805-L",
             "K960":mtk_custom+"K960-L",
             "S960":mtk_custom+"S960-L",
             "ZH960":mtk_custom+"ZH960-K"}

	#a708_sp7731c_32u_m/customer/AIMASEN-D3-A706/vCA350300
	def analyzePath(self,pathStr):
		assert(pathStr is not None)
		self.isMtkProject=True
		groups=re.match(r'(.*)/(.*)/(.*)/(.*)',pathStr)
		if groups:
			self.projectName=groups.group(1)
			self.buildTypeName=roups.group(2)
			self.customName=groups.group(3)
			self.versionName=groups.group(4)
			if self.buildTypeName.upper() == "CUSTOMER":
				self.buildType=BuildType.CUSTOMTYPE
			elif self.buildTypeName.upper() == "BASELINE":
				self.buildType=BuildType.BASELINETYPE
			elif self.buildTypeName.upper() == "SMT":
				self.buildType=BuildType.SMTTYPE
			elif self.buildTypeName.upper() == "DAILY_VERSION":
				self.buildType=BuildType.DAILYTYPE
			for i in self.SPR_PROJECT:
				if self.projectName.upper().startswith(i):
					self.isMtkProject=False
					break
			return True
		else:
			print(""+pathStr+",Not Match")
			return False

	##/mnt/Custom_MTK/W960-N/BEISHIDA-D1-W107/w960_mt6737m_35_n/vND200002
	def getLocalOtaVersionPtah(self):
		assert(self.projectName!='')
		assert(self.buildTypeName!='')
		assert(self.customName!='')
		assert(self.versionName!='')
		localotapath=MtkLocalPath
		if not self.isMtkProject:
			localotapath=SprLocalPAth
		localotabversionpath = localotapath+getLocalOtaProjectDirName()+"/" + self.customName + "/" + self.projectName + "/" + self.versionName
		localotadeltapath    = localotapath+getLocalOtaProjectDirName()+"/" + self.customName + "/" + self.projectName + "/delta"
		return (localotabversionpath,localotadeltapath)

	def getLocalOtaProjectDirName(self):
		assert(self.projectName!='')
		groups=re.match(r'(.*)_(.*)_(.*)_(.*)',self.projectName)
		if groups:
			return groups.group(1).upper()+"-"+groups.group(4).upper()
		else:
			for project in self.project_map.keys():
				if self.projectName== project:
					return self.project_map[project]
		raise Exception("Illegal ProjectName ",self.projectName)