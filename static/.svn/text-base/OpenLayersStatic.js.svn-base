/*OpenLayers.Layer.Google=OpenLayers.Class(
	OpenLayers.Layer.EventPane,
	OpenLayers.Layer.FixedZoomLevels,
	{
		MIN_ZOOM_LEVEL:0,
		MAX_ZOOM_LEVEL:21,
		RESOLUTIONS:[1.40625,0.703125,0.3515625,0.17578125,0.087890625,0.0439453125,0.02197265625,0.010986328125,0.0054931640625,0.00274658203125,0.001373291015625,0.0006866455078125,0.00034332275390625,0.000171661376953125,0.0000858306884765625,0.00004291534423828125,0.00002145767211914062,0.00001072883605957031,0.00000536441802978515,0.00000268220901489257,0.0000013411045074462891,0.00000067055225372314453],
		type:null,
		wrapDateLine:true,
		sphericalMercator:false,
		version:null,
		initialize:function(name,options){
			options=options||{};
			if(!options.version){
				options.version=typeof GMap2==="function"?"2":"3";
			}
			var mixin=OpenLayers.Layer.Google["v"+options.version.replace(/\./g,"_")];
			if(mixin){
				OpenLayers.Util.applyDefaults(options,mixin);
			}
			else{
				throw"Unsupported Google Maps API version: "+options.version;
			}
			OpenLayers.Util.applyDefaults(options,mixin.DEFAULTS);
			if(options.maxExtent){
				options.maxExtent=options.maxExtent.clone();
			}
			OpenLayers.Layer.EventPane.prototype.initialize.apply(this,[name,options]);
			OpenLayers.Layer.FixedZoomLevels.prototype.initialize.apply(this,[name,options]);
			if(this.sphericalMercator){
				OpenLayers.Util.extend(this,OpenLayers.Layer.SphericalMercator);
				this.initMercatorParameters();
			}
		},		
		clone:function(){
			return new OpenLayers.Layer.Google(this.name,this.getOptions());
		},
		setVisibility:function(visible){
			var opacity=this.opacity==null?1:this.opacity;
			OpenLayers.Layer.EventPane.prototype.setVisibility.apply(this,arguments);
			this.setOpacity(opacity);
		},
		display:function(visible){
			if(!this._dragging){
				this.setGMapVisibility(visible);
			}
			OpenLayers.Layer.EventPane.prototype.display.apply(this,arguments);
		},
		moveTo:function(bounds,zoomChanged,dragging){
			this._dragging=dragging;
			OpenLayers.Layer.EventPane.prototype.moveTo.apply(this,arguments);
			delete this._dragging;
		},
		setOpacity:function(opacity){
			if(opacity!==this.opacity){
				if(this.map!=null){
					this.map.events.triggerEvent("changelayer",{layer:this,property:"opacity"});
				}
				this.opacity=opacity;
			}
			if(this.getVisibility()){
				var container=this.getMapContainer();
				OpenLayers.Util.modifyDOMElement(container,null,null,null,null,null,null,opacity);
			}
		},
		destroy:function(){
			if(this.map){
				this.setGMapVisibility(false);
				var cache=OpenLayers.Layer.Google.cache[this.map.id];
				if(cache&&cache.count<=1){
					this.removeGMapElements();
				}
			}
			OpenLayers.Layer.EventPane.prototype.destroy.apply(this,arguments);
		},
		removeGMapElements:function(){
			var cache=OpenLayers.Layer.Google.cache[this.map.id];
			if(cache){
				var container=this.mapObject&&this.getMapContainer();
				if(container&&container.parentNode){
					container.parentNode.removeChild(container);
				}
				var termsOfUse=cache.termsOfUse;
				if(termsOfUse&&termsOfUse.parentNode){
					termsOfUse.parentNode.removeChild(termsOfUse);
				}
				var poweredBy=cache.poweredBy;
				if(poweredBy&&poweredBy.parentNode){
					poweredBy.parentNode.removeChild(poweredBy);
				}
			}
		},
		removeMap:function(map){
			if(this.visibility&&this.mapObject){
				this.setGMapVisibility(false);
			}
			var cache=OpenLayers.Layer.Google.cache[map.id];
			if(cache){
				if(cache.count<=1){
					this.removeGMapElements();
					delete OpenLayers.Layer.Google.cache[map.id];
				}
				else{
					--cache.count;
				}
			}
			delete this.termsOfUse;
			delete this.poweredBy;
			delete this.mapObject;
			delete this.dragObject;
			OpenLayers.Layer.EventPane.prototype.removeMap.apply(this,arguments);
		},
		getOLBoundsFromMapObjectBounds:function(moBounds){
			var olBounds=null;
			if(moBounds!=null){
				var sw=moBounds.getSouthWest();
				var ne=moBounds.getNorthEast();
				if(this.sphericalMercator){
					sw=this.forwardMercator(sw.lng(),sw.lat());
					ne=this.forwardMercator(ne.lng(),ne.lat());
				}
				else{
					sw=new OpenLayers.LonLat(sw.lng(),sw.lat());
					ne=new OpenLayers.LonLat(ne.lng(),ne.lat());
				}
				olBounds=new OpenLayers.Bounds(sw.lon,sw.lat,ne.lon,ne.lat);
			}
			return olBounds;
		},
		getWarningHTML:function(){
			return OpenLayers.i18n("googleWarning");
		},
		getMapObjectCenter:function(){
			return this.mapObject.getCenter();
		},
		getMapObjectZoom:function(){
			return this.mapObject.getZoom();
		},
		getLongitudeFromMapObjectLonLat:function(moLonLat){
			return this.sphericalMercator?this.forwardMercator(moLonLat.lng(),moLonLat.lat()).lon:moLonLat.lng();
		},
		getLatitudeFromMapObjectLonLat:function(moLonLat){
			var lat=this.sphericalMercator?this.forwardMercator(moLonLat.lng(),moLonLat.lat()).lat:moLonLat.lat();
			return lat;
		},
		getXFromMapObjectPixel:function(moPixel){
			return moPixel.x;
		},
		getYFromMapObjectPixel:function(moPixel){
			return moPixel.y;
		},
		CLASS_NAME:"OpenLayers.Layer.Google"
	}
);
OpenLayers.Layer.GoogleStatic.cache={};
	OpenLayers.Layer.GoogleStatic.v2={
		termsOfUse:null,
		poweredBy:null,
		dragObject:null,
		loadMapObject:function(){
			if(!this.type){
				this.type=G_NORMAL_MAP;
			}
			var mapObject,termsOfUse,poweredBy;
			var cache=OpenLayers.Layer.Google.cache[this.map.id];
			if(cache){
				mapObject=cache.mapObject;
				termsOfUse=cache.termsOfUse;
				poweredBy=cache.poweredBy;
				++cache.count;
			}
			else{
				var container=this.map.viewPortDiv;
				var div=document.createElement("div");
				div.id=this.map.id+"_GMap2Container";
				div.style.position="absolute";
				div.style.width="100%";
				div.style.height="100%";
				container.appendChild(div);
				try{
					mapObject=new GMap2(div);
					termsOfUse=div.lastChild;
					container.appendChild(termsOfUse);
					termsOfUse.style.zIndex="1100";
					termsOfUse.style.right="";
					termsOfUse.style.bottom="";
					termsOfUse.className="olLayerGoogleCopyright";
					poweredBy=div.lastChild;
					container.appendChild(poweredBy);
					poweredBy.style.zIndex="1100";
					poweredBy.style.right="";
					poweredBy.style.bottom="";
					poweredBy.className="olLayerGooglePoweredBy gmnoprint";
				}
				catch(e){
					throw(e);
				}
				OpenLayers.Layer.Google.cache[this.map.id]={
					mapObject:mapObject,
					termsOfUse:termsOfUse,
					poweredBy:poweredBy,
					count:1
				};
			}
			this.mapObject=mapObject;
			this.termsOfUse=termsOfUse;
			this.poweredBy=poweredBy;
			if(OpenLayers.Util.indexOf(this.mapObject.getMapTypes(),this.type)===-1){
				this.mapObject.addMapType(this.type);
			}
			if(typeof mapObject.getDragObject=="function"){
				this.dragObject=mapObject.getDragObject();
			}
			else{
				this.dragPanMapObject=null;
			}
			if(this.isBaseLayer===false){
				this.setGMapVisibility(this.div.style.display!=="none");
			}
		},
		onMapResize:function(){
			if(this.visibility&&this.mapObject.isLoaded()){
				this.mapObject.checkResize();
			}
			else{
				if(!this._resized){
					var layer=this;
					var handle=GEvent.addListener(this.mapObject,"load",function(){
						GEvent.removeListener(handle);
						delete layer._resized;layer.mapObject.checkResize();
						layer.moveTo(layer.map.getCenter(),layer.map.getZoom());
					});
				}
				this._resized=true;
			}
		},
		setGMapVisibility:function(visible){
			var cache=OpenLayers.Layer.Google.cache[this.map.id];
			if(cache){
				var container=this.mapObject.getContainer();
				if(visible===true){
					this.mapObject.setMapType(this.type);
					container.style.display="";
					this.termsOfUse.style.left="";
					this.termsOfUse.style.display="";
					this.poweredBy.style.display="";
					cache.displayed=this.id;
				}
				else{
					if(cache.displayed===this.id){
						delete cache.displayed;
					}
					if(!cache.displayed){
						container.style.display="none";
						this.termsOfUse.style.display="none";
						this.termsOfUse.style.left="-9999px";
						this.poweredBy.style.display="none";
					}
				}
			}
		},
		getMapContainer:function(){
			return this.mapObject.getContainer();
		},
		getMapObjectBoundsFromOLBounds:function(olBounds){
			var moBounds=null;
			if(olBounds!=null){
				var sw=this.sphericalMercator?this.inverseMercator(olBounds.bottom,olBounds.left):new OpenLayers.LonLat(olBounds.bottom,olBounds.left);
				var ne=this.sphericalMercator?this.inverseMercator(olBounds.top,olBounds.right):new OpenLayers.LonLat(olBounds.top,olBounds.right);
				moBounds=new GLatLngBounds(new GLatLng(sw.lat,sw.lon),new GLatLng(ne.lat,ne.lon));
			}
			return moBounds;
		},
		setMapObjectCenter:function(center,zoom){
			this.mapObject.setCenter(center,zoom);
		},
		dragPanMapObject:function(dX,dY){
			this.dragObject.moveBy(new GSize(-dX,dY));
		},
		getMapObjectLonLatFromMapObjectPixel:function(moPixel){
			return this.mapObject.fromContainerPixelToLatLng(moPixel);
		},
		getMapObjectPixelFromMapObjectLonLat:function(moLonLat){
			return this.mapObject.fromLatLngToContainerPixel(moLonLat);
		},
		getMapObjectZoomFromMapObjectBounds:function(moBounds){
			return this.mapObject.getBoundsZoomLevel(moBounds);
		},
		getMapObjectLonLatFromLonLat:function(lon,lat){
			var gLatLng;
			if(this.sphericalMercator){
				var lonlat=this.inverseMercator(lon,lat);
				gLatLng=new GLatLng(lonlat.lat,lonlat.lon);
			}
			else{
				gLatLng=new GLatLng(lat,lon);
			}
			return gLatLng;
		},
		getMapObjectPixelFromXY:function(x,y){
			return new GPoint(x,y);
		}
	};*/
	
	version = 3;
