
import sys
import subprocess


class VersionControlExeption(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class vModule():
    def __init__(self, files2monitor):
        self.f2m = files2monitor

    def main_code(self):
        raise Exception("vModule:main_code to be implemented by client class")

    def get_version(self, files):
        raise Exception("vModule:get_version version control tool dependent, to be implemented")

    def update_version(self, files):
        raise Exception("vModule:update_version version control tool dependent, to be implemented")

    def __monitor(self, files):
        c_version = self.get_version(files)
        self.update_version(files)
        n_version = self.get_version(files)
        print "moniroted files:", files
        print "current version:", c_version
        print "new version:    ", n_version

        return c_version != n_version

    def run(self):
        try:
            if self.__monitor(self.f2m):
                print "Source code changed, re-launching..."
                ret = subprocess.call([sys.executable] + sys.argv)
            else:
                print "Running main code..."
                ret = self.main_code()
        except VersionControlExeption as es:
            ret = "MONITOR Failed:\n" + es.value
        return ret

class vModuleGit(vModule):
    def __init__(self, files2monitor):
        vModule.__init__(self, files2monitor)

    def __raise_exception(self, cmd, out, err):
        msg ="*** GIT ERROR detected ***\ncmd:{cmd}\ncmd_stdout:{stdout}\ncmd_stderr:{stderr}\n"\
        .format(stdout=str(out),stderr=str(err), cmd=cmd)
        raise VersionControlExeption(msg)

    def __get_file_version(self, file):
        cmd = "git log --pretty=format:'%H' -n 1 " + file
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        if err != "":
            self.__raise_exception(cmd, out, err)
        return out

    def get_version(self, files):
        return [self.__get_file_version(f) for f in files]

    def update_version(self, files):
        cmd = "git pull"
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        #TODO how to detect erros here???
        

class TestModule(vModuleGit):
    def __init__(self):
        self.files2monitor = ["vModule_test"
                              #,"vModule_test/testFile2.txt"
                              #,"vModule_test/testFile2.txt"
                              #,"vModule_test/testFile3.txt"
                              #,"vModule_test/testFile4.txt"
                              ,__file__
                              ]
        vModuleGit.__init__(self, self.files2monitor)
        
    def main_code(self):
        print "My main code executed!!! :)"
        print "and new code added too :)"
        print "and yet another code of line added :)"
        return 3

def _test():
    ret = TestModule().run()
    return ret



if __name__ == '__main__':
    sys.exit(_test())
