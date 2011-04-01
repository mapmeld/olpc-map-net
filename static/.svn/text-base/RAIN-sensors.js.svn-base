//RAIN-sensors.js
//Live water quality and temperature from http://www.3rain.org
//Archive graphs from USGS
//Will soon be expanded to Allegheny River and West Virginia (upper Monongahela)

var sensors=[];
var sensor_features=[];
var lonlat = new OpenLayers.LonLat((-80-1/60-43/60/60) ,(39+46/60+55/60/60) ).transform(map.displayProjection,  map.projection);

map.setCenter(lonlat,9);

// RAIN sensors
	sensors=[];
	sensors.push({
		name:"M88 - RAIN",
		programID:"M88",
		source:"http://3rain.org",
		latlng:[39.754183,-79.927282],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"M85 - RAIN",
		programID:"M85",
		source:"http://3rain.org",
		latlng:[39.8083197251179,-79.9185967398777],
		senses:["pH","conductivity","temperature"]
	});	
	sensors.push({
		name:"M71 - RAIN",
		programID:"M71",
		source:"http://3rain.org",
		latlng:[39.9481433622391,-79.9504881032242],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"M57 - RAIN",
		programID:"M57",
		source:"http://3rain.org",
		latlng:[40.0214710839213,-79.9068400041702],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"M46 - RAIN",
		programID:"M46",
		source:"http://3rain.org",
		latlng:[40.1025746897488,-79.8425285482833],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"M25 - RAIN",
		programID:"M25",
		source:"http://3rain.org",
		latlng:[40.2501207018161,-79.9199118531109],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"M4 - RAIN",
		programID:"M4",
		source:"http://3rain.org",
		latlng:[40.4101827295744,-79.954605879819],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"O4 - RAIN",
		programID:"O4",
		source:"http://3rain.org",
		latlng:[40.4928209170082,-80.0714805992268],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"MY1 - RAIN",
		programID:"MY1",
		source:"http://3rain.org",
		latlng:[40.3385882095959,-79.8602571622452],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"A8 - RAIN",
		programID:"A8",
		source:"http://3rain.org",
		latlng:[40.4849949071367,-79.8891466910797],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"MR4 - RAIN",
		programID:"MR4",
		source:"http://3rain.org",
		latlng:[40.0158951137903,-79.8311741131719],
		senses:["pH","conductivity","temperature"]
	});
	sensors.push({
		name:"MT2 - RAIN",
		programID:"MT2",
		source:"http://3rain.org",
		latlng:[39.9804107233413,-80.0331444698185],
		senses:["pH","conductivity","temperature"]
	});
	//USGS sensors
	sensors.push({
		name:"Dunkard Creek at Shannonpin",
		programID:"03072000|394533079581501",  // location has both USGS surface water and water quality gauges
		source:"http://water.usgs.gov",
		latlng:[39.7592449,-79.9706152],
		senses:["flow","depth","|","temperature","conductivity","pH"] // include a "|" sense to separate requests to make from each gauge
	});
	sensors.push({name:"Greene County Groundwater Observation",programID:"394655080014301",source:"http://water.usgs.gov",latlng:[39.78202239,-80.0283945],senses:["gw-depth"]});
	sensors.push({name:"Cheat River at Lake Lynn",programID:"03071600",source:"http://water.usgs.gov",latlng:[39.72091177,-79.8553338],senses:["precipitation"]});
	sensors.push({name:"Mon near Masontown",programID:"03072655",source:"http://water.usgs.gov",latlng:[39+49/60+30/60/60,-79-55/60-23/60/60],senses:["flow","depth"]});
	sensors.push({name:"Mon at Maxwell L&D",programID:"03073751",source:"http://water.usgs.gov",latlng:[39+59/60+50.68/60/60,-79-57/60-32.19/60/60],senses:["depth"]});
	sensors.push({name:"Redstone Creek at Waltersburg",programID:"03074500",source:"http://water.usgs.gov",latlng:[39+58/60+48/60/60,-79-45/60-52/60/60],senses:["flow","depth"]});
	sensors.push({name:"Mon at Charleroi",programID:"03075000",source:"http://water.usgs.gov",latlng:[40+8/60+58/60/60,-79-54/60-6/60/60],senses:["depth"]});
	sensors.push({name:"Mon at Elizabeth",programID:"03075070",source:"http://water.usgs.gov",latlng:[40+15/60+44/60/60,-79-54/60-5/60/60],senses:["flow","depth","temperature","conductivity","pH","dissolved oxygen"]});
	sensors.push({name:"Mon at Braddock",programID:"03085002",source:"http://water.usgs.gov",latlng:[40+23/60+33/60/60,-79-51/60-37/60/60],senses:["depth"]});

	sensors.push({name:"Turtle Creek at Wilmerding",programID:"03084698",source:"http://water.usgs.gov",latlng:[40+23/60+39/60/60,-79-48/60-22/60/60],senses:["flow","depth"]});
	sensors.push({name:"Thompson Run at Turtle Creek",programID:"03084800",source:"http://water.usgs.gov",latlng:[40+24/60+19/60/60,-79-49/60-41/60/60],senses:["flow","depth"]});
	sensors.push({name:"Mon at Point State Park",programID:"03085152",source:"http://water.usgs.gov",latlng:[40+26/60+22/60/60,-80-39/60/60],senses:["depth"]});
	sensors.push({name:"Sawmill Run at Duquesne Heights",programID:"03085213",source:"http://water.usgs.gov",latlng:[40+25/60+58/60/60,-80-1/60-47/60/60],senses:["flow","depth"]});
	sensors.push({name:"Chartiers Creek at Carnegie",programID:"03085500",source:"http://water.usgs.gov",latlng:[40+24/60+2/60/60,-80-5/60-48/60/60],senses:["flow","depth"]});
	sensors.push({name:"Girtys Run at Millvale",programID:"03049819",source:"http://water.usgs.gov",latlng:[40+28/60+40.2/60/60,-79-58/60-12.1/60/60],senses:["flow","depth"]});
	sensors.push({name:"Ohio River at Sewickley",programID:"03086000",source:"http://water.usgs.gov",latlng:[40+32/60+57/60/60,-80-12/60-21/60/60],senses:["flow","depth"]});
	
	sensors.push({
		name:"Mon at Point Marion",
		programID:"394337079544201",
		source:"http://water.usgs.gov",
		latlng:[39+43/60+37/60/60,-79-54/60-42/60/60],
		senses:["temperature","conductivity","pH"]
	});
	sensors.push({
		name:"Youghiogheny River at Connellsville",
		programID:"03082500",
		source:"http://water.usgs.gov",
		latlng:[40+1/60+3/60/60,-79-35/60-38/60/60],
		senses:["flow","depth","temperature","conductivity","pH","dissolved oxygen"]
	});
	sensors.push({
		name:"Youghiogheny River at Sutersville",
		programID:"03083500",
		source:"http://water.usgs.gov",
		latlng:[40+14/60+24/60/60,-79-48/60-24/60/60],
		senses:["flow","depth","temperature","conductivity","pH","dissolved oxygen"]
	});
	sensors.push({
		name:"Allegheny at Acmetonia",
		programID:"03049640",
		source:"http://water.usgs.gov",
		latlng:[40+32/60+10/60/60,-79-48/60-54/60/60],
		senses:["temperature","conductivity","pH","dissolved oxygen"]
	});
	sensors.push({
		name:"Ohio River at Montgomery Dam",
		programID:"03108490",
		source:"http://water.usgs.gov",
		latlng:[40+38/60+56/60/60,-80-23/60-1/60/60],
		senses:["temperature","conductivity","pH","dissolved oxygen"]
	});

