
import os 
import subprocess

msg = \
"""
					this is something new :)
"""

cmd = "print msg\n"

#script that changes its own code and re-executes himself

my_name = os.path.basename(__file__)

print "file name:", os.path.basename(__file__), "full", __file__

print os.curdir

me = open(__file__, 'a+')

me.seek(0)
lines = me.readlines()
found = False
for l in lines:
	if cmd in l:
		found = True

if not found:
	me.write("\n" + cmd + "exit(3)")
	me.flush()
	print "cmd written :)"
	retcode = subprocess.call("python " + __file__, shell=True)
	print "2nd run return code:", retcode

me.close()

####END OF CODE
print msg
exit(3)