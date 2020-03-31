from methodHelper import MethodHelper


class ConsolItemInfo:
    def __init__(self, hint, key, methodname, argc, visible):
        self.hint = hint
        self.key = key
        assert (methodname is not None)
        self.methodname = methodname
        self.methodHelper = MethodHelper(methodname, argc)
        self.visible = visible

    def setItemVisible(self):
        self.visible = True

    def setItemInvisible(self):
        self.visible = False