//point styles
var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 0.2;
	layer_style.graphicOpacity = 1;

//RAIN style
var style_blue = OpenLayers.Util.extend({}, layer_style);
	style_blue.strokeColor = "blue";
	style_blue.fillColor = "blue";
	style_blue.graphicName = "square";
	style_blue.pointRadius = 10;
	style_blue.strokeWidth = 3;
	style_blue.rotation = 45;
	style_blue.strokeLinecap = "butt";

//usgs style
var style_green = OpenLayers.Util.extend({}, style_blue);
	style_green.strokeColor = "green";
	style_green.fillColor = "green";

//add each sensor to the map
for(var s=0; s<sensors.length; s++){
	var point = new OpenLayers.Geometry.Point(sensors[s].latlng[1],sensors[s].latlng[0]).transform(map.displayProjection,map.projection);
	var pointFeature;
	if(sensors[s].source=="http://3rain.org"){
		//3rain.org
		pointFeature = new OpenLayers.Feature.Vector(point,null,style_blue);
		pointFeature.attributes={name:"loading sensor values"};
	}
	else{
		//USGS
		pointFeature = new OpenLayers.Feature.Vector(point,null,style_green);	
		pointFeature.attributes={name:getSensorValue(sensors[s])};
	}
	sensor_features.push(pointFeature);
}

//load data from 3rain.org
var rainScript=document.createElement("script");
rainScript.src="http://65.44.168.30/rain/script/rain.js";
rainScript.onload=updateSensors;
document.body.appendChild(rainScript);

//regularly update reports layer to make sure sensors are on the map
var lastLyrId = populateReportLayer();
setInterval("populateReportLayer();",500);
function populateReportLayer(){
	var reportLayer;
	for(var lyr=0;lyr<map.layers.length;lyr++){
		if(map.layers[lyr].name.indexOf("eports")!=-1){
			reportLayer=map.layers[lyr];
			if(reportLayer.id != lastLyrId){
				reportLayer.addFeatures(sensor_features);
				lastLyrId=reportLayer.id;
			}
			return reportLayer.id;
		}
	}
}

