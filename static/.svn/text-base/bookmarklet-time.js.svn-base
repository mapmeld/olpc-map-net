/* bookmarklet-time.js for Ushahidi and CrowdMap
adjust a USGS flow chart based on the times selected in the timeline */
/* javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-time.js";document.body.appendChild(s);void(0); */

var lonlat = new OpenLayers.LonLat((-80-1/60-43/60/60) ,(39+46/60+55/60/60) ).transform(map.displayProjection,  map.projection);

map.setCenter(lonlat, 7);

var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 0.2;
	layer_style.graphicOpacity = 1;

var style_blue = OpenLayers.Util.extend({}, layer_style);
	style_blue.strokeColor = "blue";
	style_blue.fillColor = "blue";
	style_blue.graphicName = "star";
	style_blue.pointRadius = 20;
	style_blue.strokeWidth = 3;
	style_blue.rotation = 45;
	style_blue.strokeLinecap = "butt";

var point = new OpenLayers.Geometry.Point((-80-1/60-43/60/60) ,(39+46/60+55/60/60)).transform(map.displayProjection,  map.projection);
var pointFeature = new OpenLayers.Feature.Vector(point,null,style_blue);

var lastLyrId = populateReportLayer();
var lastTimeSet = updateSensors();
setInterval("populateReportLayer();updateSensors();",500);

function populateReportLayer(){
	var reportLayer;
	for(var lyr=0;lyr<map.layers.length;lyr++){
		if(map.layers[lyr].name.indexOf("eports")!=-1){
			reportLayer=map.layers[lyr];
			if(reportLayer.id != lastLyrId){
				reportLayer.addFeatures([pointFeature]);
				lastLyrId = reportLayer.id;
			}
			return reportLayer.id;
		}
	}
}

function updateSensors(){
	var startTime=timeline.startTime;
	var endTime=timeline.endTime;
	var today=new Date();
	if(lastTimeSet){
		if((startTime==lastTimeSet[0])&&(endTime==lastTimeSet[1])){
			/* no need to update */
			return;
		}
	}
	if(startTime > today){  /* don't ask for future sensor values */
		startTime = new Date(today - 1000 * 60 * 60 * 24 * 140); /* go two weeks back */
		endTime = today;
	}
	else if(endTime > today){  /* don't ask for future sensor values */
		endTime = today;
	}
	fillMonth = startTime.getMonth()*1+1;
	if(fillMonth < 10){
		fillMonth=("_"+fillMonth).replace("_","0");
	}
	fillDay = Math.max(startTime.getDate(),1);
	if(fillDay < 10){
		fillDay=("_"+fillDay).replace("_","0");
	}
	fillMonth2 = endTime.getMonth()*1+1;
	if(fillMonth2 < 10){
		fillMonth2=("_"+fillMonth2).replace("_","0");
	}
	fillDay2 = Math.max(endTime.getDate(),1);
	if(fillDay2 < 10){
		fillDay2=("_"+fillDay2).replace("_","0");
	}
	pointFeature.attributes = {name:'<div id="usgsBox" width="330" height="230" style="width:330px;height:230px;">'+loadUSGS('http://waterdata.usgs.gov/nwis/dv/?dd_cd=04_00060_00003&format=img_default&site_no=03072000&begin_date='+startTime.getFullYear()+""+fillMonth+""+fillDay+'&end_date='+endTime.getFullYear()+""+fillMonth2+""+fillDay2)+'</div>'};
	lastTimeSet = [startTime,endTime];
	return lastTimeSet;
}

function loadUSGS(url){
	return '<iframe src="'+url+'" style="border:none;overflow:hidden;zoom:0.55;-moz-transform:scale(0.55);-moz-transform-origin: 0 0;-o-transform:scale(0.55);-o-transform-origin: 0 0;-webkit-transform:scale(0.55);-webkit-transform-origin: 0 0;" border="0" width="600" height="450"/>';
}
function daysInMonth(iMonth, iYear){
	return 32 - new Date(iYear, iMonth, 32).getDate();
}
function removePopup(){}

void(0);