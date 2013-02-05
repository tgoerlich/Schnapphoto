import schnapphoto		

cam = schnapphoto.CameraHost("true")
print cam.get_model()
print cam.get_capturesetting("f-number")
print cam.get_capturesetting_all_options("f-number")
#print "-------------------------"
#print cam.get_capturesetting_all_options("f-number")
#cam.set_capturesetting("f-number","f/4.5")
#print cam.get_capturesetting("f-number")
#print cam.get_capturesetting("f-number")
#print cam.pictureloop(loops=1,layers=3,steps=15,bracketingtype="exposurecompensation",delay=0), "pictures taken"
#print cam.pictureloop(loops=1,layers=3,steps=5,bracketingtype="shutterspeed2",delay=0), "pictures taken"
#print cam.trigger_picture()
#print cam.cam.abilities.operations
print cam.get_abilities("operations")
cam.close()