//sensor descriptions for popup windows
function updateSensors(startDate,endDate){
	//update each sensor
	for(var s=0; s<sensors.length; s++){
		sensor_features[s].attributes={name:getSensorValue(sensors[s])};
	}
}
function getSensorValue(sensor){
	if(sensor.source=="http://3rain.org"){
		var lv;
		switch(sensor.programID){
			case "M85":
				lv=get_content2();
				break;
			case "M88":
				lv=get_content1();
				break;
			case "MW2":
				lv=get_content13();
				break;
			case "M71":
				lv=get_content3();
				break;
			case "M57":
				lv=get_content4();
				break;
			case "M46":
				lv=get_content5();
				break;
			case "M25":
				lv=get_content6();
				break;
			case "M4":
				lv=get_content7();
				break;
			case "O4":
				lv=get_content8();
				break;
			case "MY1":
				lv=get_content9();
				break;
			case "A8":
				lv=get_content10();
				break;
			case "MR4":
				lv=get_content11();
				break;
			case "MT2":
				lv=get_content12();
				break;
		}
		return '<a href="http://www.3rain.org" target="_blank" style="font-weight:bold;">'+sensor.name+'</a><br/><table border="1">'+lv+'</table>';
	}
	else if(sensor.source=="http://water.usgs.gov"){
		var liveValues="";
		var senseIDs = sensor.programID.split("|");
		var senseStart = 0;
		for(var id=0;id<senseIDs.length;id++){
			for(var s=senseStart;s<sensor.senses.length;s++){
				if(sensor.senses[s] == "|"){
					senseStart=s+1;
					break;
				}
				var parsense = sensor.senses[s];
				parsense=parsense.toLowerCase()
				parsense=parsense.replace("ph","00400");
				parsense=parsense.replace("temperature","00010");
				parsense=parsense.replace("conductivity","00095");
				parsense=parsense.replace("precipitation","00045");
				parsense=parsense.replace("flow","00060");
				parsense=parsense.replace("gw-depth","72019");
				parsense=parsense.replace("depth","00065");
				parsense=parsense.replace("dissolved oxygen","00300");
				var src = "http://waterdata.usgs.gov/nwisweb/graph?agency_cd=USGS&site_no=" + senseIDs[id] + "&parm_cd=" + parsense + "&period=7";
				if(s==0){
					liveValues+="<div id='sensorframe_" + s + "' style='display:block;'>";
				}
				else{
					liveValues+="<div id='sensorframe_" + s + "' style='display:none;'>";
				}
				liveValues+="<span style='height:12pt;font-size:12pt;font-weight:bold;'>"+sensor.name+"</span><br/>";
				liveValues+="<a href='" + src + "' target='_blank'><img alt='Loading Graph...' src='" + src + " style='height:220px;border:none;' border='0' height='220' width='300'/></a></div>";
			}
			if(sensor.senses.length > 0){
				liveValues+="<hr/><div id='sensorScroll' style='text-align:center;'><input id='mySensorNext' type='button' value='Next' onclick='loadSensorFrame(0,1,"+sensor.senses.length+");'/></div>";
			}
		}
		return liveValues;
	}
	else{
		var liveValues='<div style="width:400px;font-size:10pt;text-align:left;height:400px;" height="400" width="400"><img alt="Loading graph..." src="'+sensor.programID+'" style="max-width:350px;max-height:350px;" height="200"/></div>';
		return liveValues;
	}
}

// scrolling between USGS sensor charts from a particular location
function loadSensorFrame(oldfrm,frm,length){
	byId('sensorframe_'+oldfrm).style.display="none";
	byId('sensorframe_'+frm).style.display="block";
	var scrollControl='';
	if(frm>0){
		scrollControl="<input id='mySensorPrev' type='button' value='Prev' onclick='loadSensorFrame("+frm+","+(frm-1)+","+length+");'/>";
		if(frm<length-1){
			scrollControl+="&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp";
		}
	}
	if(frm<length-1){
		scrollControl+="<input id='mySensorNext' type='button' value='Next' onclick='loadSensorFrame("+frm+","+(frm+1)+","+length+");'/>";
	}
	byId('sensorScroll').innerHTML=scrollControl;
}

//3rain.org helper functions
var tableend="";
function addCaption(val){return "";}
function addRow(name,val){return "<tr><td>" + name + "</td><td>" + val + "</td></tr>";}
function addRow2(val){return "<tr><td colspan='2'>" + val + "</td></tr>";}
function byId(id){return document.getElementById(id)}

// javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/RAIN-sensors.js";document.body.appendChild(s);void(0);