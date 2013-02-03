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
import schnapphoto		


def main():
    Pyro.core.initServer()
    daemon=Pyro.core.Daemon()
    uri=daemon.connect(schnapphoto.CameraHost("false"),"schnapphoto")
      
    print "The daemon runs on port:",daemon.port
    print "The object's uri is:",uri

    daemon.requestLoop()
    
if __name__=="__main__":
    main()