/* US and Canada travel times bookmarklet; for Ushahidi and CrowdMap
javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-travel-us-ca.js";document.body.appendChild(s);void(0);
*/

djConfig = { parseOnLoad:true };
var gpTask,reactivator,wgs84,vectorLayer,originControl;
var rtPolygons=[];

/* */
var esriScript=document.createElement("script");
esriScript.src="http://serverapi.arcgisonline.com/jsapi/arcgis/?v=1.6";
esriScript.onload=function(){
	dojo.require("esri.map");
	dojo.require("esri.tasks.gp");
	gpTask = new esri.tasks.Geoprocessor("http://sampleserver1.arcgisonline.com/ArcGIS/rest/services/Network/ESRI_DriveTime_US/GPServer/CreateDriveTimePolygons");
	var newPt=document.createElement("script");
	newPt.src="http://trac.osgeo.org/openlayers/export/9597/trunk/openlayers/lib/OpenLayers/Handler/Point.js";
	newPt.onload=function(){
		var newDL=document.createElement("script");
		newDL.src="http://trac.osgeo.org/openlayers/export/9597/trunk/openlayers/lib/OpenLayers/Control/DrawFeature.js";
		newDL.onload=function(){
			var clickLayer = new OpenLayers.Layer.Vector("Click Layer");
			map.addLayers([clickLayer]);
			originControl = new OpenLayers.Control.DrawFeature(clickLayer,OpenLayers.Handler.Point);
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
	/* add a legend to explain distance rings */
	var explainer = document.createElement("div");
	explainer.style.position="fixed";
	explainer.style.left="30px";
	explainer.style.top="200px";
	explainer.style.borderColor="#000000";
	explainer.style.padding="5px";
	explainer.style.backgroundColor="#ffffff";
	explainer.style.color="#000000";
	explainer.innerHTML='Status: <span id="route_status">Click to start</span><hr/><span style="color:green">Two Minutes</span><br/><span style="color:orange">Four Minutes</span><br/><span style="color:red">Eight Minutes</span><hr/><input type="button" id="resetBtn" value="Reset" onclick="resetButton();" style="display:none;"/><br/>From <a href="http://resources.esri.com/help/9.3/arcgisserver/apis/javascript/arcgis/demos/geoprocessor/gp_servicearea.html" target="_blank">ESRI\'s Service Area code</a>';
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
	var clickPoint = feature.geometry.getCentroid().transform(map.projection, map.displayProjection);
	clickPoint = new esri.geometry.Point( clickPoint.x, clickPoint.y, wgs84 );
	var pointSymbol = new esri.symbol.SimpleMarkerSymbol();
	pointSymbol.setOutline = new esri.symbol.SimpleLineSymbol(esri.symbol.SimpleLineSymbol.STYLE_SOLID,new dojo.Color([255,0,0]), 1);
	pointSymbol.setSize(5);
	pointSymbol.setColor(new dojo.Color([0,255,0,0.25]));
	var graphic = new esri.Graphic(clickPoint,pointSymbol);
	var features= [];
	features.push(graphic);
	var featureSet = new esri.tasks.FeatureSet();
	featureSet.features = features;
	var params = { "Input_Location":featureSet, "Drive_Times":"2 4 8" };
	gpTask.execute(params, getDriveTimePolys);
}
var layer_style = OpenLayers.Util.extend({},OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 1;
	layer_style.graphicOpacity = 0;
	layer_style.strokeColor="black";
var style_orange = OpenLayers.Util.extend({}, layer_style);
	style_orange.fillColor="orange";
var style_green = OpenLayers.Util.extend({}, layer_style);
	style_green.fillColor="green";
var style_red = OpenLayers.Util.extend({}, layer_style);
	style_red.fillColor="red";

function getDriveTimePolys(results, messages) {
	document.getElementById("route_status").innerHTML="Adding to map...";
	if(vectorLayer){
		map.removeLayer(vectorLayer);
	}
	rtPolygons=[];
	vectorLayer = new OpenLayers.Layer.Vector("Drive Times", {style:layer_style});
	map.addLayer(vectorLayer);
	var routes = results[0].value.features;
	for (var f=0; f<routes.length; f++) {
		var pointList=[];
		var routeRing = routes[f].geometry.rings[0];
		for(var pt=0;pt<routeRing.length;pt++){
			pointList.push(new OpenLayers.Geometry.Point( routeRing[pt][0] ,routeRing[pt][1] ).transform(map.displayProjection,  map.projection));
		}
		var routeLinearRing = new OpenLayers.Geometry.LinearRing(pointList);
		var routePolygon;
		if(f == 0){
			routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_red);
		}else if(f == 1){
			routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_orange);
		}else if(f == 2){
			routePolygon = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Polygon([routeLinearRing]),null,style_green);
		}
		rtPolygons.push({shape:routePolygon.geometry,driveTime:f});
		vectorLayer.addFeatures([routePolygon]);
	}
	rtPolygons.reverse();
	document.getElementById("resetBtn").style.display="block";
	document.getElementById("route_status").innerHTML="Done";
}
void(0);