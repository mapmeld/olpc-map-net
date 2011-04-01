/*bookmarklet-walpha.js for Ushahidi and CrowdMap
display weather charts at a few locations, tied into the timeline
prototype of working with other Wolfram Alpha apps*/


/*From widget: <script type="text/javascript" id="WolframAlphaScript9965b21b3968b6abc41143236b035c8c" src="http://www.wolframalpha.com/widget/widget.jsp?id=9965b21b3968b6abc41143236b035c8c"></script>
Which loads large iframe: http://www.wolframalpha.com/widget/input/?input=weather%20in%20%5B%2F%2Fplace%3APort-au-Prince%2C%20Haiti%2F%2F%5D%20from%20%5B%2F%2Fdate%3AApril%2015%2C%202010%2F%2F%5D%20to%20%5B%2F%2Fdate%3AApril%2030%2C%202010%2F%2F%5D&id=9965b21b3968b6abc41143236b035c8c&includepodid=WeatherCharts%3AWeatherData&podstate=Weather%20history_Month&podstate=Weather%20history_Week&podstate=Weather%20history_Show%20metric
Will make it scrollable*/

/*var waWidget = document.createElement('script')
waWidget.src="http://www.wolframalpha.com/widget/widget.jsp?id=9965b21b3968b6abc41143236b035c8c";
waWidget.id="WolframAlphaScript9965b21b3968b6abc41143236b035c8c";
document.body.appendChild(waWidget);*/

var lonlat = new OpenLayers.LonLat(-72.334671,18.550579).transform(map.displayProjection,map.projection);
map.setCenter(lonlat, 7);

var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 0.2;
	layer_style.graphicOpacity = 1;

var vectorLayer = new OpenLayers.Layer.Vector("Simple Geometry", {style: layer_style});
	map.addLayer(vectorLayer);

var style_blue = OpenLayers.Util.extend({}, layer_style);
	style_blue.strokeColor = "blue";
	style_blue.fillColor = "blue";
	style_blue.graphicName = "star";
	style_blue.pointRadius = 20;
	style_blue.strokeWidth = 3;
	style_blue.rotation = 45;
	style_blue.strokeLinecap = "butt";

var point = new OpenLayers.Geometry.Point(-72.294502,18.57743).transform(map.displayProjection,map.projection);
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
			//no need to update
			return;
		}
	}
	if(startTime > today){  // don't ask for future sensor values
		startTime = new Date(today - 1000 * 60 * 60 * 24 * 140); // go two weeks back
		endTime = today;
	}
	else if(endTime > today){  // don't ask future sensor values
		endTime = today;
	}
	var monthNs=["January","February","March","April","May","June","July","August","September","October","November","December"];
	var walpha={
		place:escape("Port-au-Prince, Haiti"),
		startTime: escape(monthNs[startTime.getMonth()] + " " + startTime.getDate() + ", " + startTime.getFullYear()),
		endTime:escape(monthNs[endTime.getMonth()] + " " + endTime.getDate() + ", " + endTime.getFullYear())
	};
	pointFeature.attributes={name:"<div style='width:500px;max-height:300px;overflow:scroll;'><iframe scrollable='yes' style='border:none;' width='480' height='1702' src='http://www.wolframalpha.com/widget/input/?input=weather%20in%20[%2F%2Fplace%3A"+walpha.place+"%2F%2F]%20from%20[%2F%2Fdate%3A"+walpha.startTime+"%2F%2F]%20to%20[%2F%2Fdate%3A"+walpha.endTime+"%2F%2F]&id=9965b21b3968b6abc41143236b035c8c&includepodid=WeatherCharts%3AWeatherData&podstate=Weather%20history_Month&podstate=Weather%20history_Week&podstate=Weather%20history_Show%20metric'></iframe></div>"};
	pointFeature.attributes.name="<a href='http://www.wolframalpha.com/input/?i=weather+in+"+walpha.place.replace("%20","+")+"+from+"+walpha.startTime.replace("%20","+")+"+to+"+walpha.endTime.replace("%20","+")+"' target='_blank'>Click for Day-by-Day Weather - New Window</a><br/>"+pointFeature.attributes.name;
	lastTimeSet = [startTime,endTime];
	return lastTimeSet;
}
function daysInMonth(iMonth, iYear){
	return 32 - new Date(iYear, iMonth, 32).getDate();
}

// javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-walpha.js";document.body.appendChild(s);void(0);