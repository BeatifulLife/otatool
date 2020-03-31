
class MethodHelper:
    def __init__(self, methodname, argc):
        self.methodname = methodname
        self.argc = argc

    def inVoke(self, consObject, argvs):
        fun = getattr(consObject, self.methodname)
        if fun is None:
            print("Cannot find this Methodname:" + self.methodname)
        try:
            if self.argc < 1:
                return fun()
            else:
                return fun(argvs)
        except Exception as e:
            print(e)
