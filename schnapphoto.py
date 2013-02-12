#!/usr/bin/python
#
# SCHNAPPHOTO
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
import sys
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
		
	def set_widget_value(self,widgetname,value):
		print "set_widget_value (",widgetname,",",value,")"
		self.lock()
		widget=self.cam.config.get_child_by_name(widgetname)
		try:
		  widget.value=value
		  rootwidget=widget.root
		  self.cam.set_config(rootwidget)
		  result="success"
		except:
		   result="failed"
		print result
		return result	  
		
	def get_widget_value(self,widgetname):
		widget=self.cam.config.get_child_by_name(widgetname)
		self.lock()
		try:
		  result=widget.value
		except:
		   result=""
		self.unlock()
		print "get_widget_value (",widgetname,") - ",result
		#return result
	
	def get_widget_options(self,widgetname):
		self.lock()
		widget=self.cam.config.get_child_by_name(widgetname)
		choicecount=widget.count_choices()
		result=""
		for i in range(0,choicecount):
		  result+=widget.get_choice(i)
		  if (i<choicecount-1):
		    result+=","
		self.unlock()
		print "get_widget_options (",widgetname,") - ",result		
		return result  
	
	def get_widget_readonly(self,widgetname):
		self.lock()
		widget=self.cam.config.get_child_by_name(widgetname)
		result=widget.readonly
		self.unlock()
		print "get_widget_readonly (",widgetname,") - ",result
		return result  
		
	def get_widget_label(self,widgetname):
		self.lock()
		widget=self.cam.config.get_child_by_name(widgetname)
		result=widget.label
		self.unlock()
		print "get_widget_label (",widgetname,") - ",result
		return result
		
	
	#def get_capturesetting(self,attribute):
		#print "get_capturesetting (",attribute,")"
		#self.wait_until_unlocked()
		#self.lock()
		#try:
		  #retval=self.cam.config.main.capturesettings.__getattribute__(attribute).value
		#except:
		  #print "get_capturesetting (",attribute,") failed"
		  #retval="unknown"
		#self.unlock()
		#return retval
		
	#def __set_capset(self,config,attribute,value):
		#try:
		    #config.main.capturesettings.__getattribute__(attribute).value=value
		    #self.cam.set_config(config)
		    #retval=0
		    ##retval=sys.exc_info()[1].result
		    #print "success:",sys.exc_info()[1].__str__()
		#except:
		    #print "failed"
		    #retval=sys.exc_info()[1].result
		    #print sys.exc_info()[1].__str__()
		#print retval
		#return retval
		
	
	#def set_capturesetting(self,attribute,value):
		#self.wait_until_unlocked()
		#self.lock()	
		#config=self.cam.config
		#retval=-101
		#i=-1
		#while (retval==-101):
		    #i+=1
		    #print "try %d:" % (i)
		    #retval=self.__set_capset(self.cam.config,attribute,value)
		#self.unlock()
		#print "set_capturesetting (",attribute,",",value,") ", retval
		#return retval
	
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
		
	#def count_capturesetting_options(self,attribute):
		#print "count_capturesetting_options (",attribute,")"
		#self.wait_until_unlocked()
		#self.lock()
		#try:
		  #widget=self.cam.config.main.capturesettings.__getattribute__(attribute)
		  #retval=pp.gp.gp_widget_count_choices(widget._w)
		#except:
		  #retval="failure"
		#self.unlock()
		#print "count_capturesetting_options (",attribute,") ",retval
		#return retval

	#def get_capturesetting_option(self,attribute,index):
		#self.wait_until_unlocked()
		#self.lock()
		#try:
		  #widget=self.cam.config.main.capturesettings.__getattribute__(attribute)
		  #retval=widget.get_choice(index)
		#except:
		  #retval="failure"
		#self.unlock()
		##print "get_capturesetting_option ( attribute=",attribute,",index=",index,") ",retval
		#return retval
	
	#def read_capturesetting_options_from_cam(self,attribute):
		#options={}
		#c = self.count_capturesetting_options(attribute)
		#retval=""
		#for i in range(c):
		  #opt=self.get_capturesetting_option(attribute,i)
		  #options[i]=opt
		  #retval += opt
		  #if i<(c-1):
		    #retval+=","
		#self.capturesettings[attribute]=options
		#return retval
	
	#def read_capturesetting_options_from_cache(self,attribute):
		#options=self.capturesettings[attribute]
		#c=len(options)
		#retval=""
		#for i in range(c):
		  #retval += options[i]
		  #if i<(c-1):
		    #retval+=","
		#return retval	
	
	#def get_capturesetting_all_options(self, attribute):
		#retval=""
		#if attribute in self.capturesettings:
		  #retval=self.read_capturesetting_options_from_cache(attribute)
		#else:
		  #retval=self.read_capturesetting_options_from_cam(attribute)
		#print "get_all_options (",attribute,") ", retval
		#return retval
	
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
		if not hasattr (self,'self.file_index'):
		   self.create_file_index()
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
		      print("trigger_picture() result %d - retry #%d..." % (result,i))
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
		
	def pictureloop(self,loops=1,layers=1,stops=0,bracketingtype="exposurecompensation",delay=0):
		print "pictureloop(loops:",loops," layers:",layers," stops:",stops, " bracketingtype:",bracketingtype," delay",delay,")"
		p=0
		i=0
		if not bracketingtype in self.capturesettings:
		  self.get_capturesetting_all_options(bracketingtype)
		current_setting=self.get_capturesetting(bracketingtype)
		print "current_setting:",current_setting
		ec_current_key=self.get_key_for_value(self.capturesettings[bracketingtype],current_setting)
		print "ec_current_key",ec_current_key
		print "loops=",loops
		print range(0,loops)
		for i in range(0,loops):
		  print "chk"
		  print "loop ",i
		  if (delay>0):
		    time.sleep(delay)
		  ec_step_key=ec_current_key-(((layers-1)/2)*stops)
		  print "ec_step_key=",ec_step_key
		  k=0
		  print "layers=",layers
		  for k in range(0,layers):
		    print "stop ",k		      
		    if (ec_step_key<0):
			ec_step_key=0
		    print len(self.capturesettings[bracketingtype])
		    if (ec_step_key>len(self.capturesettings[bracketingtype])-1):
			ec_step_key=len(self.capturesettings[bracketingtype])-1
		    print "ec_step_key=",ec_step_key
		    self.set_capturesetting(bracketingtype,self.capturesettings[bracketingtype][ec_step_key])
		    ec_step_key+=stops
		    p+=1
		    print self.trigger_picture()
		self.set_capturesetting(bracketingtype,current_setting)
		return p
		
	def get_abilities(self, abilities):
		ablist = {
		    "operations"	: self.cam.abilities.operations,
		    "file_operations"	: self.cam.abilities.file_operations
		  }
		return ablist[abilities]
		
	def get_camerainfo(self):
		return self.cam.summary
	
		
	def get_widget_xml(self,widget):
		print "get_widget_xml"
		xmlTemplate="""  <widget>
		    <name>%(name)s</name>
		    <label>%(label)s</label>
		    <value>%(value)s</value>
		    <readonly>%(readonly)s</readonly>
		    <optioncount>%(optioncount)s</optioncount>
		    <options>
		    """
		try:
		  value=widget.value
		except:
		  value=""		  
		c=widget.count_choices()
		data={'name':widget.name,'label':widget.label,'value':value,'readonly':widget.readonly,'optioncount':c}
		for k in range(0,c):
		  xmls="""      <option number=%(number)s>%(value)s</option>
		    """
		  data2={'number':k+1,'value':widget.get_choice(k)}
		  xmlTemplate+=xmls%data2
		xmlTemplate+="""</options>
		  </widget>
		"""
		self.widgets_xml+=xmlTemplate%data
		n=widget.count_children()
		for i in range(0,n):
		  child=widget.get_child(i)
		  print "child ",i
		  self.get_widget_xml(child)
	
	def display_widgets(self,widget,prefix):
		print "display_widgets"
		label=widget.label
		name=prefix+widget.name
		print "label:    ",label
		print "name:     ",name
		if (widget.info):
		  print "info:     ",widget.info
		try:
		  print "value:    ",widget.value
		except:
		  print "value:     none"
		print "choices:  ",widget.choices
		print "readonly: ",widget.readonly
		n=widget.count_children()
		for i in range(0,n):
		  child=widget.get_child(i)
		  self.display_widgets(child,name+":")
		  
	def list_all_config(self):
		print "list_all_config"
		self.display_widgets(self.cam.config,"")
		
	def get_all_widgets_xml(self):
		self.widgets_xml=""
		self.get_widget_xml(self.cam.config)
		return """<?xml version=\"1.0\" encoding=\"utf-8\"?>
		<widgets>
		"""+self.widgets_xml+"""
		</widgets>
		"""