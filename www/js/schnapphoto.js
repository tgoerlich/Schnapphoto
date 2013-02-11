// SCHNAPPHOTO
// Middleware and webapp to remotely control your digital camera with a mobile device
// Copyright (c) 2013 Thomas Goerlich 
//
// https://github.com/tgoerlich/Schnapphoto
//
// about this file:
// jscript functionality for web frontend
// querys schnapphoto_cgi

    function get_cameraclient(element_id, command, attribute)
    {
    element = $(element_id)
    $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=' + command + '&attribute=' + attribute,
	success: function( data ) {
	  if (data=="no host") {
	    alert("could not connect to schnapphoto daemon"); 
	  }
	  element.html(data);
	}
      } );
    }
     
 
     
    function populate_selectbox(element,command,attribute)
    {    
      var temp = []
      var value = '';
      var selected=0;
      var output = [];
      var result=1;
      $(element)
	.find('option')
	.remove()
	.end()
	.append('<option value="0">loading values...</option>')
	//.selectmenu('disable')
	//.selectmenu('refresh')
      ;
      
      //pull options from camera, insert in select box
      $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=' + 'get_capturesetting_all_options' + '&attribute=' + attribute,
	success: function( data ) {
	      //$("#console").html("success function");
	      tempstr=data
	      var temp = new Array()
	      temp = tempstr.split(',');
	      //$("#console").html($(temp));
	      for(var i = 0, len = temp.length; i < len; i++){
		//instead of appending each `<option>` element, it is a better practice to either concoct a string of all the HTML or create an array that will later be turned into a string (here we are pushing new indexes onto an `output` array)
		output.push('<option value="' + temp[i]+'">' + temp[i] + '</option>');
	      }
	      //$("#console").html("end loop");
	      $(element)
		.find('option')
		.remove()
		.end()
		.append(output.join(''))
		.selectmenu('enable')
		.selectmenu('refresh');
	      ;
	      result=0;
	      // pull value from camera, select option in select box
	      selectbox_getvalue($(element),command,attribute);
	}
      } );
      return result;
    }
    
    function selectbox_getvalue(element,command,attribute)
    //read widget value and set selectmenu 
    {

      $(element).selectmenu('disable')

      $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=' + 'get_capturesetting' + '&attribute=' + attribute,
	success: function( data ) {
	      $(element)
		.val(data.replace('\n',''))
		.selectmenu({ icon: "star" })
		.selectmenu('enable')
		.selectmenu('refresh')
		;
	      $("#console").html(data);
	}
      } );
    }
    
    
    function selectbox_setvalue(element,command,attribute)
    // read selectmenu value and store setting in camera
    {
      value=$(element).val();
      $.ajax(
	{
	  type: 'get',
	  url: '/cgi-bin/schnapphoto_cgi.py',
	  data: 'cmd=' + 'set_capturesetting' + '&attribute=' + attribute + '&value=' + value,
	  success: function( data ) {
	    //alert(data);
	  }
	}
      );
    }

    function install_widget(element,command,attribute)
    {
      populate_selectbox(element,command,attribute)     
      //catch event "change", push new value to camera when changed
      $(element).on("change",function(event, ui) {
	selectbox_setvalue($(element),"set_capturesetting",attribute);
      });
    }

    
    
    function updateClock (element1, element2)
    {
	var currentTime = new Date ( );
	element1.html(currentTime.getHours()+ ":" + currentTime.getMinutes() + ":" + currentTime.getSeconds());
	element2.html(currentTime.getDate()+"."+currentTime.getMonth()+"."+currentTime.getFullYear());
    }


    function click()
    {
      picturecount=$('#picturecount').val();
      bracketinglayers=$('#bracketinglayers').val();
      bracketingtype=$('#bracketingtype').val();
      stops=$('#stops').val()
      delay=$('#delay').val();
      $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=take_picture&picturecount='+picturecount+'&bracketinglayers='+bracketinglayers+'&bracketingtype='+bracketingtype+'&stops='+stops+'&delay='+delay,
	success: function( data ) {
	}
      });
    }
    
    function changeTheme() {
	var theme = $("#ddlTheme :selected").val();
	var cssUrl = 'css/themes/you-can-red.css';

	var themeStyle = $("#theme-style");
	themeStyle.attr({
	    rel:  "stylesheet",
	    type: "text/css",
	    href: cssUrl
	}); 

    }

    function geotrack_start() 
    {  
      window.watchID=navigator.geolocation.watchPosition(geolocation_watch, geolocation_error);  
    }  
    
    
    function geotrack_stop()
    {
       navigator.geolocation.clearWatch(window.watchId);
    }
    
    function geolocation_watch(position)
    {
      $('#gps_lat').html(position.coords.latitude);
      $('#gps_long').html(position.coords.longitude);
      var currentTime = new Date ( );
      var sun = new SunriseSunset(currentTime.getUTCFullYear(),currentTime.getUTCMonth(),currentTime.getUTCDate(),position.coords.latitude,position.coords.longitude );
      var sunset=sun.sunsetLocalHours(currentTime.getTimezoneOffset()/60);
      ssmin=(sunset*60)%60
      ssmin=ssmin-(ssmin%1)
      sshours=sunset-(sunset%1)
      var sunrise=sun.sunriseLocalHours(currentTime.getTimezoneOffset()/60);
      srmin=(sunrise*60)%60
      srmin=srmin-(srmin%1)
      srhours=sunrise-(sunrise%1)
      $('#sunset').html(sshours+":"+ssmin+"  ("+sunset+")");
      $('#sunrise').html(srhours+":"+srmin+"  ("+sunrise+")");
    }
    
    function geolocation_error()
    {
    }
    
    function camerainfo(element)
    {
       $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=get_camerainfo',
	success: function( data ) {
	  $(element).html(data);
	}
      });
    }
    
    
    function unlock_features(element,ability)
    {
      $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=get_abilities&ability='+ability,
	success: function( data ) {
	  if (data=="0")
	  {
	    $(element).button('disable');
	  }
	  else
	  {
	    $(element).button('enable');
	  }
	}
      });
    }
        