OpenLayers.Layer.Google={
	DEFAULTS:{
		maxExtent:new OpenLayers.Bounds(-128*156543.0339,-128*156543.0339,128*156543.0339,128*156543.0339),
		sphericalMercator:true,
		maxResolution:156543.0339,
		units:"m",
		projection:"EPSG:900913"
	},
	loadMapObject:function(){
		if(!this.type){
			this.type="roadmap";
		}
		var mapObject;
		var cache=OpenLayers.Layer.Google.cache[this.map.id];
		if(cache){
			mapObject=cache.mapObject;
			++cache.count;
		}
		else{
			var container=this.map.viewPortDiv;
			var div=document.createElement("div");
			div.id=this.map.id+"_GMapContainer";
			div.style.position="absolute";
			div.style.width="100%";
			div.style.height="100%";
			container.appendChild(div);
			var center=this.map.getCenter();
			mapObject={
				div:div,
				center:center?center.lat+","+center.lon:"0,0",
				zoom:this.map.getZoom()||0,
				mapTypeId:this.type
			});
			var img = document.createElement("img");
			img.id=this.map.id+"_staticmap";
			img.src="http://maps.google.com/maps/api/staticmap?center=" + center.lat + "," + center.lon + "&zoom=" + this.map.getZoom() + "&maptype=" + this.type + "&sensor=false&ize=512x512';
			img.height='512';
			img.width='512';
			div.appendChild(img);
			
			cache={
				mapObject:mapObject,
				count:1
			};
			OpenLayers.Layer.Google.cache[this.map.id]=cache;
			//this.repositionListener=google.maps.event.addListenerOnce(mapObject,"center_changed",OpenLayers.Function.bind(this.repositionMapElements,this));
		}
		this.mapObject=mapObject;
		this.setGMapVisibility(this.visibility);
	},
	repositionMapElements:function(){
		//google.maps.event.trigger(this.mapObject,"resize");
		var div=this.mapObject.getDiv().firstChild;
		if(!div||div.childNodes.length<3){
			this.repositionTimer=window.setTimeout(OpenLayers.Function.bind(this.repositionMapElements,this),250);
			return false;
		}
		var cache=OpenLayers.Layer.Google.cache[this.map.id];
		var container=this.map.viewPortDiv;
		var termsOfUse=div.lastChild;
		container.appendChild(termsOfUse);
		termsOfUse.style.zIndex="1100";
		termsOfUse.style.bottom="";
		termsOfUse.className="olLayerGoogleCopyright olLayerGoogleV3";
		termsOfUse.style.display="";
		cache.termsOfUse=termsOfUse;
		var poweredBy=div.lastChild;
		container.appendChild(poweredBy);
		poweredBy.style.zIndex="1100";
		poweredBy.style.bottom="";
		poweredBy.className="olLayerGooglePoweredBy olLayerGoogleV3 gmnoprint";
		poweredBy.style.display="";
		cache.poweredBy=poweredBy;
		this.setGMapVisibility(this.visibility);
	},
	onMapResize:function(){
		if(this.visibility){
			//google.maps.event.trigger(this.mapObject,"resize");
		}
		else{
			if(!this._resized){
				var layer=this;
				//google.maps.event.addListenerOnce(this.mapObject,"tilesloaded",function(){
				//	delete layer._resized;
				//	google.maps.event.trigger(layer.mapObject,"resize");
				//	layer.moveTo(layer.map.getCenter(),layer.map.getZoom());
				//});
			}
			this._resized=true;
		}
	},
	setGMapVisibility:function(visible){
		var cache=OpenLayers.Layer.Google.cache[this.map.id];
		if(cache){
			var type=this.type;
			var layers=this.map.layers;
			var layer;
			for(var i=layers.length-1;i>=0;--i){
				layer=layers[i];
				if(layer instanceof OpenLayers.Layer.Google&&layer.visibility===true&&layer.inRange===true){
					type=layer.type;
					visible=true;
					break;
				}
			}
			var container=this.mapObject.getDiv();
			if(visible===true){
				this.mapObject.setMapTypeId(type);
				container.style.left="";
				if(cache.termsOfUse&&cache.termsOfUse.style){
					cache.termsOfUse.style.left="";
					cache.termsOfUse.style.display="";
					cache.poweredBy.style.display="";
				}
				cache.displayed=this.id;
			}
			else{
				delete cache.displayed;
				container.style.left="-9999px";
				if(cache.termsOfUse&&cache.termsOfUse.style){
					cache.termsOfUse.style.display="none";
					cache.termsOfUse.style.left="-9999px";
					cache.poweredBy.style.display="none";
				}
			}
		}
	},
	getMapContainer:function(){
		return this.mapObject.getDiv();
	},
	getMapObjectBoundsFromOLBounds:function(olBounds){
		var moBounds=null;
		if(olBounds!=null){
			var sw=this.sphericalMercator?this.inverseMercator(olBounds.bottom,olBounds.left):new OpenLayers.LonLat(olBounds.bottom,olBounds.left);
			var ne=this.sphericalMercator?this.inverseMercator(olBounds.top,olBounds.right):new OpenLayers.LonLat(olBounds.top,olBounds.right);
			moBounds=new google.maps.LatLngBounds(new google.maps.LatLng(sw.lat,sw.lon),new google.maps.LatLng(ne.lat,ne.lon));
		}
		return moBounds;
	},
	getMapObjectLonLatFromMapObjectPixel:function(moPixel){
		var size=this.map.getSize();
		var lon=this.getLongitudeFromMapObjectLonLat(this.mapObject.center);
		var lat=this.getLatitudeFromMapObjectLonLat(this.mapObject.center);
		var res=this.map.getResolution();
		var delta_x=moPixel.x-(size.w/2);
		var delta_y=moPixel.y-(size.h/2);
		var lonlat=new OpenLayers.LonLat(lon+delta_x*res,lat-delta_y*res);
		if(this.wrapDateLine){
			lonlat=lonlat.wrapDateLine(this.maxExtent);
		}
		return this.getMapObjectLonLatFromLonLat(lonlat.lon,lonlat.lat);
	},
	getMapObjectPixelFromMapObjectLonLat:function(moLonLat){
		var lon=this.getLongitudeFromMapObjectLonLat(moLonLat);
		var lat=this.getLatitudeFromMapObjectLonLat(moLonLat);
		var res=this.map.getResolution();
		var extent=this.map.getExtent();
		var px=new OpenLayers.Pixel((1/res*(lon-extent.left)),(1/res*(extent.top-lat)));
		return this.getMapObjectPixelFromXY(px.x,px.y);
	},
	setMapObjectCenter:function(center,zoom){
		document.getElementById(this.map.id + "_staticmap").src = "http://maps.google.com/maps/api/staticmap?center=" + center.lat + "," + center.lon + "&zoom=" + zoom + "&maptype=" + this.type + "&sensor=false&ize=512x512";
	},
	getMapObjectZoomFromMapObjectBounds:function(moBounds){
		return this.mapObject.getBoundsZoomLevel(moBounds);
	},
	getMapObjectLonLatFromLonLat:function(lon,lat){
		var gLatLng;
		if(this.sphericalMercator){
			var lonlat=this.inverseMercator(lon,lat);
			gLatLng=new google.maps.LatLng(lonlat.lat,lonlat.lon);
		}
		else{
			gLatLng=new google.maps.LatLng(lat,lon);
		}
		return gLatLng;
	},
	getMapObjectPixelFromXY:function(x,y){
		return new google.maps.Point(x,y);
	},
	destroy:function(){
		if(this.repositionListener){
			google.maps.event.removeListener(this.repositionListener);
		}
		if(this.repositionTimer){
			window.clearTimeout(this.repositionTimer);
		}
		OpenLayers.Layer.Google.prototype.destroy.apply(this,arguments);
	}
};