var map,geocoder,lastButton,lastWinItem,infoWindow,reports,points,layers,people,wildlife,timePoints,selectedItem,openReport,namedPlaces;
function init(){
	var myLatlng = new google.maps.LatLng(28.960089,-87.055664);
	var myOptions = {
		zoom: 7,
		center: myLatlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		scaleControl: true
	}
	map = new google.maps.Map($("mapdiv"), myOptions);
	map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push($("upperlay"));
	infoWindow = new google.maps.InfoWindow();
	google.maps.event.addListener(map,'click',function(){
		infoWindow.close();
	});
	//if(!MainProject.isNew){
		layers=MainProject.layers;
		people=MainProject.people;
		wildlife=MainProject.wildlife;
		timePoints=MainProject.timePoints;
		reports=MainProject.reports;
	/*}
	else{
		layers=[];
		people=[];
		wildlife=[];
		timePoints=[];
		reports=[];
	}*/
	selectedItem=0;
	for(var l=0;l<layers.length;l++){
		if((layers[l].kml)&&(layers[l].isOn)){
			var kml = new google.maps.KmlLayer('http://sites.google.com/site/gulfoilspillrecoverydata/projects_and_impacts.kml',{map:map,preserveViewport:true,suppressInfoWindows:true});
			google.maps.event.addListener(kml,'click',function(kmlEvent){
				var myLayer;
				for(var lyr=0;lyr<layers.length;lyr++){
					if(layers[lyr].kml == kml){
						myLayer=layers[lyr];
						break;
					}
				}
				openReport={content:kmlEvent.featureData.infoWindowHtml,latlng:[kmlEvent.latLng.lat(),kmlEvent.latLng.lng()],layer:myLayer.name,placeInfo:null};
				infoWindow.setPosition(kmlEvent.latLng);
				var winPrint="<div class='upperlayMenu'><div id='gItem0' class='gItemSelect' onclick='selectWinItem(0);'>Report</div><div id='gItem1' class='gItem' onclick='selectWinItem(1);'>Point</div><div id='gItem2' class='gItem' onclick='selectWinItem(2);'>Layer</div></div>";
				winPrint+="<div class='upperlayContent' id='infoContent'>" + openReport.content + "</div>";
				infoWindow.setContent(winPrint);
				lastWinItem=0;
				infoWindow.open(map);
			});
			layers[l].kml=kml;
		}
	}
	for(var r=0;r<reports.length;r++){
		report=reports[r];
		if(report.layer.indexOf("person:") == 0){
			var person=report.layer.split(":")[1];
			for(var p=0;p<people.length;p++){
				if(people[p].name==person){
					person=people[p];
					break;
				}
			}
			if(person.isOn){
				mapReport(report);
			}
		}
	}
	geocoder = new google.maps.Geocoder();
	namedPlaces=new Object;
}
function mapReport(rep){
	var marker = new google.maps.Marker({
		position:new google.maps.LatLng(rep.latlng[0],rep.latlng[1]), 
		map:map,
		title:rep.layer.split(":")[1]
	});
	google.maps.event.addListener(marker,'click',function(){
		showInfo(rep);
	});
	rep.marker=marker;
}
function showInfo(report){
	openReport=report;
	infoWindow.setPosition(new google.maps.LatLng(report.latlng[0],report.latlng[1]));
	var winPrint="<div class='upperlayMenu' style='width:100px;height:100%;'><div id='gItem0' class='gItemSelect' onclick='selectWinItem(0);'>Report</div><div id='gItem1' class='gItem' onclick='selectWinItem(1);'>Point</div><div id='gItem2' class='mItem' onclick='selectWinItem(2);'>Layer</div></div>";
	winPrint+="<div class='upperlayContent' id='infoContent' style='font-size:10pt;width:400px;'>" + report.content + "</div>";
	infoWindow.setContent(winPrint);
	lastWinItem=0;
	infoWindow.open(map);
}
function fetchSpatialData(point){
	spData = "<h3>Latitude and Longitude</h3>" + point[0].toFixed(6) + "," + point[1].toFixed(6) + "<br/><br/>";
	var nearestDistance = 250000;
	var nearestName = null;
	for(var r=0;r<reports.length;r++){
		if(reports[r].placeInfo){
			if(reports[r].latlng != openReport.latlng){
				var rdist = calcdistance(point[0],point[1],reports[r].latlng[0],reports[r].latlng[1]);
				if(rdist < nearestDistance){
					nearestName = reports[r].placeInfo;
					nearestDistance = rdist;
				}
			}
		}
	}
	for(myll in namedPlaces){
		var llsplit = myll.split(",");
		if(llsplit != openReport.latlng){
			var rdist = calcdistance(point[0],point[1],llsplit[0],llsplit[1]);
			if(rdist < nearestDistance){
				nearestName = namedPlaces[myll];
				nearestDistance = rdist;
			}
		}	
	}
	if(nearestName){
		spData += "Nearest named place -- " + nearestName + " -- is within " + nearestDistance.toFixed(1) + " km<br/>";
	}
	spData += "Distance to New Orleans: " + calcdistance(point[0],point[1],29.991813,-90.035706).toFixed(1) + " km";
	spData += "<br/>Distance to Deepwater Rig: " + calcdistance(point[0],point[1],28.738087,-88.387585).toFixed(1) + " km";
	return spData;
}
function calcdistance(lat1,lon1,lat2,lon2){
	var R = 6371; // km
	var dLat = (lat2-lat1)*Math.PI/180;
	var dLon = (lon2-lon1)*Math.PI/180;
	var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
			Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * 
			Math.sin(dLon/2) * Math.sin(dLon/2); 
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
	return R * c;
}
function selectWinItem(indexnum){
	//within the map infowindow
	if(!openReport){return;}
	$("gItem"+lastWinItem).className="gItem";
	$("gItem"+indexnum).className="gItemSelect";
	lastWinItem=indexnum;
	switch(indexnum){
		case 0:
			$("infoContent").innerHTML=openReport.content;
			break;
		case 1:
			if(openReport.placeInfo){
				$("infoContent").innerHTML=openReport.placeInfo + "<hr/>" + fetchSpatialData(openReport.latlng);
			}
			else{
				var lookup = namedPlaces[openReport.latlng[0] + "," + openReport.latlng[1]];
				if(lookup){
					$("infoContent").innerHTML=openReport.placeInfo = lookup;
					$("infoContent").innerHTML=openReport.placeInfo + "<hr/>" + fetchSpatialData(openReport.latlng);
				}
				else{
					$("infoContent").innerHTML="<span id='rgeoname'><input type='button' onclick='rgeocode(" + openReport.latlng[0] + "," + openReport.latlng[1] + ")' value='Add Placename'/></span><br/>" + fetchSpatialData(openReport.latlng);
				}
			}
			break;
		case 2:
			$("infoContent").innerHTML=openReport.layer;
			break;
	}
}
function rgeocode(geolat,geolng){
	geocoder.geocode({'latLng': new google.maps.LatLng(geolat,geolng)},function(results, status){
		if (status == google.maps.GeocoderStatus.OK) {
			if (results[1]) {
				$("rgeoname").innerHTML = results[1].formatted_address;
				openReport.placeInfo = results[1].formatted_address;
				namedPlaces[openReport.latlng[0] +','+ openReport.latlng[1]] = results[1].formatted_address;
			}
			else{
				$("rgeoname").innerHTML = "No results <input id='personalgeoname' size='30'/><input type='button' onclick='setPlacename();' value='Name'/>";
			}
		}
		else{
			$("rgeoname").innerHTML = "No results <input id='personalgeoname' size='30'/><input type='button' onclick='setPlacename();' value='Name'/>";
		}
    });
}
function setPlacename(){
	var pname = replaceAll(escape($("personalgeoname").value),"%20"," ");
	pname = replaceAll(pname,"%2C",",");
	namedPlaces[openReport.latlng[0] +','+ openReport.latlng[1]] = pname;
	openReport.placeInfo = pname;
	$("rgeoname").innerHTML = pname;
}
function selectItem(indexnum){
	//upperlay mode
	$("mItem"+selectedItem).className="mItem";
	$("mItem"+indexnum).className="mItemSelect";
	selectedItem=indexnum;
	var readItem=null;
	switch(lastButton.innerHTML){
		case "People":
			readItem=people[indexnum];
			if(readItem.isOn){
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();" checked/>Show Posts</label>';
			}
			else{
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();"/>Show Posts</layer>';
			}
			break;
		case "Wildlife":
			readItem=wildlife[indexnum];
			if(readItem.isOn){
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();" checked/>Show Stories</label>';
			}
			else{
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();"/>Show Stories</layer>';
			}
			break;
		case "Layers":
			readItem=layers[indexnum];
			if(readItem.isOn){
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();" checked/>Show Layer</label>';
			}
			else{
				readItem.extra='<label><input id="lyrbox" type="checkbox" onclick="toggleLayer();"/>Show Layer</layer>';
			}
			break;
		case "Timeline":
			readItem=timePoints[indexnum];
			readItem.extra="";
			break;
	}
	if(readItem){
		$("upperlayTitle").innerHTML=readItem.title;
		$("upperlayContent").innerHTML=readItem.content+"<hr/>"+readItem.extra;
	}
}
function toggleLayer(){
	var openLayer;
	switch(lastButton.innerHTML){
		case "People":
			openLayer = people[selectedItem];
			break;
		case "Wildlife":
			openLayer = wildlife[selectedItem];
			break;
		case "Layers":
			openLayer = layers[selectedItem];
			break;
	}
	if(openLayer){
		if(openLayer.kml){
			if(openLayer.isOn){
				openLayer.kml.setMap(null);
			}
			else{
				openLayer.kml.setMap(map);
			}
		}
		else{
			for(var r=0;r<reports.length;r++){
				if(reports[r].layer.split(":")[1]==openLayer.name){
					if(reports[r].marker){
						if(openLayer.isOn){
							reports[r].marker.setMap(null);
						}
						else{
							reports[r].marker.setMap(map);						
						}
					}
				}
			}
		}
	}
	openLayer.isOn=!openLayer.isOn;
}
function showUpperlay(uid,button){
	$("upperlay").style.display="block";
	if(lastButton){
		if(button.innerHTML==lastButton.innerHTML){closeUpperlay();return;}
		lastButton.style.backgroundColor="blue";
		lastButton.style.color="white";
	}
	selectedItem=0;
	button.style.backgroundColor="#dddddd";
	button.style.color="black";
	lastButton=button;
	var upContent="";
	var menuContent="";
	switch(uid){
		case "people":
			//list first
			for(var p=0;p<people.length;p++){
				menuContent+='<div id="mItem'+p+'" class="mItem" onclick="selectItem('+p+')">'+people[p].name+'</div>';
			}
			//content panel
			upContent+='Select a person to find out who they are, what they are doing, and how to work with their project.';
			break;
		case "wildlife":
			//list first
			for(var w=0;w<wildlife.length;w++){
				menuContent+='<div id="mItem'+w+'" class="mItem" onclick="selectItem('+w+')">'+wildlife[w].name+'</div>';
			}
			//content panel
			upContent+='In the wildlife section, selecting a topic focuses the map on a particular animal or ecosystem.';
			break;
		case "layers":
			//list first
			for(var l=0;l<layers.length;l++){
				menuContent+='<div id="mItem'+l+'" class="mItem" onclick="selectItem('+l+')">'+layers[l].name+'</div>';
			}
			//content panel
			upContent+='Mapmakers use the term "layer" to describe a collection of points you can place atop your map.<br/><br/>Add or remove layers from different sources to customize your map.';
			break;
		case "timeline":
			//list first
			for(var t=0;t<timePoints.length;t++){
				menuContent+='<div id="mItem'+t+'" class="mItem" onclick="selectItem('+t+')">'+timePoints[t].name+'</div>';
			}
			//content panel
			upContent+='Use this panel to affect the range of times you want to display on the map, and view the state of the map at certain archived times.';
			upContent+='<br/><br/>You can also click <input type="button" value="Dock Timeline" onclick="dockTimeline();"/> to fix the timeline onto the main map';
			break;
	}
	$("upperlayMenu").innerHTML=menuContent;
	$("upperlayContent").innerHTML=upContent;
	//$('mItem0').className='mItemSelect';
}
function reloadUpperlay(){
	//for people and organization Twitter ; latest blog updates ; etc
}
function closeUpperlay(){
	$("upperlay").style.display="none";
	if(lastButton){
		lastButton.style.backgroundColor="blue";
		lastButton.style.color="white";
	}
	lastButton=null;
}
function dockTimeline(){

}
function replaceAll(string,older,fixer){
	while(string.indexOf(older) != -1){
		string=string.replace(older,fixer);
	}
	return string;
}
function $(id){return document.getElementById(id);}