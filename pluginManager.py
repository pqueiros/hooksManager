import sys
import time
import threading
import guiManager
from pluginTraits import *

if __name__ == '__main__':
    import examplePlugins



ERROR_EXIT_MSG=\
"""
PluginManager exited, triggered by user input or a run time error.
"""



class PluginManager(threading.Thread):
    def __init__(self, plugins, gui):
        threading.Thread.__init__(self)
        self.__plugins = plugins
        self.__gui = gui
        self.__info_map = {
        RunState.WARNING: guiManager.InfoFormat.CONFIRMATION
        ,RunState.FAILED: guiManager.InfoFormat.ERROR
        ,RunState.SUCCESS: guiManager.InfoFormat.NONE
        }
        self.ret_code = ERROR_EXIT_MSG

    def run(self):
        interrupted = False
        for pg in self.__plugins:
            if not self.__run_plugin(pg):
                interrupted = True
                break

        if not interrupted:
            print "Everything done, sleep a bit & stop Gui"
            time.sleep(1)
            self.__gui.stop()
            print "gui stopped, PluginManager_run says goodby"
            self.ret_code = 0
        print "run Done"

    def __run_plugin(self, pg):
        try:
            prefix = "Plugin-{id}: ".format(id=pg.id)
            self.__gui.updateUserInfo(prefix+"Starting...\n")
            
            state, pg_out = pg.run()

            print 5*"*", prefix, "BEGIN", 5*"*"
            print prefix
            print "Reported:", state
            print "Output:", pg_out
            print 5*"*", prefix, "END", 5*"*"

            info = prefix + str(pg_out) + "\n"  
            self.__gui.updateUserInfo(info, self.__info_map[state])

            self.__gui.updateUserInfo(prefix+"Done.\n")

            result = (state == RunState.SUCCESS)

            if state == RunState.WARNING:
                result = self.__gui.waitUserConfirmation()
        except guiManager.GUITerminating:
            msg = "# Gui terminating Exception caught, Terminate #"
            print len(msg)*"#"
            print msg
            print len(msg)*"#"
            result = False
        
        return result


################### TEST CODE ####





def __test_main(use_fail_plugin = False):
    __conf_plugin = examplePlugins.DebugPlugin("confirmation_plugin", RunState.WARNING, \
"""
This should have different color
please Cancel to stop or Confirm to continue
"""
)

    __failed_plugin = examplePlugins.DebugPlugin("Failure_plugin", RunState.FAILED, \
"""
This should have different color
plugin failed execution and user can only press cancel
to abort execution
No other plugin is executed after a failed plugin
"""
)

    #test setup
    plugins = []
    for id in range(1,20):
        plugins.append(examplePlugins.Plugin(id))

    plugins.append(__conf_plugin)

    plugins.append(examplePlugins.Plugin("Last_plugin"))

    if use_fail_plugin:
        plugins.append(__failed_plugin)

    #execution
    gui_manager = guiManager.GuiManager()

    plugin_manager = PluginManager(plugins, gui_manager)

    plugin_manager.start()

    gui_manager.main_loop()

    plugin_manager.join()
    print "Done:"
    return plugin_manager.ret_code

if __name__ == '__main__':
    __test_main()
    sys.exit(__test_main(use_fail_plugin = True))
