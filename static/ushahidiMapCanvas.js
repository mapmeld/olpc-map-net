var GMapCanvas2={
	initialize: function(prefLat, prefLng, prefZoom, prefType)
	{	this.map = document.getElementById("map");
		this.center = new google.maps.LatLng(prefLat,prefLng);
		this.zoom=prefZoom;
		this.resolution="480x303";
		this.factor=0.75;
		switch(prefType){
			case "terrain":
				this.mapType = "terrain";break;
			case "sat":
				this.mapType = "satellite";break;
			case "terr":
				this.mapType = "hybrid";break;
			case "hyb":
				this.mapType = "hybrid";break;
			case "osm":
				this.mapType = "osm";break;
			default:
				this.mapType = "roadmap";break;
		}
		document.getElementById(this.mapType).className="selectmaptype";
		this.markerList=[];
		this.lineColor="ff0000";
		this.updateImg();
		return this;
	},
	get_center:function(){return this.center;},
	get_zoom:function(){return this.zoom;},
	get_type:function(){return this.mapType;},
	get_bounds:function(){
		var sw=new google.maps.LatLng(1*this.center.lat()-0.55618*this.factor*Math.pow(2,(9-1*this.zoom)),this.center.lng()*1 - 0.98877*this.factor*Math.pow(2,(9-1*this.zoom)));
		var ne=new google.maps.LatLng(1*this.center.lat()+0.55618*this.factor*Math.pow(2,(9-1*this.zoom)),this.center.lng()*1 + 0.98877*this.factor*Math.pow(2,(9-1*this.zoom)));
		return new google.maps.LatLngBounds(sw,ne);
	},
	set_center:function(latlng){
		if(latlng.lat()>85){latlng=new google.maps.LatLng(85,latlng.lng())}
		if(latlng.lat()<-85){latlng=new google.maps.LatLng(-85,latlng.lng())}
		this.center = latlng;
		this.updateImg();
		updateLoc()
	},
	set_zoom:function(z){this.zoom = z;this.updateImg();},
	set_type:function(type){
		if(type==this.mapType){return;}
		try{document.getElementById(this.mapType).className = "maptype";document.getElementById(type).className = "selectmaptype";}
		catch(e){}
		this.mapType=type;
		this.updateImg();
	},
	fitBounds:function(bounds){
		this.bounds=bounds;
		this.center=bounds.getCenter();
		var latDiff=bounds.toSpan().lat();
		var lngDiff=bounds.toSpan().lng();
		if(latDiff/lngDiff>0.628){this.zoom=Math.floor(10-Math.log(latDiff/0.556)/0.301);}
		else{this.zoom=Math.floor(10-Math.log(lngDiff/0.8789)/0.301);}
		this.zoom=Math.min(Math.max(this.zoom,3),15);
		this.updateImg();
	},
	setLineLayer:function(data){
		if((this.lineLayer)&&(mapData)){this.lineLayer+="&path=color:0x"+this.lineColor+"|weight:5|"+data;}
		else{this.lineLayer = data;}
	},
	setLineColor:function(color){this.lineColor = color;},
	setResolution:function(res){this.resolution = res;},
	updateImg:function(){
		params=[];
		if(this.mapType!="osm"){
			params.push("center="+this.center.lat()+","+this.center.lng());
			params.push("zoom="+this.zoom);
			params.push("maptype="+this.mapType);
			if(this.markerList.length>0){
				var lls="";
				var bounds=this.get_bounds();
				for(var m=0;m<this.markerList.length;m++){
					var mar=this.markerList[m];
					if(mar.icon=="null"){lls +="|"+ mar.getLatLng().lat()+","+mar.getLatLng().lng();}
					else{
						if(!mar.iconDiv){
							mar.iconDiv=document.createElement("img");
							mar.iconDiv.src=mar.icon;
							var px=pixel(mar.pt,bounds);
							mar.iconDiv.style.left=parseInt(px[0]-mar.iconDiv.width/2)+"px";
							mar.iconDiv.style.top=parseInt(px[1]-mar.iconDiv.height/2)+"px";
							mar.iconDiv.style.position="absolute";
							mar.iconDiv.style.display="block";
							mar.iconDiv.onclick=function(event){mID=mar.markerId;isMedia=false;showInfo(mar.get_info());}
							document.body.appendChild(mar.iconDiv);
						}
						if(bounds.contains(mar.pt)){
							mar.iconDiv.style.display="block";
							var px=pixel(mar.pt,bounds);
							mar.iconDiv.style.left=parseInt(px[0]-mar.iconDiv.width/2)+"px";
							mar.iconDiv.style.top=parseInt(px[1]-mar.iconDiv.height/2)+"px";
						}
						else{ mar.iconDiv.style.display="none" }
					}
				}
				if(lls!=""){params.push("markers=size:mid" + lls);}
			}
			if(this.lineLayer){params.push("path=color:0x" + this.lineColor + "|weight:5|" + this.lineLayer);}
			if((this.mapType=="roadmap")||(this.mapType=="satellite")){params.push("mobile=true");}
			this.map.src="http://maps.google.com/maps/api/staticmap?sensor=false&size=" + this.resolution + "&format=jpg&" + params.join("&");
		}else{
			params.push("center="+this.center.lng()+","+this.center.lat());
			params.push("zoom="+this.zoom);
			var lls="";
			var bounds=this.get_bounds();
			for(var m=0;m<this.markerList.length;m++){
				var mar=this.markerList[m];
				if(mar.icon=="null"){lls +=mar.getLatLng().lng()+","+mar.getLatLng().lat()+";"}
				else{
					if(!mar.iconDiv){
						mar.iconDiv=document.createElement("img");
						mar.iconDiv.src=mar.icon;
						var px=pixel(mar.pt,bounds);
						mar.iconDiv.style.left=parseInt(px[0]-mar.iconDiv.width/2)+"px";
						mar.iconDiv.style.top=parseInt(px[1]-mar.iconDiv.height/2)+"px";
						mar.iconDiv.style.position="absolute";
						mar.iconDiv.style.display="block";
						mar.iconDiv.onclick=function(event){mID=mar.markerId;isMedia=false;showInfo(mar.get_info());}
						document.body.appendChild(mar.iconDiv)
					}
					if(bounds.contains(mar.pt)){
						mar.iconDiv.style.display="block";
						var px=pixel(mar.pt,bounds);
						mar.iconDiv.style.left=parseInt(px[0]-mar.iconDiv.width/2)+"px";
						mar.iconDiv.style.top=parseInt(px[1]-mar.iconDiv.height/2)+"px"
					}
					else{ mar.iconDiv.style.display="none"}
				}
			}
			if(lls!=""){params.push("points="+lls)}
			if(this.lineLayer){
				var linefill=[];
				var linebunch=this.lineLayer.split("|");
				for(var p=0;p<linebunch.length;p++){if(linebunch[p].indexOf(",")!=-1){linefill.push(linebunch[p].split(",")[1] + "," + linebunch[p].split(",")[0])}}
				if(this.lineLayer.indexOf("fill")>-1){params.push("polygons="+linefill.join(",")+",thickness:5,transparency:50")}
				else{params.push("paths="+linefill.join(",")+",thickness:5,transparency:50")}
			}
			this.map.src="http://dev.openstreetmap.org/~pafciu17/?module=map&width=480&height=303&imgType=jpg&"+params.join("&");
		}
	}
}