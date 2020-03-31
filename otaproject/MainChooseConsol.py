from ConsolItemInfo import ConsolItemInfo
from ConsolParent import ConsolParent


class MainChooseConsol(ConsolParent):
    def __init__(self):
        self.consolItemList = [
            ConsolItemInfo("1)上一层目录", "P", "listPreviousDir", 0, True),
            ConsolItemInfo("O)OTA目录", "O", "listOtaDir", 0, True),
            ConsolItemInfo("R)根目录", "R", "listRootDir", 0, True),
            ConsolItemInfo("*)或直接输入目录", "*", "listRelativeDir", 1, True)
        ]