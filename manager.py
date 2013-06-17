import guiManager as guiM
import threading
import time
import sys

ERROR_EXIT_MSG=\
"""
PluginManager exited has been interrupted,
triggered by user input or a run time error.
"""


class RunState:
	WARNING = "Warning"
	FAILED  = "Failed"
	SUCCESS = "Success"

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


class PluginManager(threading.Thread):
	def __init__(self, plugins, gui):
		threading.Thread.__init__(self)
		self.__plugins = plugins
		self.__gui = gui
		self.__info_map = {
		RunState.WARNING: guiM.InfoFormat.CONFIRMATION
		,RunState.FAILED: guiM.InfoFormat.ERROR
		,RunState.SUCCESS: guiM.InfoFormat.NONE
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
			time.sleep(5)
			self.__gui.stop()
			print "gui stopped, PluginManager_run says goodby"
			self.ret_code = 0
		print "run Done"

	def __run_plugin(self, pg):
		try:
			prefix = "Plugin-{id}: ".format(id=pg.id)
			self.__gui.updateUserInfo(prefix+"Starting...\n")
			
			state, pg_out = pg.run()	

			info = prefix + str(pg_out) + "\n"	
			self.__gui.updateUserInfo(info, self.__info_map[state])

			self.__gui.updateUserInfo(prefix+"Done.\n")

			result = (state == RunState.SUCCESS)

			if state == RunState.WARNING:
		 		result = self.__gui.waitUserConfirmation()
		except guiM.GUITerminating:
		 	msg = "# Gui terminating Exception caught, Terminate #"
		 	print len(msg)*"#"
		 	print msg
		 	print len(msg)*"#"
		 	result = False
		
		return result

def main():
	gui = guiM.GUIManager()

	conf_plugin = DebugPlugin("confirmation_plugin", RunState.WARNING,
		"""
		This should have different color
		please Cancel to stop or Confirm to continue
		"""
		)

	failed_plugin = DebugPlugin("Failure_plugin", RunState.FAILED,
		"""
		This should have different color
		plugin failed execution and user can only press cancel
		to abort execution
		No other plugin is executed after a failed plugin
		"""
		)

	plugins = [conf_plugin]
	for id in range(1,50):
		plugins.append(Plugin(id))

	plugins.append(conf_plugin)

	plugins.append(Plugin("Last_plugin"))

	plugins.append(failed_plugin)

	plugin_manager = PluginManager(plugins, gui)

	plugin_manager.start()

	gui.main_loop()

	plugin_manager.join()
	print "Done:"
	return plugin_manager.ret_code

if __name__ == '__main__':
    sys.exit(main())