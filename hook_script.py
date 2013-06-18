
import sys
import vMonitor
import guiManager
import pluginManager
import examplePlugins #TODO remove example


#TODO build module for svn
class HookScriptModule(vMonitor.vModuleGit):
    def __init__(self):
        self.files2monitor = ["."]
        vMonitor.vModuleGit.__init__(self, self.files2monitor)
        
    def main_code(self):
        #TODO integrate svn plugins
        plugins = []
        for id in range(1,20):
            plugins.append(examplePlugins.Plugin(id))

        #execution
        gui_manager = guiManager.GuiManager()
        plugin_manager = pluginManager.PluginManager(plugins, gui_manager)

        plugin_manager.start()
        gui_manager.main_loop()
        plugin_manager.join()

        return plugin_manager.ret_code
        


if __name__ == '__main__':
    sys.exit(HookScriptModule().run())