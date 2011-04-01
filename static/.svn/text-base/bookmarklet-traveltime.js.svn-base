/* driving travel time within Africa - bookmarklet for Ushahidi and CrowdMap
javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-traveltime.js";document.body.appendChild(s);void(0); */

djConfig = { parseOnLoad:true };
var gpTask,reactivator,wgs84,vectorLayer,originControl;
var rtPolygons=[];
var esriScript=document.createElement("script");
esriScript.src="http://serverapi.arcgisonline.com/jsapi/arcgis/?v=1.6";
esriScript.onload=function(){
	dojo.require("esri.tasks.gp");
	gpTask = new esri.tasks.Geoprocessor('http://173.201.21.209/HcTest/rest/services/AfLive/GPServer/MarketDistance');
	var newPt=document.createElement("script");
	newPt.src="http://trac.osgeo.org/openlayers/export/9597/trunk/openlayers/lib/OpenLayers/Handler/Point.js";
	newPt.onload=function(){
		var newDL=document.createElement("script");
		newDL.src="http://trac.osgeo.org/openlayers/export/9597/trunk/openlayers/lib/OpenLayers/Control/DrawFeature.js";
		newDL.onload=function(){
			var clickLayer = new OpenLayers.Layer.Vector("Click Layer");
			map.addLayers([clickLayer]);
			originControl = new OpenLayers.Control.DrawFeature(clickLayer, OpenLayers.Handler.Point);
			originControl.featureAdded=executeGPTask;
			map.addControl(originControl);
			originControl.activate();
		};
		document.body.appendChild(newDL);
	};
	document.body.appendChild(newPt);
};
document.body.appendChild(esriScript);

if(OpenLayers){
	/* add a legend explaining color rings */
	var explainer = document.createElement("div");
	explainer.style.position="fixed";
	explainer.style.left="30px";
	explainer.style.top="200px";
	explainer.style.borderColor="#000000";
	explainer.style.padding="5px";
	explainer.style.backgroundColor="#ffffff";
	explainer.style.color="#000000";
	explainer.innerHTML='Status: <span id="route_status">Click to start</span><hr/><span style="color:green">Two Hours</span><br/><span style="color:yellow">Four Hours</span><br/><span style="color:orange">Six Hours</span><br/><span style="color:red">Eight Hours</span><hr/><input type="button" id="resetBtn" value="Reset" onclick="resetButton();" style="display:none;"/><br/>From <a href="http://mappr.info/agmarketfinder/" target="_blank">ESRI\'s AgMarketFinder</a>';
	document.body.appendChild(explainer);
}

function resetButton(){
	document.getElementById("resetBtn").style.display="none";
	document.getElementById("route_status").innerHTML="Click to start";
	originControl.activate();
}
function executeGPTask(feature) {
	originControl.deactivate();
	document.getElementById("route_status").innerHTML="Sending...";
	wgs84 = new esri.SpatialReference({wkid:4326});
	var clickPoint = feature.geometry.getCentroid().transform(map.projection, map.displayProjection );
	clickPoint = new esri.geometry.Point( clickPoint.x, clickPoint.y, wgs84 );
	var clickPointSymbol = new esri.symbol.SimpleMarkerSymbol(esri.symbol.SimpleMarkerSymbol.STYLE_SQUARE, 8, new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_SOLID, new dojo.Color([0, 0, 0]), 2), new dojo.Color([255, 255, 255]));
    clickGraphic = new esri.Graphic(clickPoint, clickPointSymbol);
	var featureSet = new esri.tasks.FeatureSet();
	featureSet.features = [clickGraphic];
	var params = {"Input_Location": featureSet};
	gpTask.setOutputSpatialReference(wgs84);
	gpTask.submitJob(params,getGPResult,statusCallback);
}

function getGPResult(jobInfo) {
	gpTask.getResultData(jobInfo.jobId, "zipName", handleZipName, handleGPError);
	gpTask.getResultData(jobInfo.jobId, "Travel_Time_Stats", handleGPResults, handleGPError);    
}

var _statusMessages = {esriJobSucceeded:"Processing Complete", esriJobExecuting: "Processing", esriJobSubmitted: "Processing", esriJobFailed:"There was a problem processing the request.", esriJobWaiting:"Waiting to Process"};
function statusCallback(jobInfo) {
	var status = jobInfo.jobStatus;
	var cleanedMsg;
	try {
		cleanedMsg = eval("_statusMessages." + status);
	}
	catch (e) {
		cleanedMsg = "Processing.";
	}
	document.getElementById("route_status").innerHTML=cleanedMsg;
}

var _zipname = "";
function handleZipName(results, messages) {
	if (results) {
		_zipname = results.value.toString();
	}
}
function handleGPError(e) {
	alert("handleGPError " + e);
}

var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 1;
	layer_style.graphicOpacity = 0;
	layer_style.strokeColor="black";
var style_orange = OpenLayers.Util.extend({}, layer_style);
	style_orange.fillColor="orange";
var style_green = OpenLayers.Util.extend({}, layer_style);
	style_green.fillColor="green";
var style_red = OpenLayers.Util.extend({}, layer_style);
	style_red.fillColor="red";

function handleGPResults(results, messages) {
	if(vectorLayer){
		map.removeLayer(vectorLayer);
	}
	rtPolygons=[];
    vectorLayer = new OpenLayers.Layer.Vector("Drive Times", {style: layer_style});
	var routes = results.value.features.reverse();
	dojo.forEach(routes, function(route) {
		route.geometry.setSpatialReference(wgs84);
		for(var ring=0;ring<route.geometry.rings.length;ring++){
			var routeRing = route.geometry.rings[ring];
			var pointList=[];
			for(var pt=0;pt<routeRing.length;pt++){
				pointList.push(new OpenLayers.Geometry.Point( routeRing[pt][0] , routeRing[pt][1] ).transform(map.displayProjection,  map.projection));
			}
			var routeLinearRing = new OpenLayers.Geometry.LinearRing(pointList);
			var routePolygon;
		
			if (route.attributes.GRIDCODE == 2) {
				routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_green);
			} else if (route.attributes.GRIDCODE == 4) {
				routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]));
			} else if (route.attributes.GRIDCODE == 6) {
				routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_orange);
			} else if (route.attributes.GRIDCODE == 8) {
				routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_red);
			}
			rtPolygons.push({shape:routePolygon.geometry,driveTime:route.attributes.GRIDCODE});
			vectorLayer.addFeatures([routePolygon]);
		}
	});
	rtPolygons.reverse();
	map.addLayer(vectorLayer);
	document.getElementById("resetBtn").style.display="block";
	document.getElementById("route_status").innerHTML="Done";
}

var lastLyrId = populateReportLayer();
setInterval("populateReportLayer();",500);
function populateReportLayer(){
	if(!rtPolygons){return;}
	if(rtPolygons.length<1){return;}
	var reportLayer;
	for(var lyr=0;lyr<map.layers.length;lyr++){
		if(map.layers[lyr].name.indexOf("eports")!=-1){
			reportLayer=map.layers[lyr];
			if(reportLayer.id != lastLyrId){
				var ptList=reportLayer.features;
				for(var pt=0;pt<ptList.length;pt++){
					for(var crossPoly=0;crossPoly<rtPolygons.length;crossPoly++){
						if(rtPolygons[crossPoly].shape.intersects( ptList[pt].geometry )){
							ptList[pt].attributes.name+="<br/><b>Within " + rtPolygons[crossPoly].driveTime + " hour drive</b><br/>";
							break;
						}
					}
				}
				lastLyrId=reportLayer.id;
			}
			return reportLayer.id;
		}
	}
}
void(0);