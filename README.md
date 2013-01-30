CameraPi
========

Middleware and webapp-interface to remotely control your digital camera with your mobile device

About this project
==================

This project is based on ideas of David Hunt (http://davidhunt.ie/?p=2641) and Kürth Williams (http://islandinthenet.com/2012/08/23/hdr-photography-with-raspberry-pi-and-gphoto2/) who describe different approaches on how to control a digital camera remotely with a Raspberry Pi mini computer.
The vision is to have a battery powered linux system sitting closed to the camera and function as a "second brain" for it, enhancing the built-in features in many ways (bracketing, focus stacking, time lapse, remote control....)

This implementation offers a python back-end and a HTML5 user interface for remote camera control via libgphoto2. 
The backend is aimed to work with all cameras supported by gPhoto2 (http://www.gphoto.org/proj/libgphoto2/support.php). The frontend should work with any device supported by jquery mobile (http://jquerymobile.com/gbs/)

planned features:
- control camera in a libgphoto-session (keep session open instead of time consuming repeated inits for every shot)
- use your mobile device (smartphone) to
  - see and alter capture settings (like aperture, shutter speed etc)
  - monitor camera status (battery life etc)
  - shoot pictures
  - shoot bracketing series
  - shoot time lapse series
  - combined bracketing and time lapse series
  - see previews
  - browse camera roll
  - geotag pictures using your smartphone's GPS
  - synchronise client's / camera's clock and timezone
 
Current status
==============

Right now, the project is still in "proof of concept" status. A neat web interface exists, the backend connects with the gphoto libraries and reading of capture settings works.
Next steps:
- write back altered (capture) settings
- wire everything together for bracketing
- read and write back files from camera
- retrieve GPS postition from client and write them into EXIF block
- enable tethering (initiate actions when camera button is pressed)
- etc

How it works
============

The backend is mainly running a gphoto session as a daemon. It receives commands from a CGI-script through the pyro framework.
The CGI-script itself simply translates URL commands into python calls.
The backend heavily relies on piggyphoto, the python bindings for libgphoto

The frontend is based on jquery mobile. It's a mobile web app that queries the backend dynamically through ajax calls.

System requirements
===================

- libghoto2 (deleloped on version 2.5, don't know about earlier versions)
- Python 2.7 (didn't try python 3 yet)
- These Python modules:
  - Pyro4
  - <tbd>
- piggyphoto (find it on github, make sure to get the latest version / trunk)
- jquery mobile
- a webserver (apache), configured to execute CGI scripts

as a client, any recent web browser will do.

recommended hardware setup
==========================
- A digital camera that is capable of tethered shootings with gPhoto. I used a Nikon D40X for development.
- A linux system that connects to the camera via usb. In my case, it's a Raspberry Pi with the latest Raspbian Wheezy
- A Wifi-adapter running in host mode (so you can connect to the host with your smartphone if you do shootings outside)
- If you want to move around with your camera and system, a battery power supply my be usefull. I decided to build my own power supply with two LiPo batteries and a step-up DC/DC converter, fitting nicely together with the RasPi and a switch into a little box that sits on the flash mount of my DSLR.
- A smartphone or other mobile device with a recent web browser and Wi-Fi. I personally use an iPhone 4.
