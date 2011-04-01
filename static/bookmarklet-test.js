/* bookmarklet-test.js for Ushahidi and CrowdMap */
/* javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-test.js";document.body.appendChild(s);void(0); */

var lonlat = new OpenLayers.LonLat((-80-1/60-43/60/60) ,(39+46/60+55/60/60) ).transform(map.displayProjection,  map.projection);

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

var point = new OpenLayers.Geometry.Point((-80-1/60-43/60/60) ,(39+46/60+55/60/60)).transform(map.displayProjection,  map.projection);
var pointFeature = new OpenLayers.Feature.Vector(point,null,style_blue);
pointFeature.attributes = {name:"<img src='http://waterdata.usgs.gov/nwisweb/graph?agency_cd=USGS&site_no=394655080014301&parm_cd=72019&period=3' height='300' width='400'/>"};

var lastLyrId = populateReportLayer();
setInterval("populateReportLayer();",500);

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
void(0);