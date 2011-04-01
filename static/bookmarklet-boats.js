/*bookmarklet-boats.js - a bookmarklet for Ushahidi and CrowdMap
Live boat positions around the BP / Deepwater oil drill*/

var lonlat = new OpenLayers.LonLat(-88.365997,28.736628).transform(map.displayProjection, map.projection);
map.setCenter(lonlat,7);

var layer_style = OpenLayers.Util.extend({},OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 0.2;
	layer_style.graphicOpacity = 1;

var style_blue = OpenLayers.Util.extend({}, layer_style);
	style_blue.strokeColor = "red";
	style_blue.fillColor = "white";
	style_blue.graphicName = "square";
	style_blue.pointRadius = 10;
	style_blue.strokeWidth = 3;
	style_blue.rotation = 0;
	style_blue.strokeLinecap = "butt";

var style_green={
	strokeColor: "#00FF00",
	strokeWidth: 3,
	strokeDashstyle: "solid",
	pointRadius: 6,
	pointerEvents: "visiblePainted"
};

/*load data from marinetraffic.com*/
var ships=[
	{id:366978490,
		name:"Kobe Chouest",
		size:"93 m X 19 m",
		photo:"http://mapmeld.appspot.com/kobe_chouest.jpg",
		callsign:"WDB9562"},
	{id:369804000,
		name:"Dante",
		size:"85 m X 18 m",
		photo:"http://photos.marinetraffic.com/ais/showphoto.aspx?mmsi=369804000&imo=9347346",
		callsign:"KUGY"},
	{id:366601000,
		name:"Mississippi Responder",
		size:"70 m X 15 m",
		photo:"http://media.kitsapsun.com/media/img/photos/2010/05/01/media_415db5f68a6744888443bc7a1b8e0d9e_t607.jpg",
		callsign:"WBO8584"},
	{id:576541000,
		name:"Ocean Project",
		size:"57m x 15m",
		photo:"http://www.marinetraffic.com/ais/icons/shipping_small.gif",
		callsign:"YJRF7"},
	{id:366811640,
		name:"Clay Ella",
		size:"50 m X 12 m",
		photo:"http://mapmeld.appspot.com/clay_ella.jpg",
		callsign:"WDB7446"},
	{id:576813000,
		name:"Express",
		size:"159m x 31m",
		photo:"http://www.shipspotting.com/photos/small/5/0/3/1080305.JPG",
		callsign:"YJSR8"}
];
var shipData=[];
var ship_features=[];
var shipDex=0;
var lastLyrId;
loadBoat();

/*sequentially load each boat's data through JavaScript*/
function loadBoat(){
	if(shipDex < ships.length){
		var boatScript=document.createElement("script");
		boatScript.src="http://mapmeld.appspot.com/boats?id=" + ships[shipDex].id + "&name=" + ships[shipDex].name + "&photo=" + ships[shipDex].photo+ "&size=" + ships[shipDex].size + "&call=" + ships[shipDex].callsign;
		boatScript.onload=loadBoat;
		shipDex++;
		document.body.appendChild(boatScript);
	}
	else{
		lastLyrId = populateReportLayer();
		setInterval("populateReportLayer();",500);
	}
}
function datastoreBoat(xmlStr,name,photo,call){
	var xmlArr=xmlStr.split("TIMESTAMP");
	xmlArr.pop();
	var shipLocale;
	if(xmlArr.length > 1){
		var chkdPts=[];
		for(var x=0;x<xmlArr.length;x++){
			xmlArr[x]=[ 1*xmlArr[x].substring( xmlArr[x].indexOf("LON")+5, xmlArr[x].indexOf("LAT")-2), 1*xmlArr[x].substring(xmlArr[x].indexOf("LAT")+5, xmlArr[x].indexOf("SPEED")-2) ];
			if((xmlArr[x][1] < 32)&&(xmlArr[x][1] > 24)){
				chkdPts.push(new OpenLayers.Geometry.Point( xmlArr[x][0], xmlArr[x][1]).transform(map.displayProjection,  map.projection));
			}
		}
		var lineFeature = new OpenLayers.Feature.Vector(new OpenLayers.Geometry.LineString(chkdPts),null,style_green);
		ship_features.push(lineFeature);
		shipLocale = new OpenLayers.Feature.Vector( chkdPts[0] ,null,style_blue);
	}
	else if(xmlArr.length == 1){
		xmlArr[0]=[ 1*xmlArr[0].substring( xmlArr[0].indexOf("LON")+5, xmlArr[0].indexOf("LAT")-2), 1*xmlArr[0].substring(xmlArr[0].indexOf("LAT")+5, xmlArr[0].indexOf("SPEED")-2) ];
		xmlArr[0]= new OpenLayers.Geometry.Point( xmlArr[0][0], xmlArr[0][1]).transform(map.displayProjection,  map.projection);
		shipLocale = new OpenLayers.Feature.Vector( xmlArr[0] ,null,style_blue);
	}
	else{return;}
	shipLocale.attributes={name:"<h4>"+name+"-" + call + "</h4><img src='"+photo+"' style='max-width:300px;max-height:300px;'/>"};
	ship_features.push(shipLocale);
}

/*regularly update reports layer to make sure boats are on the map*/

function populateReportLayer(){
	var reportLayer;
	for(var lyr=0;lyr<map.layers.length;lyr++){
		if(map.layers[lyr].name.indexOf("eports")!=-1){
			reportLayer=map.layers[lyr];
			if(reportLayer.id != lastLyrId){
				reportLayer.addFeatures(ship_features);
				lastLyrId=reportLayer.id;
			}
			return reportLayer.id;
		}
	}
}
void(0);
/* javascript:var s=document.createElement("script");s.src="http://mapmeld.appspot.com/bookmarklet-boats.js";document.body.appendChild(s);void(0); */