$(document).ready(function () {

// 	$('#takepictures').button('disable');
// 	$('#viewcameraroll').button('disable');

	get_cameraclient( $('#camidentifier'),"get_model","")

	install_widget( $('#shutterspeed'),"get_capturesetting","shutterspeed2")
	install_widget( $('#fnumber'),"get_capturesetting","f-number")
	install_widget( $('#exposurecompensation'),"get_capturesetting","exposurecompensation")
	install_widget( $('#aelaflmode'),"get_capturesetting","aelaflmode")
	install_widget( $('#capturemode'),"get_capturesetting","capturemode")
	install_widget( $('#autofocusarea'),"get_capturesetting","autofocusarea")
	install_widget( $('#exposurelock'),"get_capturesetting","exposurelock")
	install_widget( $('#expprogram'),"get_capturesetting","expprogram")
	install_widget( $('#flashmode'),"get_capturesetting","flashmode")
	install_widget( $('#focusmode2'),"get_capturesetting","focusmode2")
	install_widget( $('#assistlight'),"get_capturesetting","assistlight")
	install_widget( $('#exposuremetermode'),"get_capturesetting","exposuremetermode") 
	install_widget( $('#focallength'),"get_capturesetting","focallength") 
	install_widget( $('#focusmetermode'),"get_capturesetting","focusmetermode") 
	install_widget( $('#focusmode'),"get_capturesetting","focusmode") 
	install_widget( $('#imagequality'),"get_capturesetting","imagequality") 
	install_widget( $('#imagereview'),"get_capturesetting","imagereview") 
	install_widget( $('#nikonflashmode'),"get_capturesetting","nikonflashmode")
	install_widget( $('#tonecompensation'),"get_capturesetting","tonecompensation")

	
	
	
	
	//config.main.capturesettings
	//'aelaflmode', 'assistlight', 'autofocusarea','capturemode', 'exposurecompensation', 'exposurelock','expprogram', 'f-number', 'flashexposurecompensation', 'flashmode', 'focusmode2','shutterspeed2'
	//'afbeep',  'burstnumber','filenrsequencing', 'flashmodemanualpower',   
	//  'imagerotationflag', 'isoautohilimit', 'longexpnr', 'maximumshots', 'minimumshutterspeed', 'nocfcardrelease', 'optimizeimage', 'remotetimeout', 'saturation', 'selftimerdelay', 'sharpening', 'shutterspeed',
	//'exposuremetermode', 'flexibleprogram', 'focallength', 'focusmetermode', 'focusmode','hueadjustment', 'imagequality', 'imagereview', 'nikonflashmode','tonecompensation', 'whitebiaspreset0', 'whitebiaspreset1', 'whitebiaspresetno'
	
	//config.main.actions
	//autofocusdrive
	
	//config.main.imgsettings
	//'autoiso', 'colormodel', 'imagesize', 'iso', 'isoauto', 'whitebalance'
	
	//config.main.settings
	//'capturetarget', 'datetime', 'fastfs', 'imagecomment', 'imagecommentenable', 'lcdofftime', 'recordingmedia'
	
	//config.main.status
	//'acpower', 'aelocked', 'aflocked', 'apertureatmaxfocallength', 'apertureatminfocallength', 'batterylevel', 'externalflash', 'flashcharged', 'flashopen', 'lightmeter', 'lowlight', 'maxfocallength', 'minfocallength', 'orientation'
	
	$('#flip-geotracking').on("slidestop",function(event, ui) {
	  if ($('#flip-geotracking').val()=="on")
	  {
	    geotrack_start();
	  }
	  else
	  {
	    geotrack_stop();
	  }
	});

	setInterval('updateClock($("#time"),$("#date"))', 1000);

	$("#click_button").on("click",function(event, ui) {
		click();
	});

	camerainfo('#camerainfotext')
	
//	unlock_features('#takepictures','operations');
// 	unlock_features('#viewcameraroll','file_operations');


}); 
