#coding=utf-8
import staticHelper
from ConsolItemInfo import ConsolItemInfo
from ConsolParent import ConsolParent
from methodHelper import MethodHelper


class ConsolSys:
    def __init__(self, consObject: ConsolParent, consolServer, matchMethod=None):
        """
        :param consObject:  ConsolParent子类并集成了doInit 和 doExit函数
        :param consolServer: 每个子项调用函数的实例
        :param matchMethod: 结果的匹配函数，默认None
        """
        self.title = "请选择:"
        if not isinstance(consObject, ConsolParent):
            raise Exception("Type must be ConsolParent")
        self.consObject = consObject
        self.consolServer = consolServer
        self.consolinfolist = []
        if matchMethod is not None:
            self.matchMethod = matchMethod
        else:
            self.matchMethod = self.isCommatch

    def insertConsolInfo(self, consolinfo):
        if not isinstance(consolinfo, ConsolItemInfo):
            print("Insert element not belong ConsolParent type")
        else:
            self.consolinfolist.append(consolinfo)

    def setConsolInfoList(self, consolinfolist):
        self.consolinfolist = consolinfolist

    def clearConsolInfoList(self):
        self.consolinfolist.clear()

    def makeTitle(self):
        if len(self.consolinfolist) < 1:
            return False
        self.title = "请选择:"
        for consolinfo in self.consolinfolist:
            if not isinstance(consolinfo, ConsolItemInfo):
                print("not ConsolParent type")
                return False
            if consolinfo.visible:
                self.title += "\n\t"+consolinfo.hint
        self.title += "\n\t"
        return True

    def startInit(self):
        self.consObject.doInit()
        self.makeTitle()

    def exitClear(self):
        self.consObject.doExit()

    def isCommatch(self, chooice, key):
        if chooice is None or key is None:
            return False
        else:
            if key.strip() == "*" and key.strip() != "":
                return True
            else:
                return chooice.strip() == key

    def isMatch(self, chooice, key):
        if self.matchMethod is None:
            return False
        else:
            return self.matchMethod(chooice, key)

    def isQuit(self, chooice):
        if chooice == "Q":
            return True
        else:
            return False

    def doRawInput(self):
        self.startInit()
        rawstatue = staticHelper.ConsolReturnValue.CONSOL_NONE
        while True:
            if rawstatue == staticHelper.ConsolReturnValue.CONSOL_NEWTITLE:
                self.makeTitle()
            chooice = input(self.title)
            if self.isQuit(chooice):
                self.exitClear()
                break
            for consolinfo in self.consolinfolist:
                if consolinfo.visible and self.isMatch(chooice, consolinfo.key):
                    self.doChoose(consolinfo.methodHelper, chooice)
                    break

    def doChoose(self, methodHelper, argvs):
        if methodHelper is None:
            print("Current option not implemented!")
        if not isinstance(methodHelper, MethodHelper):
            print("method is not MethodHelper type!")
        return methodHelper.inVoke(self.consolServer, argvs)

