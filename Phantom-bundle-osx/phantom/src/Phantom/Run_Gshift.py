from os import devnull
from os.path import abspath
from subprocess import Popen
from subprocess import check_output
from sys import platform
from Debug import Debug
import logging
import atexit

class Run_Gshift:

    def __init__(self):
        self.log = logging.getLogger("gshift")
        self.process = None
        self.fnull = open(devnull, 'wb')

    def start(self):
        self.log.info("Starting gshift...")
        try:
            if platform == 'win':
                command = [abspath('gshift.exe'), '--shh']
                self.process = Popen(command, stdout=self.fnull, stderr=self.fnull, shell=False)
            else:
                command = [abspath('gshift'), '--shh']
                self.process = Popen(command, stdout=self.fnull, stderr=self.fnull, shell=True)

            atexit.register(self.stop)
            return self.process

        except Exception, err:
            print "Error starting gshift: %s" % Debug.formatException(err)
            self.log.error("Error starting gshift: %s" % Debug.formatException(err))
            return False


    def check_running_proc(self,name):

        for i in range(1,10):
            try:
                pidlist = map(int, check_output(["pidof", name]).split())
            except Exception as e:
                return False

            if len(pidlist) > 0:
                return pidlist
            if i == 10:
                break

        return False


    def stop(self):
        self.log.info("Stopping gshift...")
        try:
            self.process.terminate()
        except Exception, err:
            self.log.error("Error stopping gshift: %s" % err)
