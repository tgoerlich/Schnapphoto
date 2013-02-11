#!/usr/bin/python
#
# SCHNAPPHOTO
# Middleware and webapp to remotely control your digital camera with a mobile device
# Copyright (c) 2013 Thomas Goerlich
#
# https://github.com/tgoerlich/Schnapphoto
#
# about this file:
# cgi command interface
# connects to camerahost object with pyro
# translates cgi requests into python calls to camerahost

import Pyro.core
import cgi
import cgitb
cgitb.enable()

content_txt="Content-Type: text/plain\n\n"
content_jpg="Content-Type: img/jpeg\n\n"


def get_model(data):
    global content_txt
    global cam
    return content_txt+cam.get_model()
   
#def get_capturesetting(data):
    #global content_txt
    #global cam
    #if data.has_key( 'attribute' ):
	#result=content_txt+cam.get_capturesetting(data['attribute'].value)
    #else:
	#result="no attribute given"
    #return result

def get_widget_value(data):    
    global content_txt
    global cam
    if data.has_key( 'attribute' ):
	result=content_txt+cam.get_widget_value(data['attribute'].value)
    else:
	result="no attribute given"
    return result    
    
def get_widget_label(data):
    global content_txt
    global cam
    if data.has_key( 'attribute' ):
	result=content_txt+cam.get_widget_label(data['attribute'].value)
    else:
	result="no attribute given"
    return result 

def set_widget_value(data):
    global content_txt
    global cam
    if data.has_key( 'attribute' ):
	if data.has_key( 'value' ):
	    result=content_txt+cam.set_widget_value(data['attribute'].value,data['value'].value)
	else:
	    result="no value given"
    else:
	result="no attribute given"
    return result    
    
#def set_capturesetting(data):
    #global content_txt
    #global cam
    #if data.has_key( 'attribute' ):
	#if data.has_key( 'value' ):
	    #result=content_txt+cam.set_capturesetting(data['attribute'].value,data['value'].value)
	#else:
	    #result="no value given"
    #else:
	#result="no attribute given"
    #return result
  
def get_widget_options(data):
    global content_txt
    global cam
    if data.has_key( 'attribute' ):
	result=content_txt+cam.get_widget_options(data['attribute'].value)
    else:
	result="no attribute given"
    return result
        
#def get_capturesetting_all_options(data):
    #global content_txt
    #global cam
    #if data.has_key( 'attribute' ):
	#result=content_txt+cam.get_capturesetting_all_options(data['attribute'].value)
    #else:
	#result="no attribute given"
    #return result
   
   
#def get_choice(data):
    #global content_txt
    #global cam
    #return result
  
  
def get_file_index(data):
    global content_txt
    global cam
    result=content_txt+cam.create_file_index()
    return result
  
  
def get_latest_image(data):
    global content_txt
    global cam
    result=content_jpg+cam.get_latest_image()
    return result
  
  
#def get_status(data):
    #global content_txt
    #global cam
    #if data.has_key( 'attribute' ):
      #result=content_txt+cam.get_status(data['attribute'].value)
    #else:
      #result=content_txt+"no attribute given"
    #return result
  
  
#def get_cameratime(data):
    #global content_txt
    #global cam
    #result="cameratime"
    #return result

def getparam(data,key,defaultvalue):
    if data.has_key( key ):
      result=data[key].value
    else:
      result=defaultvalue
    return result

    
def take_picture(data):
    global content_txt
    global cam
    result=cam.pictureloop(
      loops=int(getparam(data,'picturecount',1)),
      layers=int(getparam(data,'bracketinglayers',1)),
      bracketingtype=getparam(data,'bracketingtype','shutterspeed2'),
      stops=int(getparam(data,'stops',0)),
      delay=int(getparam(data,'delay',0))
      )
    return content_txt+result
    
def get_abilities(data):
    global content_txt
    global cam
    result=cam.get_abilities(getparam(data,'abilities'))
    return content_txt+result
      
def get_systemtime(data):
    global content_txt
    global cam
    result="systemtime"
    return result
  
def get_camerainfo(data):
    global content_txt
    global cam
    result=cgi.escape(cam.get_camerainfo())
    return content_txt+result
  
def unknowncmd(data):
    global content_txt
    return content_txt+"unknown command: "+data['cmd'].value

    
def unknownerror(data):
    global content_txt
    return content_txt+"command execution failed: "+data['cmd'].value
  
def nocmd():
    global content_txt
    return content_txt+"no command"
  
  
command_array = {
  "get_model"         :get_model,
  #"get_cameratime"    :get_cameratime,
  "get_widget_value"  :get_widget_value,
  "set_widget_value"  :set_widget_value,
  "get_widget_options":get_widget_options,
  "get_widget_label"  :get_widget_label,
  #"get_capturesetting":get_capturesetting,
  #"set_capturesetting":set_capturesetting,
  #"get_capturesetting_all_options":get_capturesetting_all_options,
  "get_latest_image"  :get_latest_image,
  "take_picture"      :take_picture,
  "get_abilities"     :get_abilities,
  "get_camerainfo"    :get_camerainfo
}


try:
  cam = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/schnapphoto")
  data = cgi.FieldStorage()
  result="" 
  if data.has_key( 'cmd' ):  
    command = data['cmd'].value
    try:
      result=command_array[command](data)
    except KeyError:
      result=unknowncmd(data)
  else:
    result=nocmd()
except:
  #result = content_txt+"connection to camerahost.py failed"
  result=content_txt+"could not connect to schnapphoto daemon"
  
print result