from pluginTraits import *

class Plugin():
    
    def __init__(self, id):
        self.id = id

    def run(self):
        msg = "Default plugin id:" + str(self.id) + " run call executed -- Does nothing"
        return RunState.SUCCESS, msg

class DebugPlugin(Plugin):
    def __init__(self, id, returnCode, message):
        Plugin.__init__(self,id)
        self.__retCode = returnCode
        self.__msg = message

    def run(self):
        msg = "DebugPlugin:\n" + self.__msg 
        return self.__retCode,  msg

