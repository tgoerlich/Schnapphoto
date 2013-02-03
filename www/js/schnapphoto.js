// schnapphoto.js
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

    
    
    function updateClock (element)
    {
	var currentTime = new Date ( );
	var currentHours = currentTime.getHours ( );
	var currentMinutes = currentTime.getMinutes ( );
	var currentSeconds = currentTime.getSeconds ( );

	var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds;
	
	element.html(currentTimeString);
    }


    function click()
    {
      picturecount=$('#picturecount').val();
      bracketinglayers=$('#bracketinglayers').val();
      exposurecompensation=$('#evstops').val()
      delay=$('#delay').val();
      $.ajax( 
      {
	type: 'get',
	url: '/cgi-bin/schnapphoto_cgi.py',
	data: 'cmd=take_picture&picturecount='+picturecount+'&bracketinglayers='+bracketinglayers+'&exposurecompensation='+exposurecompensation+'&delay='+delay,
	success: function( data ) {
	  alert(data);
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

    function initiate_geolocation() {  
      navigator.geolocation.getCurrentPosition(handle_geolocation_query);  
    }  
    
    function handle_geolocation_query(position){  
      $('#gps_lat').html(position.coords.latitude);
      $('#gps_long').html(position.coords.longitude);
    }  
        

$(document).ready(function () {
	get_cameraclient( $('#camidentifier'),"get_model","")

	install_widget( $('#shutterspeed'),"get_capturesetting","shutterspeed2")
	install_widget( $('#fnumber'),"get_capturesetting","f-number")
	install_widget( $('#exposurecompensation'),"get_capturesetting","exposurecompensation")
	install_widget( $('#aelaflmode'),"get_capturesetting","aelaflmode")

	setInterval('updateClock($("#clientclock"))', 1000);

	$("#click_button").on("click",function(event, ui) {
		click();
	});
	$('#gps_long').html="hello world";
	initiate_geolocation();
  
}); 
