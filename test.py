import schnapphoto		

cam = schnapphoto.CameraHost("true")
print cam.get_model()
#print cam.get_capturesetting("f-number")
#print cam.get_capturesetting_all_options("f-number")
#print "-------------------------"
#print cam.get_capturesetting_all_options("f-number")
#cam.set_capturesetting("f-number","f/4.5")
#print cam.get_capturesetting("f-number")
#print cam.get_capturesetting("f-number")
#print cam.pictureloop(loops=1,layers=3,steps=15,bracketingtype="exposurecompensation",delay=0), "pictures taken"
#print cam.pictureloop(loops=1,layers=3,steps=5,bracketingtype="shutterspeed2",delay=0), "pictures taken"
#print cam.trigger_picture()
#print cam.cam.abilities.operations
#print cam.get_abilities("operations")
#print cam.get_camerainfo()

#print cam.get_file_index()

# this returns "piggyphoto.libgphoto2error: Bad parameters (-2)" even with the NIKON attached:
#print cam.cam.get_config()
#print dir(cam.cam.config.main.actions)

widget=cam.cam.config.get_child_by_name("shutterspeed2")
print widget.name
print cam.get_widget_value("shutterspeed2")
print cam.get_widget_options("shutterspeed2")
cam.set_widget_value("shutterspeed2","1/30")
#cam.list_all_config()
cam.close()