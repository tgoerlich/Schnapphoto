#!/usr/bin/python
#
# schnapphoto_host.py
# Middleware and webapp to remotely control your digital camera with a mobile device
# Copyright (c) 2013 Thomas Goerlich
#
# https://github.com/tgoerlich/Schnapphoto
#
# about this file:
# runs camerahost object as pyro daemon

import Pyro.core
from daemon import runner
import schnapphoto		


#def main():
    
#if __name__=="__main__":
#    main()
    

class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/schnapphoto_host.pid'
        self.pidfile_timeout = 5
    
    def run(self):
	Pyro.core.initServer()
	daemon=Pyro.core.Daemon()
	uri=daemon.connect(schnapphoto.CameraHost("false"),"schnapphoto")
	  
	print "The daemon runs on port:",daemon.port
	print "The object's uri is:",uri

	daemon.requestLoop()

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action() 
