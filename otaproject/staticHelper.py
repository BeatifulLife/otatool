from enum import Enum


class BuildType(Enum):
	CUSTOMTYPE = 0
	BASELINETYPE = 1
	SMTTYPE = 2
	DAILYTYPE = 3


class PandaFileInfoIndex(Enum):
	ACCESSTIM = 0
	CREATTIME = 1
	MODIFYTIME = 2


class SortMode(Enum):
	SORT_NONE = 0
	SORT_FILENAME = 1
	SORT_FILESIZE = 2
	SORT_CREATETIME = 3
	SORT_ACCESSTIME = 4
	SORT_MODIFYTIME = 5
	SORT_ZIPTIME = 6


class ChipPlatform(Enum):
	MTK_PROJECT = 0
	SPR_PROJECT = 1


class ConsolStatus(Enum):
	KEY_MATCH = 0
	KEY_NOTMATCH = 1
	KEY_EXIT = 2


class OtaFileChangeCondition(Enum):
	FILE_TIME = 0
	ZIP_TIME = 1


class VersionPathType(Enum):
	VERSION_NONE_PATHNUM = 0
	VERSION_BASELINE_PATHNUM = 3
	VERSION_CUSTOM_PATHNUM = 4


class ConsolReturnValue(Enum):
	CONSOL_NONE = 0
	CONSOL_NEWTITLE = 1
	CONSOL_MANUAL = 2


class SignatureType(Enum):
	SIGNATURE_ANDROID = 0
	SIGNATURE_JLINK = 1
	SIGNATURE_CUSTOM = 2


class AndroidVersion(Enum):
	ANDROID_NONE = -1
	ANDROID_K = 19
	ANDROID_L = 21
	ANDROID_M = 23
	ANDROID_N = 24
	ANDROID_O = 27
	ANDROID_P = 28

