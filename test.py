import schnapphoto		

cam = schnapphoto.CameraHost("true")
#print cam.get_model()
print cam.get_capturesetting("f-number")
#print cam.get_capturesetting_all_options("f-number")
print "-------------------------"
#print cam.get_capturesetting_all_options("f-number")
cam.set_capturesetting("f-number","f/4.2")
print cam.get_capturesetting("f-number")
#print cam.get_capturesetting("f-number")
print cam.pictureloop(count=1,layers=3,evsteps=6,delay=0), "pictures taken"
#print cam.trigger_picture()