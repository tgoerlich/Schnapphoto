#!/usr/bin/python
#
# schnapphoto.py
# Middleware and webapp to remotely control your digital camera with a mobile device
# Copyright (c) 2013 Thomas Goerlich
#
# https://github.com/tgoerlich/Schnapphoto
#
# about this file:
# the class CameraHost implements libgphoto functionality in python
# heavily relies on piggyphoto python bindings for libgphoto


import piggyphoto as pp
import Pyro.core
import os
import time
from array import array
from ctypes import byref

class CameraHost(Pyro.core.ObjBase):
        
        def __init__(self,standalone):
                if (standalone=="false"): Pyro.core.ObjBase.__init__(self)
                print "init"
                try:
		  self.cam = pp.Camera()
		  self.cfile = pp.CameraFile()
		except:
		  print "camera init failed"
		self.locked=0
		print "init done"
		self.capturesettings = {}
	
	def lock(self):
	  self.locked=1
	  
	def unlock(self):
	  self.locked=0
	  
	def is_locked(self):
	    return self.locked
	  
	def wait_until_unlocked(self):
	    if (self.is_locked()==1): print "locked. wait..."
	    while (self.is_locked()==1):
	      time.sleep(0.3)
	    
	  
	def close(self):
	  result = "close camera"
	  self.cam.close()
	  print result
	  return result
                
        def reinit(self):
	    print "reinit"
	    retval=0
	    try:
	      self.cam = piggyphoto.Camera()
            except:
	      print "reinit failed"
	      retval=1
	    return retval
            
        def get_model(self):
		print "get_model"
		self.wait_until_unlocked()
		self.lock()
		try:
		  retval=self.cam.abilities.model
		except:
		  print "failed, trying reinit..."
		  self.reinit()
		try:
		  retval=self.cam.abilities.model
		except:
		  print "get_model failed"
		  retval="no camera"
		print retval
		self.unlock()
		return retval
		  
	def get_capturesetting(self,attribute):
		print "get_capturesetting (",attribute,")"
		self.wait_until_unlocked()
		self.lock()
		try:
		  retval=self.cam.config.main.capturesettings.__getattribute__(attribute).value
		except:
		  print "get_capturesetting (",attribute,") failed"
		  retval="unknown"
		self.unlock()
		return retval
	
	def set_capturesetting(self,attribute,value):
		#print "set_capturesetting (",attribute,",",value,")"
		self.wait_until_unlocked()
		self.lock()
		retval="unknown"
		config=self.cam.config
		#widget=self.cam.config.main.capturesettings.__getattribute__(attribute)
		#print widget._get_name()," - ",widget._get_value()
		retries=9
		delay=0.5
		result = 0
		#TODO: wait until camera not busy
		#for i in range(1 + retries):
		try:
		  config.main.capturesettings.__getattribute__(attribute).value=value
		  #widget.value=value  
		  #self.cam.config.main.capturesettings.__getattribute__(attribute)._set_value(value)
		  self.cam.set_config(config)
		  retval="ok"
		except:
		  retval="failed"
		  
		 #   if retval == 0: break
		  #  else:
		   #   time.sleep(delay)
		    #  print("set_capturesetting (",attribute,",",value,") : retval=%s, retry #%d..." % (retval,i))
		self.unlock()
		print "set_capturesetting (",attribute,",",value,") ", retval
		return retval
	
	def get_status(self,attribute):
		print "get_status (",attribute,")"
		self.wait_until_unlocked()
		self.lock()
		try:
		  retval=self.cam.config.main.status.__getattribute__(attribute).value
		  retval="successful"
		except:
		  retval="failure"
		self.unlock()
		print "get_status (",attribute,") ", retval
		return retval
		
	def count_capturesetting_options(self,attribute):
		print "count_capturesetting_options (",attribute,")"
		self.wait_until_unlocked()
		self.lock()
		try:
		  widget=self.cam.config.main.capturesettings.__getattribute__(attribute)
		  retval=pp.gp.gp_widget_count_choices(widget._w)
		except:
		  retval="failure"
		self.unlock()
		print "count_capturesetting_options (",attribute,") ",retval
		return retval

	def get_capturesetting_option(self,attribute,index):
		self.wait_until_unlocked()
		self.lock()
		try:
		  widget=self.cam.config.main.capturesettings.__getattribute__(attribute)
		  retval=widget.get_choice(index)
		except:
		  retval="failure"
		self.unlock()
		#print "get_capturesetting_option ( attribute=",attribute,",index=",index,") ",retval
		return retval
	
	def read_capturesetting_options_from_cam(self,attribute):
		options={}
		c = self.count_capturesetting_options(attribute)
		retval=""
		for i in range(c):
		  opt=self.get_capturesetting_option(attribute,i)
		  options[i]=opt
		  retval += opt
		  if i<(c-1):
		    retval+=","
		self.capturesettings[attribute]=options
		return retval
	
	def read_capturesetting_options_from_cache(self,attribute):
		options=self.capturesettings[attribute]
		c=len(options)
		retval=""
		for i in range(c):
		  retval += options[i]
		  if i<(c-1):
		    retval+=","
		return retval	
	
	def get_capturesetting_all_options(self, attribute):
		retval=""
		if attribute in self.capturesettings:
		  retval=self.read_capturesetting_options_from_cache(attribute)
		else:
		  retval=self.read_capturesetting_options_from_cam(attribute)
		print "get_all_options (",attribute,") ", retval
		return retval
	
	def get_picture(self):
		print "get_picture"
		retval=""
		return retval
	
	def _list_files(self,path):
		print "_list_files ("+path+")"
		try:
		    l  = pp.CameraList()
		except:
		    print "failed"
		pp.gp.gp_camera_folder_list_files(self.cam._cam, str(path), l._l, pp.context)
		for i in range(pp.gp.gp_list_count(l._l)):
			#print "   ",i,": ",l.get_name(i)
			fname=l.get_name(i)
			fileName, fileExtension = os.path.splitext(fname)
			if (fileExtension == ".JPG"):
			  self.file_index.append(path+"/"+l.get_name(i))
			#get_file_info(path,l.get_name(i))	
		print "end loop"
	
	def _list_folders(self,p):
		print "_list_folders ("+p+")"
		path=p+"/"
		self._list_files(path)
		l  = pp.CameraList()
		l2 = pp.CameraList()
		try:
		    pp.gp.gp_camera_folder_list_folders(self.cam._cam, str(path), l._l, pp.context)
		except:
		    print "error at pp.gp.gp_camera_folder_list_folders(self.cam._cam, str(path), l._l, pp.context)"
		count=pp.gp.gp_list_count(l._l)
		for i in range(count):
			print i,": ",path,l.get_name(i)
			pp.gp.gp_camera_folder_list_folders(self.cam._cam, str(path+l.get_name(i)), l2._l, pp.context)	
			if pp.gp.gp_list_count(l2._l) > 0: 
				self._list_folders(path + l.get_name(i))
			else:
				#print path + l.get_name(i) + "/"
				self._list_files(path + l.get_name(i))
		
	def create_file_index(self):
		print "create_file_index"
		self.file_index = []
		self._list_folders("")
		#print self.file_index
		return "file index created"
		
	def get_latest_image(self):
		print "get_latest_image"
		#print self.file_index[-1]
		destination = "/var/www/cameraroll/"+os.path.basename(self.file_index[-1])
		print "destination=",destination
		srcfolder=os.path.dirname(self.file_index[-1])+"/"
		print "srcfolder=",srcfolder
		srcfilename=os.path.basename(self.file_index[-1])
		print "srcfilename=",srcfilename
		#cfile = pp.CameraFile(self.cam._cam, srcfolder, srcfilename)
		self.cfile.__init__(self.cam._cam, srcfolder, srcfilename)
		print "save"
		self.cfile.save(destination)
		print "unref"
		pp.gp.gp_file_unref(self.cfile._cf)
		#print "self.cam.download_file(",os.path.dirname(self.file_index[-1]),",",os.path.basename(self.file_index[-1]),",",destination,")"
		#self.cam.download_file(os.path.dirname(self.file_index[-1])+"/",os.path.basename(self.file_index[-1]),destination)
		#print "pp.CameraFile(self.cam,",os.path.dirname(self.file_index[-1]),",",os.path.basename(self.file_index[-1]),")"
		#cfile=pp.CameraFile(self.cam,os.path.dirname(self.file_index[-1]),os.path.basename(self.file_index[-1]))
		#print cfile.name
		#return cfile.to_pixbuf()
		return destination
		
	def get_file_index(self):
		return self.file_index
		
	def get_file(self,i):
		return self.file_index[i]
		
	def trigger_picture(self):
		self.wait_until_unlocked()
		self.lock()
		retries=9
		delay=0.5
		result = 0
		returntype=0
		data=""
		for i in range(1 + retries):
		    # triggers shutter, image is stored in camera roll (no path returned)
		    result=pp.gp.gp_camera_trigger_capture(self.cam._cam)
		    if result == 0: break
		    else:
		      time.sleep(delay)
		      print("trigger_picture() retry #%d..." % (i))
		    for m in range(20):  
		      retval = pp.gp.gp_camera_wait_for_event(self.cam._cam, 1, byref(returntype), byref(data), pp.context);
		      print m,": ",retval
		self.unlock()
		return result
		
	def take_picture(self):
		self.wait_until_unlocked()
		self.lock()
		result=self.cam.capture_image()
		self.unlock()
		return result
		
	def get_key_for_value(self,list,searchvalue):
		result = [key for key,value in list.iteritems() if value == searchvalue]
		return int(result[0])
		
	def pictureloop(self,count=1,layers=1,evsteps=0,delay=0):
		print "pictureloop(count:",count,"layers:",layers,"ev:",evsteps,"delay",delay,")"
		p=0
		i=0
		if not "exposurecompensation" in self.capturesettings:
		  self.get_capturesetting_all_options("exposurecompensation")
		ec_current=self.get_capturesetting("exposurecompensation")
		print "ec_current:",ec_current
		ec_current_key=self.get_key_for_value(self.capturesettings["exposurecompensation"],ec_current)
		print "ec_current_key",ec_current_key
		print "count=",count
		print range(0,count)
		for i in range(0,count):
		  print "chk"
		  print "loop ",i
		  if (delay>0):
		    time.sleep(delay)
		  ec_step_key=ec_current_key-(((layers-1)/2)*evsteps)
		  print "ec_step_key=",ec_step_key
		  k=0
		  print "layers=",layers
		  for k in range(0,layers):
		    print "stop ",k		      
		    if (ec_step_key<0):
			ec_step_key=0
		    if (ec_step_key>count(self.capturesettings['exposurecompensation'])-1):
			ec_step_key=count(self.capturesettings['exposurecompensation'])-1
		    print "ec_step_key=",ec_step_key
		    self.set_capturesetting("exposurecompensation",self.capturesettings['exposurecompensation'][ec_step_key])
		    ec_step_key+=evsteps
		    p+=1
		    print self.trigger_picture()
		self.set_capturesetting("exposurecompensation",ec_current)
		return p
 
