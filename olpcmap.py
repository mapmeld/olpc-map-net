import cgi,logging,random

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache,users,mail
from google.appengine.api.urlfetch import fetch,GET,POST
from datetime import datetime
from geomodel import GeoModel
import geotypes

class Home(webapp.RequestHandler):
	def get(self):
		url = ''
		uid = ""
		#if not facebookapi.check_connect_session(self.request):
		#	uid="no check connect"
		#else:
		#	try:
		#		uid = str(facebookapi.users.getLoggedInUser())
		#	except:
		#		uid = "could not get facebook api users"
		if(self.request.get('map') == ""):
			self.response.out.write('''<!DOCTYPE html>
<html>
<head id="head">
	<title>olpcMAP.net</title>
	<meta name="viewport" content="initial-scale=1.0,user-scalable=no" />
	<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
	<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
	<script type='text/javascript'>
var map,countries,people,orgs,infoWindow,geocoder,myPoints,specialRegion,isEditor,lastSText,approxd,clusters,defSize;
function init(){
	joinNetwork=true;
	var myOptions = {
		zoom:2,
		scaleControl:true,
		center:new google.maps.LatLng(30,-20),
		streetViewControl:false,
		mapTypeId:google.maps.MapTypeId.TERRAIN,
		mapTypeControlOptions:{mapTypeIds:[google.maps.MapTypeId.TERRAIN,google.maps.MapTypeId.ROADMAP,google.maps.MapTypeId.SATELLITE, 'OSM']}
	};
	defSize=new google.maps.Size(42,42);
	map = new google.maps.Map($("map"),myOptions);
	var osmMapLayer = new google.maps.ImageMapType({
		getTileUrl: function(coord, zoom) {
			return "http://tile.openstreetmap.org/" +
			zoom + "/" + coord.x + "/" + coord.y + ".png";
		},
		tileSize: new google.maps.Size(256, 256),
		isPng: true,
		alt: "OSM",
		name: "OSM",
		maxZoom: 19
	});
	map.mapTypes.set('OSM',osmMapLayer);

	orgs=[
		{name:"Moving Windmills",website:"http://williamkamkwamba.typepad.com",
			pts:[
				{name:"William Kamkwamba's Primary School",details:"1 XO,brought by William from TED in Arusha after telling the world about his homemade windmill.  Inspiring story.  <a href='http://williamkamkwamba.typepad.com/williamkamkwamba/2008/03/bringing-an-olp.html' target='_blank'>William's OLPC blog post</a>",pt:[-12.9829,33.6831],photo:"http://williamkamkwamba.typepad.com/williamkamkwamba/images/2008/03/21/img_0005.jpg"}
			]},
		{name:"OLPC Canada",website:"http://www.olpccanada.com",
			ajax:[
				{name:"OLPC Canada",pt:[55.786613,-98.885193],query:"/json?country=Canada",icon:new google.maps.MarkerImage("http://lib.store.yahoo.net/lib/yhst-91918294864082/canada-flag.gif",defSize)}
			],
			pts:[]},
		{name:"OLPC Australia",website:"http://www.olpc.org.au",video:"http://youtube.com/watch?v=68p4kmKilyI",
			ajax:[{name:"Sydney Center",pt:[-26.4312,121.6406],query:"/json?country=Australia"}],
			pts:[]},
		{name:"DBF OLPC India",website:"http://www.digitalbridgefoundation.org/",
			pts:[
				{name:"St. Anthony School,Dugawar,UP",details:"<a href='http://wiki.laptop.org/go/Oeuvre_des_pains' target='_blank'>School wiki page</a>",pt:[28.7168,78.5552],photo:"http://wiki.laptop.org/images/3/3c/OeuvreDesPains-Belgium-P1030833.JPG"},
				{name:"Auroville,TN",details:"<a href='http://wiki.laptop.org/go/OLPC_India/Auroville' target='_blank'>School wiki page</a>",pt:[12.0093,79.8102],photo:"http://wiki.laptop.org/images/4/44/The_Joy_of_Exploration.JPG"},
				{name:"Khairat School",pt:[18.917492,73.299408],details:"OLPC India's first pilot site<br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/Khairat_school' target='_blank'>School wiki page</a>",photo:"http://wiki.laptop.org/images/b/b8/P1060290.JPG"},
				{name:"Kikarwali",details:"India Foundation for Children Education and Care<br/><br/><a href='http://picasaweb.google.com/darshan2008/OLPCDeploymentProjectAtKikarwaliRajasthanIndiaOnMarch242010' target='_blank'>School Deployment Photos</a>",pt:[28.423199,75.60751],photo:"http://lh5.ggpht.com/_TKLjoqnmIB8/S6tmt8NyDhI/AAAAAAAAArA/6rZbCfBKDLQ/s512/DSC_0320.jpg"},
				{name:"Parikrma Center for Learning,Bangalore",details:"30 XO laptops were deployed at this center,run by the <a href='http://www.parikrmafoundation.org' target='_blank'>Parikrma Foundation</a><br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School-specific wiki page</a>",pt:[12.942348,77.585542],photo:"http://wiki.laptop.org/images/7/7b/Olpc-bangalore8.JPG"},
				{name:"Aradhna School, Bangalore",details:"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School wiki page</a>",pt:[12.885608,77.591865],photo:"http://wiki.laptop.org/images/6/66/Olpc-bangalore7.JPG"},
				{name:"Holy Mother School,Nashik",details:"<a href='http://wiki.laptop.org/go/OLPC_India/Nashik' target='_blank'>School wiki page</a>",pt:[20.00574,73.748186],photo:"http://wiki.laptop.org/images/9/9e/P1010444.jpg"},
				{name:"Mandal Parishad Primary School",details:"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Hyderabad-Mandal_Parishad_Primary_School' target='_blank'>School wiki page</a>",pt:[17.445319,78.38625],photo:"http://wiki.laptop.org/images/d/d5/DSC09954.JPG"},
				{name:"Our Lady of Merces High School",details:"wiki page under development",pt:[15.277893,73.924255]}
			]},
		{name:"OLPC Mongolia",website:"http://www.laptop.gov.mn",
			pts:[
				{name:"Alag-Erdene soum",details:"one of three schools in Khovsgol district",pt:[50.1167,100.045]},
				{name:"Khatgal soum",details:"one of three schools in Khovsgol district",pt:[50.4425,100.1603],photo:"http://farm4.static.flickr.com/3233/2915260637_f5f0375063.jpg",details:"Photo CC-BY Elana Langer"},
				{name:"21 Ulanbaatar Schools",pt:[47.920484,106.925125],photo:"http://upload.wikimedia.org/wikipedia/commons/3/37/OLPC_Class_-_Mongolia_Ulaanbaatar.JPG"},
				{name:"Khankh soum",details:"one of three schools in Khovsgol district",pt:[51.5023,100.6674]}
			]},
		{name:"OLPC Asia",website:"http://www.olpc.asia/index.html",
			pts:[
				{name:"Dujiangyan School,Sichuan",pt:[30.998285,103.619785],photo:"http://farm5.static.flickr.com/4138/4900464912_786490fed5_z.jpg",details:"Photo CC-BY OLPC"}
			]},
		{name:"Digital Literacy Project",website:"http://www.digiliteracy.org",
			pts:[
				{name:"Cambridge Friends School",details:"This XO pilot program is one of the first in the Boston area.  CFS is an independent K-8 Quaker school.  The XO is being introduced into the existing curriculum.",pt:[42.387,-71.1311],photo:"http://seeta.in/wiki/images/1/1e/DigiLit_at_CFS.JPG"},
				{name:"Mission Hill School",details:"This pilot program is DigiLit's first collaboration with the Boston Public School System.  The program is designed to help this charter school's 4th and 5th grades grow to a 1:1 laptop ratio",pt:[42.3306,-71.0993],photo:"http://seeta.in/wiki/images/3/3d/DigiLit_at_Mission_Hill.jpg"},
				{name:"Nicaragua Project",details:"In January 2010,DigiLit worked with the IADB to set up an XO laptop library at the Nicaraguan Deaf Association in Managua.  We are exploring how to close the education technology gap for these students.",pt:[12.1452,-86.2806],photo:"http://seeta.in/wiki/images/0/0d/DigiLit_in_Nicaragua_1.jpg"}
			]},
		{name:"Waveplace",website:"http://waveplace.org",
			pts:[				
				{name:"Buenos Aires,Nicaragua",
				details:"Our first pilot in Spanish,Waveplace worked with Campo Alegria to teach at arural elementary school without electricity. The government of Nicaragua was so impressed,they asked us to train 300 teachers throughout the country.<br/><a href='http://waveplace.org/locations/nicaragua' target='_blank'>Link</a>",
				pt:[11.455799,-85.759277],
				photo:"http://waveplace.com/mu/waveplace/item/tp166.jpg"},
				{name:"St. John,US Virgin Islands",
				details:"Waveplace started our journey at Guy H. Benjamin Elementary School in Coral Bay with twenty fourth graders who received the world's first 20 production XOs from OLPC. The pilot was a true learning experience for all.<br/><a href='http://waveplace.org/locations/usvi' target='_blank'>Link</a>",
				pt:[18.360798,-64.74402],
				photo:"http://waveplace.com/mu/waveplace/item/tp16.jpg"},		
				{name:"St. Vincent Pilot",
				details:"<a href='http://waveplace.com/mu/waveplace/item/tp53' target='_blank'>Link</a> - please help us add details",
				pt:[13.235935,-61.180115],
				photo:"http://waveplace.com/mu/waveplace/item/tp51.jpg"},
				{name:"Port-au-Prince,Haiti",
				details:"Our first pilot in Haiti,taught in French,Waveplace trained teachers and orphans at Mercy & Sharing Foundation's John Branchizio School in Port-au-Prince. It was here we first felt our mission have a clear effect.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>",
				pt:[18.693001,-72.353511],
				photo:"http://waveplace.com/mu/waveplace/item/tp81.jpg"},
				{name:"Petite Rivere de Nippes,Haiti",
				details:"Partnering with the American Haitian Foundation,Waveplace trained four local mentors and three from the island of Lagonav. Petite Rivere remains our longest active pilot location in Haiti,with laptop classes continuing to this day.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>",
				pt:[18.473992,-73.23349],
				photo:"http://waveplace.com/mu/waveplace/item/tp2.jpg"},
				{name:"Cambridge",
				details:"<a href='http://waveplace.com/news/blog/archive/000850.jsp' target='_blank'>Link</a> - please help us add details",
				pt:[42.371988,-71.086693],
				photo:"http://waveplace.com/images/xoPrep.jpg"}
			]},
		{name:"OLPC Papua New Guinea",website:"http://www.olpc.org.pg/",video:"http://www.youtube.com/watch?v=woS3wDpoMiU",
			pts:[
				{name:"North Wahgi",pt:[-5.684658,144.49665],details:"250 XO laptops funded by PNGSDP",photo:"http://www.olpc.org.pg/images/stories/jim_taylor_primary1.jpg"},
				{name:"Gaire",pt:[-9.676569,147.417297],details:"53 XO laptops,saturated 3rd grade class",photo:"http://wiki.laptop.org/images/d/d3/PNG-Nov08-2.jpg"},
				{name:"Dreikikir",pt:[-3.57516,142.76946],details:"Dreikikir Admin Primary School is located in East Sepik Province,near Wewak. This school is participating in the EU-funded Improvement of Rural Primary Education Facilities (IRPEF) project,based in Madang. The IRPEF is collaborating with the Department of Education and OLPC Oceania to implement the trial."}
			]},
		{name:"OLPC Alabama",website:"http://wiki.laptop.org/go/OLPC Birmingham",video:"http://youtube.com/watch?v=inxOg-dt6rw",
			pts:[
				{name:"Birmingham",pt:[33.5271,-86.8229],details:"15000 XOs deployed? <a href='http://blog.laptop.org/2010/05/21/updates-from-alabama'>Latest update</a>",photo:"http://blog.laptop.org/wp-content/uploads/2010/05/westend-camp.jpg"}
			]},
		{name:"OLPC South Carolina",website:"http://www.laptopsc.org",video:"http://youtube.com/watch?v=y3VLAUtv9Rw",
			ajax:[
				{name:"South Carolina",pt:[33.767732,-80.507812],query:"/json?state=SouthCarolina"}
			],
			pts:[
			]},
		{name:"Gureghian Family",
			pts:[
				{name:"Chester Community Charter School",pt:[39.847031,-75.357971],details:"Deployment of 1400 laptops for students grades 3-8<br/><br/><a href='http://webcache.googleusercontent.com/search?q=cache:0yNNTyovLIcJ:wiki.laptop.org/images/9/9a/CCCS_12.10.08_Final.doc+olpc+chester&cd=1&hl=en&ct=clnk&gl=us' target='_blank'>Project Page</a>"}
			]},
		{name:"Amagezi Gemaanyi Youth Association",website:"http://amagezigemaanyi.blogspot.com",
			pts:[
				{name:"Lubya Youth Education Centre",details:"Community center in Kampala; received XO laptops through Contributors Program project by USC",pt:[0.3289,32.5527],photo:"http://1.bp.blogspot.com/_3doFkXas3vs/TEy34ipYQbI/AAAAAAAABkU/XlMIvb3KrxA/S390/agya-olpc4.jpg"}
			]},
		{name:"SEETA",website:"http://wiki.sugarlabs.org/go/Sugar_on_a_Stick_in_Delhi_India",
			pts:[
				{name:"Veda Vyasa DAV School",details:"Sugar on a Stick deployment in Delhi,India<br/>Our goal is to measure student learning improvements - students have a digital portfolio of their work and achievements. We will be publishing a case study in fall 2010 with a professor in Boston University's School of Education<br/><a href='http://theteamgoestoindia.wordpress.com' target='_blank'>Blog</a>",pt:[28.6384,77.0617]}
			]},
		{name:"OLE Nepal",website:"http://www.olenepal.org",video:"",
			pts:[],
			ajax:[{name:"OLE Nepal",pt:[27.3728,85.1897],query:"/json?country=Nepal"}]},
		{name:"TecnoTzotzil",website:"http://sites.google.com/tecnotzotzil",
			pts:[
				{name:"4 San Cristobal De Las Casas Schools",details:"SoaS deployment with 44 students,using Intel Classmate PCs. Photo CC-BY Jose I. Icaza",pt:[16.7404,-92.6307],photo:"http://farm3.static.flickr.com/2600/3979066854_e9fdf5c530.jpg"}
			]},
		{name:"Educa Libre",website:"http://educalibre.cl",
			pts:[
				{name:"Florence Nightingale School",details:"SoaS deployment with 25 K-3 students in Macul,Chile. Acer netbooks and some PCs",pt:[-33.4871,-70.6048],photo:"http://educalibre.cl/wp-content/uploads/2010/07/alumno_piloto_memorice3.jpg"}
			]},
		{name:"United Action for Children",website:"http://www.unitedactionforchildren.org/",
			pts:[
				{name:"UPenn OLPCorps",details:"Students and teachers trained to use Scratch,Write,and more<br/><br/><a href='http://upennuac.blogspot.com/' target='_blank'>Blog</a>",pt:[4.061536,9.448242],photo:"http://1.bp.blogspot.com/_iSJqZVkttQc/SpM7e6-Qh_I/AAAAAAAAACc/YLR726R5GP0/s320/5848_237169645060_875880060_8375546_6766219_n%5B1%5D.jpg"}
			]},
		{name:"Ethiopia Engineering Capacity Building",website:"http://www.ecbp.biz/",
			pts:[
				{name:"OLPCorps:Dalarna U. and Royal IT",details:"<br/><br/><a href='http://wiki.laptop.org/go/OLPCorps_DKTH_ETHIO_PROPOSAL' target='_blank'>Wiki Page</a>",photo:"",pt:[7.939556,39.122314]}
			]},
		{name:"OLPCorps",
			pts:[
				{name:"OLPCorps:Harvard and MIT",pt:[-24.20689,16.167669]}
			]},
		{name:"GMin",website:"http://www.gmin.org/",
			pts:[
				{name:"OLPCorps Sahn Malen",details:"Princeton University and University of Maryland students<br/><br/><a href='http://olpcsm.blogspot.com/' target='_blank'>Wiki Page</a>",photo:"http://3.bp.blogspot.com/_I7lfwYcs8Jo/Sn871AI5K6I/AAAAAAAABpc/gzJ2XA-bed8/s400/DSC02252.JPG",pt:[8.063479,-11.42252]}
			]},
		{name:"ONE",website:"http://www.one.org",video:"http://www.youtube.com/watch?v=lPUXj7EqGWw",
			pts:[
				{name:"OLPCorps Senegal",details:"Students from U. Miami and U. Minnesota teamed up for this deployment<br/><br/><a href='http://www.one.org/blog/?p=7703' target='_blank'>Report from ONE.org</a><br/><br/><a href='http://africaxo.blogspot.com/' target='_blank'>Blog</a>",photo:"http://farm4.static.flickr.com/3500/3833004781_f0533a4c32.jpg",pt:[14.26638,-16.34697]}
			]},
		{name:"Intenge Development Foundation",website:"http://olpcorpsnamibiangoma.wordpress.com/idf-ngo-community-based-organization-in-caprivi/",
			pts:[
				{name:"OLPCorps Namibia-Ngoma",details:"<br/><br/><a href='http://olpcorpsnamibiangoma.wordpress.com/' target='_blank'>Blog</a>",pt:[-20.131298,19.510431]}
			]},
		{name:"One Here One There",website:"http://onehereonethere.org",
			pts:[
				{name:"OLPCorps IU",details:"Students from Indiana University. Installed an electric generator and ran a short student newspaper-writing project.<br/><br/><a href='http://2009iuohot.blogspot.com/' target='_blank'>Blog</a>",pt:[-24.153019,29.351349]}
			]},
		{name:"OLPCorps",
			pts:[
				{name:"OLPCorps:Niger",details:"University of Lagos,Royal Holloway University of London,and University of Salford students",pt:[8.762429,5.799923]},
				{name:"OLPCorps:Sierra Leone",details:"Tulane University and UC Davis students",pt:[8.760054,-12.572136]},
				{name:"OLPCorps:U of Education,Winneba",pt:[6.14128,-1.670179]},
				{name:"OLPCorps:U. Kinhasa",pt:[-1.710866,28.959188]},
				{name:"OLPCorps:U of Ibadan",details:"This project is targeted at empowering people with disabilities by improving their access to technology.<br/><br/><a href='http://abledisableinxo.blogspot.com' target='_blank'>Blog</a>",photo:"http://4.bp.blogspot.com/_HbCc4VF-oTw/Splp_fs_JvI/AAAAAAAAADs/xI-fu0xLxWw/s320/teaching.jpg",pt:[9.277909,10.195785]},
				{name:"OLPCorps:CUNY Baruch",pt:[8.407168,0.087891]},
				{name:"OLPCorps:Soweto",details:"Deployment with detailed updates for the Global Post<br/><br/><a href='http://oplokhii.blogspot.com' target='_blank'>Blog</a>",pt:[-26.194877,27.993164],photo:"http://3.bp.blogspot.com/_jBm2wqTTQu8/SpX-ytitHwI/AAAAAAAAAQ4/PnIoAZ7bGME/s320/IMG_9629.JPG"},
				{name:"OLPCorps:Mauritania",details:"Students from Cornell University",pt:[14.349548,-16.918945]},
				{name:"OLPCorps:Ungana Foundation",details:"Students from Utah State University supported the Ungana Foundation's effort to extend and support OLPC Rwanda<br/><br/><a href='http://unganafoundation.blogspot.com/'>Blog</a>",photo:"http://1.bp.blogspot.com/_EkMPu5bJnVU/Sqav0piu-cI/AAAAAAAAAPI/C3ZKbTbPpFA/s400/P1010406.JPG",pt:[-1.83406,29.486618]},
				{name:"OLPCorps:Heritage Nigeria",details:"Students from Texas A&M University<br/><br/><a href='http://olpcheritagenigeria.blogspot.com/' target='_blank'>Blog</a>",pt:[6.509768,3.537598],photo:"http://2.bp.blogspot.com/_ytQa4_LpsOk/SnfG0uka1-I/AAAAAAAAAFk/A5D3QoWvDkQ/s320/IMG_1478.JPG"},
				{name:"OLPCorps:Zimbabwe",details:"Students from Macalester College,Midlands State University,and University of Zimbabwe - installed solar and then national grid power<br/><br/><a href='http://olpcorpszimbabwe09.blogspot.com' target='_blank'>Blog</a>",pt:[-17.137838,31.072083]},
				{name:"OLPCorps:Madagascar",details:"Students from GWU and U Maryland<br/><br/><a href='http://ampitso.wordpress.com/' target='_blank'>Blog</a>",photo:"http://ampitso.smugmug.com/photos/638764729_UCofq-M.jpg",pt:[-13.57024,49.306641]},
				{name:"OLPCorps:Laval University",details:"<br/><br/><a href='http://collabo.fse.ulaval.ca/olpc/' target='_blank'>Website</a>",photo:"http://collabo.fse.ulaval.ca/olpc/images/teach.jpg",pt:[3.387307,12.877007]},
				{name:"OLPCorps:Tanzania",details:"Students from Tumaini University.<br/><br/>The school was connected to the internet<br/><br/><a href='http://mot-tumaini.blogspot.com/' target='_blank'>Blog</a>",photo:"http://4.bp.blogspot.com/_z6OVkOJNvTQ/SpvI0dyRxGI/AAAAAAAAAO4/ukhEnWkZXEg/s320/IMG0011A.jpg",pt:[-7.794677,35.690117]},
				{name:"OLPCorps:Vutakaka",details:"Students from U. Washington and the New School<br/><br/><a href='http://vutakakaolpc.blogspot.com/' target='_blank'>Blog</a>",photo:"http://4.bp.blogspot.com/_C_wadBS6-ek/SmX5aiSypyI/AAAAAAAAIzg/XKbSjGgYCoo/s320/100_0057.jpg",pt:[-3.513421,39.835739]},
				{name:"OLPCorps:Kampala",details:"Still operating (though not online). Supported by MIT and Wellesley College<br/><br/><a href='http://uganda-olpc.blogspot.com/' target='_blank'>Blog</a>",photo:"http://2.bp.blogspot.com/_Sm-Wjgh0ZWk/SlCq2EOvw2I/AAAAAAAAABU/Xm_8bmDF7tY/s320/olpc_kps_10.JPG",pt:[0.29663,32.640381]},
				{name:"OLPCorps:GTech",details:"Students from Grahamstown and Gettysburg <a href='http://picasaweb.google.com/aimeegeorge/PicsFromGTECHSouthAfrica?feat=email#' target='_blank'>Photos Page</a><br/><br/><a href='http://gtech-olpc.blogspot.com/' target='_blank'>Blog</a>",photo:"http://lh3.ggpht.com/_7PSu0kxiZPQ/SrrntMYgpLI/AAAAAAAABFY/41saWNP1JNw/s640/P1080072.JPG",pt:[-33.315037,26.548634]},
				{name:"OLPCorps:Kwame Nkrumah U.",pt:[7.227441,-0.747414]}
			]}
	];
	myPoints=[];\n''')
		elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
			self.response.out.write('''<!DOCTYPE html>
<html>
<head id="head">
	<title>olpcMAP - Quick Version</title>
	<meta name="viewport" content="initial-scale=1.0,user-scalable=no" />
	<script type='text/javascript'>
var map,myPoints,center,markerStuff,zoom,rad,box;
var factor=1.000000;
function p(m){myPoints.push(m)}
function load(){
	myPoints=[];\n''')
		myResults = None
		results = None
		hiddenGeoResults = None
		directGeo = 1
		mapImgUrl = None
		try:
			if(self.request.get('llcenter') != ''):
				directGeo = 0
				ctr_lat = self.request.get('llcenter').replace('%20','').split(',')[0]
				ctr_lng = self.request.get('llcenter').replace('&20','').split(',')[1]
				radius = float(self.request.get('km-distance'))
				results = GeoRefUsermadeMapPoint.proximity_fetch(
					GeoRefUsermadeMapPoint.all(),
					geotypes.Point(float(ctr_lat),float(ctr_lng)),
					max_results=100,
					max_distance=1000 * radius)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Circle({center:new google.maps.LatLng('+ cgi.escape(ctr_lat) +',' + cgi.escape(ctr_lng) + '),radius:'+str(1000*radius)+'});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&center=" + ctr_lat + "," + ctr_lng
					hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
						GeoRefMapPoint.all(),
						geotypes.Point(float(ctr_lat),float(ctr_lng)),
						max_results=100,
						max_distance=1000 * radius
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
					self.response.out.write('center=['+ ctr_lat + "," + ctr_lng + '];\nrad="'+str(radius)+'";\n')
			elif(self.request.get('llregion') != ''):
				directGeo = 0
				ne_lat = self.request.get('llregion').replace('%20','').split(',')[0]
				ne_lng = self.request.get('llregion').replace('%20','').split(',')[1]
				sw_lat = self.request.get('llregion').replace('%20','').split(',')[2]
				sw_lng = self.request.get('llregion').replace('%20','').split(',')[3]
				results = GeoRefUsermadeMapPoint.bounding_box_fetch(
					GeoRefUsermadeMapPoint.all(),
					geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
					max_results=100
				)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Rectangle({bounds:new google.maps.LatLngBounds(new google.maps.LatLng('+ cgi.escape(sw_lat) +',' + cgi.escape(sw_lng) + '),new google.maps.LatLng(' + cgi.escape(ne_lat) +',' + cgi.escape(ne_lng) + '))});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&visible=" + ne_lat + "," + ne_lng + "|" + sw_lat + "," + sw_lng
					hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
						GeoRefMapPoint.all(),
						geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
						max_results=100
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
					self.response.out.write('center=['+ str((float(ne_lat)+float(sw_lat))/2) + "," + str((float(ne_lng)+float(sw_lng))/2) + '];box="' + ne_lat +"," + ne_lng + "," + sw_lat + "," + sw_lng + '";\n')

			elif(self.request.get('llregions') != ''):
				# &llregions=llregion1|llregion2
				directGeo = 0
				llregions = self.request.get('llregions').split('|')
				minlat=90
				minlng=180
				maxlat=-90
				maxlng=-180
				for llregion in llregions:
					llregion=llregion.replace('%20','').split(',')
					ne_lat=float(llregion[0])
					if(ne_lat<minlat):
						minlat=ne_lat
					if(ne_lat>maxlat):
						maxlat=ne_lat
					ne_lng=float(llregion[1])
					if(ne_lng<minlng):
						minlng=ne_lng
					if(ne_lng>maxlng):
						maxlng=ne_lng
					sw_lat=float(llregion[2])
					if(sw_lat<minlat):
						minlat=sw_lat
					if(sw_lat>maxlat):
						maxlat=sw_lat
					sw_lng=float(llregion[3])
					if(sw_lng<minlng):
						minlng=sw_lng
					if(sw_lng>maxlng):
						maxlng=sw_lng
					if(results is None):
						results=GeoRefUsermadeMapPoint.bounding_box_fetch(
							GeoRefUsermadeMapPoint.all(),
							geotypes.Box(ne_lat,ne_lng,sw_lat,sw_lng),
							max_results=100
						)					
					else:
						results=results+GeoRefUsermadeMapPoint.bounding_box_fetch(
							GeoRefUsermadeMapPoint.all(),
							geotypes.Box(ne_lat,ne_lng,sw_lat,sw_lng),
							max_results=100
						)
					if(self.request.get('map')=='image'):
						if(hiddenGeoResults is None):
							hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
								GeoRefMapPoint.all(),
								geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
								max_results=100
							)
						else:
							hiddenGeoResults = hiddenGeoResults + GeoRefMapPoint.bounding_box_fetch(
								GeoRefMapPoint.all(),
								geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
								max_results=100
							)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Rectangle({bounds:new google.maps.LatLngBounds(new google.maps.LatLng('+ str(minlat) +',' + str(minlng) + '),new google.maps.LatLng(' + str(maxlat) +',' + str(maxlng) + '))});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&visible=" + str(maxlat) + "," + str(maxlng) + "|" + str(minlat) + "," + str(minlng)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
						self.response.out.write('center=['+ str((ne_lat+sw_lat)/2) + "," + str((ne_lng+sw_lng)/2) + '];box="' + str(maxlat) +"," + str(maxlng) + "," + str(minlat) + "," + str(minlng) + '";\n')				

			elif(self.request.get('center') != ''):
				directGeo = 0
				ctr_lat = None
				ctr_lng = None
				suggestCtr = memcache.get("center:" + cgi.escape(self.request.get('center')))
				if(suggestCtr is not None):
					# center was in memcache
					ctr_lat = suggestCtr.split(",")[0]
					ctr_lng = suggestCtr.split(",")[1]
				else:
					llcenter = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJ&q=" + self.request.get('center'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
					ctr_lat = llcenter[llcenter.find('latitude')+11:len(llcenter)]
					ctr_lat = ctr_lat[0:ctr_lat.find('"')]
					ctr_lng = llcenter[llcenter.find('longitude')+12:len(llcenter)]
					ctr_lng = ctr_lng[0:ctr_lng.find('"')]
					memcache.add("center:" + cgi.escape(self.request.get('center')),ctr_lat + "," + ctr_lng,500000)
				radius = float(self.request.get('km-distance'))
				results = GeoRefUsermadeMapPoint.proximity_fetch(
						GeoRefUsermadeMapPoint.all(),
						geotypes.Point(float(ctr_lat),float(ctr_lng)),
						max_results=100,
						max_distance=1000 * radius)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Circle({center:new google.maps.LatLng('+ cgi.escape(ctr_lat) +',' + cgi.escape(ctr_lng) + '),radius:'+str(1000*radius)+'});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&center=" + ctr_lat + "," + ctr_lng
					hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
						GeoRefMapPoint.all(),
						geotypes.Point(float(ctr_lat),float(ctr_lng)),
						max_results=100,
						max_distance=1000 * radius
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
					self.response.out.write('center=['+ ctr_lat + "," + ctr_lng + '];\nrad="'+str(radius)+'";')

			elif(self.request.get('region') != ''):
				directGeo = 0
				ne_lat=None
				ne_lng=None
				sw_lat=None
				sw_lng=None
				suggestRgn = memcache.get("region:" + cgi.escape(self.request.get('region')))
				if(suggestRgn is not None):
					# center was in memcache
					suggestRgn=suggestRgn.split(",")
					ne_lat = suggestRgn[0]
					ne_lng = suggestRgn[1]
					sw_lat = suggestRgn[2]
					sw_lng = suggestRgn[3]
				else:
					llregion = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJX&q=" + self.request.get('region'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
					ne_lat = llregion[llregion.find('north')+8:len(llregion)]
					ne_lat = ne_lat[0:ne_lat.find('"')]
					ne_lng = llregion[llregion.find('east')+7:len(llregion)]
					ne_lng = ne_lng[0:ne_lng.find('"')]
					sw_lat = llregion[llregion.find('south')+8:len(llregion)]
					sw_lat = sw_lat[0:sw_lat.find('"')]
					sw_lng = llregion[llregion.find('west')+7:len(llregion)]
					sw_lng = sw_lng[0:sw_lng.find('"')]
					memcache.add("region:" + cgi.escape(self.request.get('region')),ne_lat + "," + ne_lng + "," + sw_lat + "," + sw_lng,500000)
				results = GeoRefUsermadeMapPoint.bounding_box_fetch(
					GeoRefUsermadeMapPoint.all(),
					geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
					max_results=100
				)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Rectangle({bounds:new google.maps.LatLngBounds(new google.maps.LatLng('+ cgi.escape(sw_lat) +',' + cgi.escape(sw_lng) + '),new google.maps.LatLng(' + cgi.escape(ne_lat) +',' + cgi.escape(ne_lng) + '))});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&visible=" + ne_lat + "," + ne_lng + "|" + sw_lat + "," + sw_lng
					hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
						GeoRefMapPoint.all(),
						geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
						max_results=100
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
					self.response.out.write('center=['+ str((float(ne_lat)+float(sw_lat))/2) + "," + str((float(ne_lng)+float(sw_lng))/2) + '];\nbox="'+ne_lat+","+ne_lng+","+sw_lat+","+sw_lng+'"\n')

			elif(self.request.get('go') != ''):
				directGeo = 0
				ne_lat=None
				ne_lng=None
				sw_lat=None
				sw_lng=None
				suggestRgn = memcache.get("region:" + cgi.escape(self.request.get('go')))
				if(suggestRgn is not None):
					# center was in memcache
					suggestRgn=suggestRgn.split(",")
					ne_lat = suggestRgn[0]
					ne_lng = suggestRgn[1]
					sw_lat = suggestRgn[2]
					sw_lng = suggestRgn[3]
				else:
					llregion = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJX&q=" + self.request.get('go'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
					ne_lat = llregion[llregion.find('north')+8:len(llregion)]
					ne_lat = ne_lat[0:ne_lat.find('"')]
					ne_lng = llregion[llregion.find('east')+7:len(llregion)]
					ne_lng = ne_lng[0:ne_lng.find('"')]
					sw_lat = llregion[llregion.find('south')+8:len(llregion)]
					sw_lat = sw_lat[0:sw_lat.find('"')]
					sw_lng = llregion[llregion.find('west')+7:len(llregion)]
					sw_lng = sw_lng[0:sw_lng.find('"')]
					memcache.add("region:" + cgi.escape(self.request.get('go')),ne_lat + "," + ne_lng + "," + sw_lat + "," + sw_lng,500000)
				results = GeoRefUsermadeMapPoint.bounding_box_fetch(
					GeoRefUsermadeMapPoint.all(),
					geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
					max_results=100
				)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Rectangle({bounds:new google.maps.LatLngBounds(new google.maps.LatLng('+ cgi.escape(sw_lat) +',' + cgi.escape(sw_lng) + '),new google.maps.LatLng(' + cgi.escape(ne_lat) +',' + cgi.escape(ne_lng) + '))});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&visible=" + ne_lat + "," + ne_lng + "|" + sw_lat + "," + sw_lng
					hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
						GeoRefMapPoint.all(),
						geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
						max_results=100
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
					self.response.out.write('center=['+ str((float(ne_lat)+float(sw_lat))/2) + "," + str((float(ne_lng)+float(sw_lng))/2) + '];\nbox="'+ne_lat+","+ne_lng+","+sw_lat+","+sw_lng+'"\n')

			elif((self.request.get('km-distance') != '') and (self.request.get('id') != '')):
				directGeo = 0
				ctrPoint = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
				radius = float(self.request.get('km-distance'))
				results = GeoRefUsermadeMapPoint.proximity_fetch(
					GeoRefUsermadeMapPoint.all(),
					geotypes.Point(float(ctrPoint.location.lat),float(ctrPoint.location.lon)),
					max_results=100,
					max_distance=1000 * radius)
				if(self.request.get('map') == ''):
					self.response.out.write('	var specialRegion=new google.maps.Circle({center:new google.maps.LatLng('+ str(ctrPoint.location.lat) +',' + str(ctrPoint.location.lon) + '), radius:'+str(1000*radius)+'});\n	map.fitBounds(specialRegion.getBounds());\n')
				elif(self.request.get('map') == 'image'):
					mapImgUrl = "http://maps.google.com/maps/api/staticmap?sensor=false&maptype=terrain&center=" + str(ctrPoint.location.lat) +',' + str(ctrPoint.location.lon)
					hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
						GeoRefMapPoint.all(),
						geotypes.Point(float(ctrPoint.location.lat),float(ctrPoint.location.lon)),
						max_results=100,
						max_distance=1000 * radius
					)
				elif((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast') ):
					self.response.out.write('center=['+ str(ctrPoint.location.lat) + "," + str(ctrPoint.location.lon) + '];\nrad="' + str(radius) + '";')
		except:
			directGeo = 1

		if(directGeo == 1):
			oldPoints = memcache.get('oldPoints')
			if(oldPoints is None):
				oldr = Oldest()
				oldPoints = oldr.snap()
			newPoints = memcache.get('newPoints')
			if(newPoints is None):
				newr = Newest()
				newPoints = newr.snap()
			myResults = oldPoints + newPoints
		if myResults is not None:
			self.response.out.write(myResults)
			mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
			results = mapPoints.fetch(30)
			resultOut = u''
			for pt in results:
				resultOut = resultOut + u'pS({name:"'
				usename = cgi.escape(pt.name)
				if(usename.find("privatized") != -1):
					fixname = usename.replace("privatized:","")
					sndNames = 0
					outname = ""
					for letter in fixname:
						if(sndNames == 0):
							outname = outname + letter
						elif(sndNames == -1):
							outname = outname + letter
							sndNames = 1
						if(letter == " "):
							sndNames = -1
							outname = outname + " "
					usename = outname
				resultOut = resultOut + cgi.escape(usename).replace('"','\\"') + u'",id:"' + str(pt.key().id()) + u'",pt:[' + str(pt.location.lat) + "," + str(pt.location.lon) + u'],icon:"' + cgi.escape(pt.icon or "").replace('"','\\"') + u'",details:"'
				resultOut = resultOut + cgi.escape(pt.details or "").replace('"','\\"').replace("&lt;","<").replace("&gt;",">").replace('\\n','<br/>').replace('\\r','<br/>').replace('\n','<br/>').replace('\r','<br/>') + '"'
				if(pt.tabs is not None):
					resultOut = resultOut + u',tabs:["' + '","'.join(pt.tabs) + '"]'
				resultOut = resultOut + u',photo:"' + cgi.escape(pt.photo or "").replace('"','\\"') + u'",album:"' + cgi.escape(pt.album or "").replace('"','\\"') + u'",group:"' + cgi.escape(pt.group or "").replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + u'",icon:"' + cgi.escape(pt.icon or "") + u'"});\n'
			self.response.out.write(resultOut)
		else:
			mapPoints = None
			#mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
			if(results is None):
				mapPoints = GeoRefUsermadeMapPoint.all()
				if mapPoints is not None:
					results = mapPoints.fetch(200)
			
			if((results is not None) and (self.request.get('map') != 'image')):
				resultOut=u''
				for pt in results:
					#if(writeGeo == 1):
					#	newMP = GeoRefUsermadeMapPoint(name = pt.name,
					#	blog = pt.blog,
					#	details = pt.details,
					#	group = pt.group,
					#	photo = pt.photo,
					#	album = pt.album,
					#	icon = pt.icon,
					#	country = pt.country,
					#	region = pt.region,
					#	email = pt.email,
					#	lastUpdate = pt.lastUpdate,
					#	creator = pt.creator,
					#	location = pt.center)
					#	newMP.update_location()
					#	newMP.put()
					#	pt.delete()
					#	continue
					resultOut = resultOut + u'p({name:"'
					usename = cgi.escape(pt.name)
					if(usename.find("privatized") != -1):
						fixname = usename.replace("privatized:","")
						sndNames = 0
						outname = ""
						for letter in fixname:
							if(sndNames == 0):
								outname = outname + letter
							elif(sndNames == -1):
								outname = outname + letter
								sndNames = 1
							if(letter == " "):
								sndNames = -1
								outname = outname + " "
						usename = outname
					resultOut = resultOut + cgi.escape(usename).replace('"','\\"') + u'",id:"' + str(pt.key().id()) + u'",pt:[' + str(pt.location.lat) + "," + str(pt.location.lon) + u'],icon:"' + cgi.escape(pt.icon or "") + u'",details:"'
					resultOut = resultOut + cgi.escape(pt.details or "").replace('"','\\"').replace("&lt;","<").replace("&gt;",">").replace('\\n','<br/>').replace('\\r','<br/>').replace('\n','<br/>').replace('\r','<br/>') + '"'
					if(pt.tabs is not None):
						resultOut = resultOut + u',tabs:["' + '","'.join(pt.tabs) + '"]'
					resultOut = resultOut + u',photo:"' + cgi.escape(pt.photo or "").replace('"','\\"') + u'",album:"' + cgi.escape(pt.album or "").replace('"','\\"') + u'",group:"' + cgi.escape(pt.group or "").replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + u'",icon:"' + cgi.escape(pt.icon or "") + u'"});\n'
				self.response.out.write(resultOut)
			elif(self.request.get('map')=='image'):
				byIcon={}
				iconList=[]
				if results is not None:
					#outlat=str(pt.location.lat)
					#if(len(outlat) > 9):
						#outlat = outlat[0:9]
					#outlon=str(pt.location.lon)
					#if(len(outlon) > 9):
						#outlon = outlon[0:9]
					#mapImgUrl += "|" + outlat + "," + outlon
					for pt in results:
						ic=pt.icon.replace('https','http')
						if byIcon.has_key(ic):
							byIcon[ic].append(pt.location)
						else:
							byIcon[ic]=[pt.location]
							iconList.append(ic)
				if(hiddenGeoResults is not None):
					for pt in hiddenGeoResults:
						ic=pt.icon.replace('https','http')
						if byIcon.has_key(ic):
							byIcon[ic].append(pt.location)
						else:
							byIcon[ic]=[pt.location]
							iconList.append(ic)
				iconsum=0
				for icon in iconList:
					mapImgUrl=mapImgUrl+"&markers=icon:"+icon
					ptList = byIcon[icon]
					for latlon in ptList:
						mapImgUrl=mapImgUrl+"|"+str(latlon.lat)+","+str(latlon.lon);
						iconsum=iconsum+1
				w=self.request.get('w')
				h=self.request.get('h')
				if(w==''):
					w='500'
				if(h==''):
					h='500'
				if(self.request.get('z')!=''):
					h=h+"&zoom="+self.request.get('z')
				else:
					h=h+"&format=jpg"
				self.redirect(mapImgUrl + "&size="+w+"x"+h)
				return
		if((self.request.get('map') == 'quick') or (self.request.get('map') == 'fast')):
			self.response.out.write('''	markerStuff="";
	var byIcon={};
	var allIcons=[];
	for(var mPt=0;mPt<myPoints.length;mPt++){
		var ic=myPoints[mPt].icon.replace('https','http');
		if(byIcon[ic]!=null){
			byIcon[ic].push(mPt);
		}
		else{
			byIcon[ic]=[mPt];
			allIcons.push(ic);
		}
	}
	for(var mIc=0;mIc<allIcons.length;mIc++){
		markerStuff+="&markers=icon:"+allIcons[mIc];
		for(var mE=0;mE<byIcon[allIcons[mIc]].length;mE++){
			var outlat=myPoints[byIcon[allIcons[mIc]][mE]].pt[0].toFixed(4);
			var outlon=myPoints[byIcon[allIcons[mIc]][mE]].pt[1].toFixed(4);
			markerStuff+="|"+outlat+","+outlon;
		}
	}
	if(rad){
		var lngDiff=rad/111;
		zoom=Math.min(Math.max(Math.floor(10-Math.log(lngDiff/0.556)/0.301),3),15);
		zoom++;
	}
	else if(box){
		box=box.split(',');
		var latDiff=box[0]-box[2];
		var lngDiff=box[1]-box[3];
		if(latDiff/lngDiff>0.628){zoom=Math.floor(10-Math.log(latDiff/0.556)/0.301)}
		else{zoom=Math.floor(10-Math.log(lngDiff/0.8789)/0.301)}
		zoom=Math.min(Math.max(zoom,3),15);
		zoom++;
	}
	updateImg();
}
function zoomIn(){zoom++;updateImg()}
function zoomOut(){zoom--;updateImg()}
function clkMar(event){
	var bounds=get_bounds();
	var lowestPt=-1;
	var lowestDist=5*mapYSPAN;
	for(var m=0;m<myPoints.length;m++){
		var mark=myPoints[m];
		var pix=pixel(mark.pt,bounds);
		var pDiff=Math.pow(Math.abs(pix[0]-event.clientX+mapXOFF),2)+Math.pow(Math.abs(pix[1]-event.clientY),2);
		if(pDiff<lowestDist){
			lowestDist=pDiff;
			lowestPt=m;
		}
	}
	if(lowestPt!=-1){
		showInfo(myPoints[lowestPt]);
	}
}
function get_bounds(){
	var sw=[center[0]-0.55618*factor*Math.pow(2,(9-1*zoom)),center[1]*1-0.98877*factor*Math.pow(2,(9-1*zoom))];
	var ne=[center[0]+0.55618*factor*Math.pow(2,(9-1*zoom)),center[1]*1+0.98877*factor*Math.pow(2,(9-1*zoom))];
	return [sw,ne]
}
var mapYSPAN=500;
var mapXSPAN=400;
var mapXOFF=80;
var cCtr;
function pixel(latlng,bounds){
	var latDiff=Math.abs(latlng[0]-center[0]);
	var lngDiff=Math.abs(latlng[1]-center[1]);
	var latSpan=bounds[1][0]-bounds[0][0];
	var lngSpan=bounds[1][1]-bounds[0][1];
	if((center[1]>0)&&(latlng[1]<0)){lngDiff=latlng[1]-(center[1]-360)}
	if((latlng[1]>0)&&(center[1]<0)){lngDiff=center[1]-(latlng[1]-360)}
	var yDiff=Math.round(latDiff/latSpan*mapYSPAN/1.3);
	if(1*latlng[0]<1*center[0]){yDiff=mapYSPAN*0.500000+yDiff}
	else{yDiff=mapYSPAN*0.50000000-yDiff}
	var xDiff=Math.round(lngDiff/lngSpan*mapXSPAN/1.2);
	if(1*latlng[1]>1*center[1]){xDiff=mapXSPAN*0.500000+xDiff}
	else{xDiff=mapXSPAN*0.50000000-xDiff}
	return [xDiff,yDiff];
}
function toLatLng(x,y){
	x+=".000000";
	y+=".000000";
	var yfactor=factor*1.00;
	var mapLng=(x-mapXOFF-0.50000000*mapXSPAN)*0.00141335458*1.25*factor*Math.pow(2,(10-zoom))+1*center[1];
	var mapLat=1*center[0]-(y-0.50000000*mapYSPAN)*yfactor*0.001255065*1.25*Math.pow(2,(10-zoom));
	return [mapLat,mapLng];
}
function tab(tabDex,closetabDex){
	$("tab-"+tabDex).style.display="block";
	$("tab-"+closetabDex).style.display="none";
}
function showInfo(markerData){
	var er="<h4>"+markerData.name+"</h4><a class='tab' href='#' onclick='tab(0,1)'>Info</a><a class='tab' href='#' onclick='tab(1,0)'>Contact</a>";
	er+="<div id='tab-0'>"+markerData.details+"</div>";
	er+="<div id='tab-1' style='display:none'><iframe src='http://mapmeld.appspot.com/olpcMAP/contacter?id="+markerData.id+"' style='border:none;height:400px;width:400px;'></iframe></div>";
	$("iWin").innerHTML=er;
	$("iEnc").style.display="block";
	$("iWin").style.display="block";
}
function closeiWin(){
	$("iWin").style.display="none";
	$("iEnc").style.display="none";
}
var mapType="hybrid";
function set_type(type){
	if(type==mapType){return}
	try{$(mapType).className="maptype";$(type).className = "selectmaptype"}catch(e){}
	mapType=type;
	updateImg();
}
function updateImg(){
	if(mapType!="osm"){
		$("map").src="http://maps.google.com/maps/api/staticmap?sensor=false&zoom="+zoom+"&maptype="+mapType+"&size=400x500&format=jpg&center="+center.join(',')+markerStuff;
	}
	else{
		$("map").src="http://dev.openstreetmap.org/~pafciu17/?module=map&imgType=jpg&center="+center[1]+","+center[0]+"&zoom="+zoom+"&width=400&height=500";
	}
}
function clickToZoom(event){center=toLatLng(event.clientX,event.clientY);zoom++;updateImg()}
function clickingCenter(){cCtr=true;$("map").className="crosshairMap"}
function clkCtr(event){center=toLatLng(event.clientX,event.clientY);$("map").className="-moz-grab";cCtr=false;updateImg()}
function $(id){return document.getElementById(id)}
</script>
<style type="text/css">
body{font-family:arial}
#map{width:400px;height:500px;top:0px;left:80px;position:absolute;-moz-user-select:none;-khtml-user-select:none;user-select:none;}
img.crosshairMap{cursor:crosshair}
#go{position:absolute;bottom:30px;left:0px}
a.tab{font-size:10pt;margin-left:10px;margin-right:10px;}
#sidebar{position:absolute;top:0px;left:0px;width:80px;height:98%;border-top:1px solid #000;border-bottom:1px solid #000}
div.maptype{-moz-border-radius:5px;background-color:silver;color:#000;border:1px solid #000;padding:3px;cursor:pointer}
div.selectmaptype{-moz-border-radius:5px;background-color:#fff;color:#000;border:1px solid #000;padding:3px;font-weight:bold;cursor:pointer}
#iEnc{position:absolute;left:90px;top:30px;-moz-border-radius:10px;border:2px solid #000;background:#fff;width:330px;padding:3px;padding-left:10px;display:none;z-index:10}
input.cBtn{float:right}
input:hover{color:#000;cursor:pointer}
::-moz-selection{background:none;color:#fff}
textarea{border:1px solid #000}
img.zoom{cursor:pointer;margin-left:24px;border:1px solid #fff}
img.zoom:hover{border:1px solid #000}
</style>
</head>
<body id="body" onload="load();">
<div id="sidebar">
	<div id="roadmap" class="maptype" onclick="set_type('roadmap')">Map</div>
	<div id="satellite" class="maptype" onclick="set_type('satellite')">Satellite</div>
	<div id="hybrid" class="selectmaptype" onclick="set_type('hybrid')">Hybrid</div>
	<div id="terrain" class="maptype" onclick="set_type('terrain')">Terrain</div>
	<div id="osm" class="maptype" onclick="set_type('osm')">OSM</div>
	<span id="center">Center</span><br/><input type="button" onclick="clickingCenter()" value="(+)"/><br/><br/>
	<span id="zoom">Zoom</span><br/>
	<img src="http://maptonomy.appspot.com/zPlus.png" class="zoom" onclick="zoomIn()"/><br/><br/>
	<img src="http://maptonomy.appspot.com/zMinus.png" class="zoom" onclick="zoomOut()"/><br/><br/>
</div>
<img id="map" class="defaultMap" src="" onclick="if(cCtr){clkCtr(event)}else{clkMar(event)}" ondblclick="clickToZoom(event)" alt="Connecting to Google Maps..."/>
<div id="iEnc"><input type="button" class="cBtn" onclick="closeiWin()" value="x"/><div id="iWin"></div></div>
</body></html>''')
		else:
			self.response.out.write('''	infoWindow = new google.maps.InfoWindow();
	google.maps.event.addListener(map,'click',function(){if(!isEditor){infoWindow.close()}});
	for(var myPt=0;myPt<myPoints.length;myPt++){
		var marker;
		if(myPoints[myPt].icon.toLowerCase().indexOf("default") != -1){
			myPoints[myPt].icon="";
		}
		if(myPoints[myPt].icon.length > 6){
			marker=new google.maps.Marker({
				position:new google.maps.LatLng(myPoints[myPt].pt[0],myPoints[myPt].pt[1]),
				map:map,
				icon:new google.maps.MarkerImage(myPoints[myPt].icon,defSize),
				title:myPoints[myPt].name
			});
		}
		else{
			var myRandIcon=randIcon();
			marker=new google.maps.Marker({
				position:new google.maps.LatLng(myPoints[myPt].pt[0],myPoints[myPt].pt[1]),
				map:map,
				icon:new google.maps.MarkerImage(myRandIcon,defSize),
				title:myPoints[myPt].name
			});		
		}
		if(!myPoints[myPt].group){myPoints[myPt].group="";}
		myPoints[myPt].marker=marker;
		contentString=setupContent(myPt);
		addInfo(marker,contentString);
	}
	for(var mOrg=0;mOrg<orgs.length;mOrg++){
		if(orgs[mOrg].ajax){
			for(var mAj=0;mAj<orgs[mOrg].ajax.length;mAj++){
				if(specialRegion){
					if(orgs[mOrg].ajax[mAj].pt[0] > specialRegion.getBounds().getNorthEast().lat()){continue;}
					if(orgs[mOrg].ajax[mAj].pt[0] < specialRegion.getBounds().getSouthWest().lat()){continue;}
					if(orgs[mOrg].ajax[mAj].pt[1] > specialRegion.getBounds().getNorthEast().lng()){continue;}
					if(orgs[mOrg].ajax[mAj].pt[1] < specialRegion.getBounds().getSouthWest().lng()){continue;}
				}
				var marker=new google.maps.Marker({
					position:new google.maps.LatLng(orgs[mOrg].ajax[mAj].pt[0],orgs[mOrg].ajax[mAj].pt[1]),
					map:map,
					icon:"http://mapmeld.appspot.com/cluster-icon.jpg",
					title:orgs[mOrg].ajax[mAj].name
				});
				addQuery(marker,orgs[mOrg].ajax[mAj].query);
			}
		}
		if(orgs[mOrg].pts){
			if(orgs[mOrg].pts.length>0){
				for(var mPt=0;mPt<orgs[mOrg].pts.length;mPt++){
					if(specialRegion){
						if(orgs[mOrg].pts[mPt].pt[0] > specialRegion.getBounds().getNorthEast().lat()){continue;}
						if(orgs[mOrg].pts[mPt].pt[0] < specialRegion.getBounds().getSouthWest().lat()){continue;}
						if(orgs[mOrg].pts[mPt].pt[1] > specialRegion.getBounds().getNorthEast().lng()){continue;}
						if(orgs[mOrg].pts[mPt].pt[1] < specialRegion.getBounds().getSouthWest().lng()){continue;}
					}
					var myRandIcon=randIcon();
					orgs[mOrg].pts[mPt].icon=myRandIcon;
					orgs[mOrg].pts[mPt].id = "mOrg:" + mOrg + ":mPt:" + mPt;
					orgs[mOrg].pts[mPt].group = orgs[mOrg].name;
					var suggested=pU(orgs[mOrg].pts[mPt]);
					if(suggested){
						var marker = new google.maps.Marker({
							position:new google.maps.LatLng(orgs[mOrg].pts[mPt].pt[0],orgs[mOrg].pts[mPt].pt[1]),
							map:map,
							icon:new google.maps.MarkerImage(myRandIcon,defSize),
							title:orgs[mOrg].pts[mPt].name
						});
						myPoints[myPoints.length-1].marker=marker;
						addInfo(marker,setupContent(myPoints.length-1));
					}
				}
			}
		}
	}
	if(gup("id")){
		var ptID=gup("id");
		for(var mPt=0;mPt<myPoints.length;mPt++){
			if(myPoints[mPt].id==ptID){
				if(!specialRegion){
					map.setOptions({center:myPoints[mPt].marker.getPosition(),zoom:12});
				}
				infoWindow.setContent(setupContent(mPt));
				infoWindow.open(map,myPoints[mPt].marker);
				break;
			}
		}
	}
	geocoder = new google.maps.Geocoder();\n''')
		if(self.request.get('view') != 'alt'):
			self.response.out.write('''	var controlDiv = document.createElement('div');
	controlDiv.style.padding = '5px';
	var controlUI = document.createElement('div');
	controlUI.style.backgroundColor = 'white';
	controlUI.style.borderStyle = 'solid';
	controlUI.style.borderWidth = '2px';
	controlUI.style.borderColor = '#0000ff';
	controlUI.style.cursor = 'pointer';
	controlUI.style.textAlign = 'center';
	/*controlUI.style.minWidth = '300px';*/
	controlDiv.appendChild(controlUI);
	var controlText = document.createElement('input');
	controlText.id='searchbox';
	controlText.type='text';
	controlText.style.size=300;
	controlText.style.width="300";
	controlText.style.fontFamily = 'Arial,sans-serif';
	controlText.style.fontSize = '14px';
	controlText.style.height='90%';
	controlText.style.verticalAlign="middle";
	controlText.style.paddingLeft = '10px';
	controlText.style.paddingRight = '10px';
	controlText.style.fontSize="15pt";
	controlText.width="100%";
	/*controlText.size=18;*/
	controlText.minWidth="300";
	controlText.onkeydown=function(event){
		lastSText="";
		if(event!=null){
			if(event.keyCode==13){
				searchSearchBox();
			}
		}
	};
	controlUI.appendChild(controlText);
	
	var controlBtn = document.createElement('button');
	var xoIcon=document.createElement('img');
	xoIcon.src="http://mapmeld.appspot.com/xo-red.png";
	xoIcon.width="16"
	xoIcon.height="16"
	xoIcon.style.verticalAlign="middle";
	controlBtn.appendChild(xoIcon);
	var sSpan=document.createElement('span');
	sSpan.innerHTML='Search';
	controlBtn.appendChild(sSpan);
	controlUI.appendChild(controlBtn);
	google.maps.event.addDomListener(controlBtn,'click',function(){
		searchSearchBox();
	});
	map.controls[google.maps.ControlPosition.TOP].push(controlDiv);
	var searchOut = document.createElement('div');
	searchOut.id='searchResBox';
	searchOut.style.padding='4px';
	searchOut.style.borderTop='2px solid blue';
	searchOut.style.borderRight='2px solid blue';
	searchOut.style.backgroundColor='white';
	searchOut.style.width='16%';
	searchOut.style.height='80%';
	searchOut.width='16%';
	searchOut.height='80%';
	searchOut.style.overflow='scroll';
	map.controls[google.maps.ControlPosition.LEFT].push(searchOut);
	searchOut.style.display="none";''')
		self.response.out.write('''	if(gup("q")){
		searchAccept("geoq "+gup("q"));
	}
	try{
		$("projCheck").checked=true;
		$("volCheck").checked=true;
		$("newsCheck").checked=false;
	}
	catch(e){}
}
var newsLayer;
function toggle(cBox){
	switch(cBox.id){
		case "newsCheck":
			if(!newsLayer){
				newsLayer = new google.maps.KmlLayer("http://mapmeld.appspot.com/olpcMAPolpc/geonews?view=global",{map:map,preserveViewport:true});
			}
			else{
				if(cBox.checked){newsLayer.setMap(map)}
				else{newsLayer.setMap(null)}
			}
			break;
		case "projCheck":
			for(var i=0;i<myPoints.length;i++){
				if((myPoints[i].icon.indexOf("xo-")==-1)&&(myPoints[i].icon.indexOf("/olpcau/")==-1)){
					if(cBox.checked){
						myPoints[i].marker.setMap(map);
					}
					else{
						myPoints[i].marker.setMap(null);				
					}
				}
			}
			break;
		case "volCheck":
			for(var i=0;i<myPoints.length;i++){
				if((myPoints[i].icon.indexOf("xo-")!=-1)||(myPoints[i].icon.indexOf("/olpcau/")!=-1)){
					if(cBox.checked){
						myPoints[i].marker.setMap(map);
					}
					else{
						myPoints[i].marker.setMap(null);				
					}
				}
			}
			break;
	}
}
function p(pointData){
	myPoints.push(pointData);
}
function randIcon(){
	var randIcon;
	var randIconI=Math.floor(Math.random()*18);
	switch(randIconI){
		case 0:
			randIcon="http://google-maps-icons.googlecode.com/files/computer.png";
			break;
		case 1:
			randIcon="http://google-maps-icons.googlecode.com/files/world.png";
			break;
		case 2:
			randIcon="http://google-maps-icons.googlecode.com/files/industrialmuseum.png";
			break;
		case 3:
			randIcon="http://google-maps-icons.googlecode.com/files/music-classical.png";
			break;
		case 4:
			randIcon="http://google-maps-icons.googlecode.com/files/postal.png";
			break;
		case 5:
			randIcon="http://google-maps-icons.googlecode.com/files/housesolarpanel.png";
			break;
		case 6:
			randIcon="http://google-maps-icons.googlecode.com/files/park.png";
			break;
		case 7:
			randIcon="http://google-maps-icons.googlecode.com/files/laboratory.png";
			break;
		case 8:
			randIcon="http://google-maps-icons.googlecode.com/files/university.png";
			break;
		case 9:
			randIcon="http://google-maps-icons.googlecode.com/files/daycare.png";
			break;
		case 10:
			randIcon="http://google-maps-icons.googlecode.com/files/school.png";
			break;
		case 11:
			randIcon="http://google-maps-icons.googlecode.com/files/bookstore.png";
			break;
		case 12:
			randIcon="http://google-maps-icons.googlecode.com/files/workoffice.png";
			break;
		case 13:
			randIcon="http://google-maps-icons.googlecode.com/files/photo.png";
			break;
		case 14:
			randIcon="http://google-maps-icons.googlecode.com/files/bigcity.png";
			break;
		case 15:
			randIcon="http://google-maps-icons.googlecode.com/files/places-unvisited.png";
			break;
		case 16:
			randIcon="http://google-maps-icons.googlecode.com/files/amphitheater-tourism.png";
			break;
		case 17:
			randIcon="http://google-maps-icons.googlecode.com/files/flowers.png";
			break;
	}
	return randIcon;
}
function writeSearchCat(category,resultsList){
	if(resultsList.length==0){return ""}
	var searchCat='<div class="searchCat">' + category + '</div><ul class="searchList">';
	for(var sR=0;sR<resultsList.length;sR++){
		var provenName=resultsList[sR].name;
		while(provenName.indexOf("<")!=-1){
			provenName=provenName.replace("<","&lt;");
		}
		if(resultsList[sR].href){
			if(resultsList[sR].sharer){
				searchCat+='<li><span onclick="searchAccept('+"'"+resultsList[sR].acceptance+"'"+')">' + provenName + ' <a href="' + resultsList[sR].href + '" target="_blank">(Link)</a></span>';			
				searchCat+='<br/><small><i>shared by <a href="#" onclick="searchAccept(' + "'" + 'byName ' + resultsList[sR].sharer + "');" + '">' + resultsList[sR].sharer + '</a></i></small>';
			}
			else{
				searchCat+='<li onclick="searchAccept('+"'"+resultsList[sR].acceptance+"'"+')">' + provenName + ' <a href="' + resultsList[sR].href + '" target="_blank">(Link)</a>';			
			}
			searchCat+='</li>';
		}
		else{
			searchCat+='<li onclick="searchAccept('+"'"+resultsList[sR].acceptance+"'"+')">' + provenName + '</li>';
		}
	}
	searchCat+="</ul>"
	return searchCat;
}
function searchAccept(term){
	if(term.indexOf("viewport")==0){
		term=term.replace("viewport ","").split(",");
		map.fitBounds(new google.maps.LatLngBounds(new google.maps.LatLng(term[0],term[1]),new google.maps.LatLng(term[2],term[3])));
	}
	else if(term.indexOf("byName")==0){
		$("searchbox").value=term.replace("byName ","");
		searchSearchBox();
	}
	else if(term.indexOf("latlng")==0){
		term=term.replace("latlng","").replace(" ","").split(",");
		map.setCenter(new google.maps.LatLng(term[0],term[1]),12);
		map.setZoom(12);
	}
	else if(term.indexOf("myPoint")==0){
		var ptID=term.replace("myPoint","").replace(" ","");
		for(var mPt=0;mPt<myPoints.length;mPt++){
			if(myPoints[mPt].id==ptID){
				myPoints[mPt].marker.setAnimation(null);
				if(!specialRegion){
					map.setOptions({center:myPoints[mPt].marker.getPosition(),zoom:12});
				}
				infoWindow.setContent(setupContent(mPt));
				infoWindow.open(map,myPoints[mPt].marker);
				break;
			}
		}
	}
	else if(term.indexOf("geoq") != -1){
		term = term.replace("geoq ","").replace("geoq","");
		geocoder.geocode({'address':term},
			function(results,status){
				if(status==google.maps.GeocoderStatus.OK){
					if(results[0].geometry.viewport){
						map.fitBounds(results[0].geometry.viewport);
					}
					else{
						map.setCenter(results[0].geometry.location,12);
						map.setZoom(12);
					}
				}
			}
		);		
	}
	else if(term.indexOf("mOrg")==0){
		term=term.replace("mOrg ","");
		uniqueGroup=orgs[term];
		if(uniqueGroup.pts.length == 1){
			map.setCenter(new google.maps.LatLng(uniqueGroup.pts[0].pt[0],uniqueGroup.pts[0].pt[1]),16);
			approxd="<span class='topResult'>&rarr;"+uniqueGroup.name+"</span>";
		}
		else if(uniqueGroup.pts.length == 0){
			map.setCenter(new google.maps.LatLng(uniqueGroup.ajax[0].pt[0],uniqueGroup.ajax[0].pt[1]),16);
			var qScript=document.createElement("script");
			qScript.src="http://mapmeld.appspot.com/olpcMAP" + uniqueGroup.ajax[0].query + "&format=js&act=center";
			document.body.appendChild(qScript);
			approxd="<span class='topResult'>Loading "+uniqueGroup.name+"</span>";
		}
		else{
			var northMost=uniqueGroup.pts[0].pt[0];
			var southMost=uniqueGroup.pts[0].pt[0];
			var eastMost=uniqueGroup.pts[0].pt[1];
			var westMost=uniqueGroup.pts[0].pt[1];
			for(var grpPt=1;grpPt<uniqueGroup.pts.length;grpPt++){
				if(uniqueGroup.pts[grpPt].pt[0] > northMost){
					northMost=uniqueGroup.pts[grpPt].pt[0];
				}
				else if(uniqueGroup.pts[grpPt].pt[0] < southMost){
					southMost=uniqueGroup.pts[grpPt].pt[0];
				}
				if(uniqueGroup.pts[grpPt].pt[1] > eastMost){
					eastMost=uniqueGroup.pts[grpPt].pt[1];
				}
				else if(uniqueGroup.pts[grpPt].pt[1] < westMost){
					westMost=uniqueGroup.pts[grpPt].pt[1];
				}
			}
			map.fitBounds(new google.maps.LatLngBounds(
				new google.maps.LatLng(southMost,westMost),
				new google.maps.LatLng(northMost,eastMost)
			));
			approxd="<span class='topResult'>&rarr;"+uniqueGroup.name+"</span>";
		}
	}
	try{$("approxd").innerHTML="Choose a result"}catch(e){}
}
function gup(nm){nm=nm.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");var rxS="[\?&]"+nm+"=([^&#]*)";var rx=new RegExp(rxS);var rs=rx.exec(window.location.href);if(!rs){return null;}else{return rs[1];}}
function searchSearchBox(){
	makeSearch($("searchbox").value);
}
function makeSearch(search){
	approxd=null;
	joinNetwork=true;\n''')
		if(self.request.get('view')!='alt'):
			self.response.out.write('	map.setOptions({navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}});')
		self.response.out.write('''	searchCats="";
	$("searchResBox").style.display="block";
	var uniqueGroup = null;
	var matchItems = [];
	for(var grp=0;grp<orgs.length;grp++){
		if(orgs[grp].name.toLowerCase().indexOf(search.toLowerCase()) != -1){
			if(uniqueGroup==null){
				uniqueGroup = orgs[grp];
			}
			else{
				uniqueGroup = -1;
			}
			matchItems.push({name:orgs[grp].name,acceptance:"mOrg " + grp});
		}
		else if(orgs[grp].details!=null){
			if(orgs[grp].details.toLowerCase().indexOf(search.toLowerCase()) != -1){
				if(uniqueGroup==null){
					uniqueGroup = orgs[grp];
				}
				else{
					uniqueGroup = -1;
				}
				matchItems.push({name:orgs[grp].name,acceptance:"mOrg " + grp});
			}
		}
	}
	if((uniqueGroup != null) && (approxd==null)){
		if(uniqueGroup!=-1){
			if(uniqueGroup.pts.length==1){
				map.setCenter(new google.maps.LatLng(uniqueGroup.pts[0].pt[0],uniqueGroup.pts[0].pt[1]),16);
				approxd="<span class='topResult'>&rarr;"+uniqueGroup.name+"</span>";
			}
			else if(uniqueGroup.pts.length == 0){
				map.setCenter(new google.maps.LatLng(uniqueGroup.ajax[0].pt[0],uniqueGroup.ajax[0].pt[1]),16);
				var qScript=document.createElement("script");
				qScript.src="http://mapmeld.appspot.com/olpcMAP" + uniqueGroup.ajax[0].query + "&format=js&act=center";
				document.body.appendChild(qScript);
				approxd="<span class='topResult'>Loading "+uniqueGroup.name+"</span>";
			}
			else{
				var northMost=uniqueGroup.pts[0].pt[0];
				var southMost=uniqueGroup.pts[0].pt[0];
				var eastMost=uniqueGroup.pts[0].pt[1];
				var westMost=uniqueGroup.pts[0].pt[1];
				for(var grpPt=1;grpPt<uniqueGroup.pts.length;grpPt++){
					if(uniqueGroup.pts[grpPt].pt[0] > northMost){
						northMost=uniqueGroup.pts[grpPt].pt[0];
					}
					else if(uniqueGroup.pts[grpPt].pt[0] < southMost){
						southMost=uniqueGroup.pts[grpPt].pt[0];
					}
					if(uniqueGroup.pts[grpPt].pt[1] > eastMost){
						eastMost=uniqueGroup.pts[grpPt].pt[1];
					}
					else if(uniqueGroup.pts[grpPt].pt[1] < westMost){
						westMost=uniqueGroup.pts[grpPt].pt[1];
					}
				}
				map.fitBounds(new google.maps.LatLngBounds(
					new google.maps.LatLng(southMost,westMost),
					new google.maps.LatLng(northMost,eastMost)
				));
				approxd="<span class='topResult'>&rarr;"+uniqueGroup.name+"</span>";
			}
		}
	}
	searchCats+=writeSearchCat('Groups',matchItems);
	var uniquePoint = null;
	matchItems=[];
	var buried=""; // buried gives name precedence, even if term appears in two items' details or group names
	for(var mPt=0;mPt<myPoints.length;mPt++){
		if( myPoints[mPt].name.toLowerCase().indexOf(search.toLowerCase()) != -1){
			if(uniquePoint==null){
				uniquePoint = myPoints[mPt];
				uniquePoint.found = "name";
			}
			else if((uniquePoint != -1)||(buried=="group")||(buried=="details")){
				if((uniquePoint.found == "details")||(uniquePoint.found == "group")||(buried=="group")||(buried=="details")){
					uniquePoint = myPoints[mPt];
					uniquePoint.found="name";
					buried="";
				}
				else{
					uniquePoint=-1;
					buried="name";
				}
			}
			matchItems.push({name:myPoints[mPt].name,acceptance:"myPoint " + myPoints[mPt].id});
		}
		else if((myPoints[mPt].group!=null)&&(myPoints[mPt].group.toLowerCase().indexOf(search.toLowerCase()) != -1)){
			if(uniquePoint==null){
				uniquePoint = myPoints[mPt];
				uniquePoint.found="group";
			}
			else if((uniquePoint != -1)||(buried=="details")){
				if((uniquePoint.found == "details")||(buried=="details")){
					uniquePoint = myPoints[mPt];
					uniquePoint.found="group";
					buried="";
				}
				else if(uniquePoint.found == "group"){
					uniquePoint=-1;
					buried="group";
				}
			}
			matchItems.push({name:myPoints[mPt].name,acceptance:"myPoint " + myPoints[mPt].id});
		}
		else if(myPoints[mPt].details!=null){
			if(myPoints[mPt].details.toLowerCase().indexOf(search.toLowerCase()) != -1){
				if(uniquePoint==null){
					uniquePoint = myPoints[mPt];
					uniquePoint.found = "details";
				}
				else if(uniquePoint != -1){
					if(uniquePoint.found == "details"){
						uniquePoint = -1;
						buried="details";
					}
				}
				matchItems.push({name:myPoints[mPt].name,acceptance:"myPoint " + myPoints[mPt].id});
			}
		}
	}
	if((uniquePoint!=null)&&(approxd==null)){
		if(uniquePoint != -1){
			approxd="<span class='topResult'>&rarr;"+uniquePoint.name+"</span>";
			if(specialRegion==null){
				map.setOptions({center:uniquePoint.marker.getPosition(),zoom:12});
			}
			for(var mPt=0;mPt<myPoints.length;mPt++){
				if(myPoints[mPt].id==uniquePoint.id){
					infoWindow.setContent(setupContent(mPt));
					break;
				}
			}
			infoWindow.open(map,uniquePoint.marker);
		}
	}
	searchCats+=writeSearchCat('Points',matchItems);
	geocoder.geocode( { 'address':search},
		function(results,status) {
			if (status == google.maps.GeocoderStatus.OK){
				if((approxd==null)&&(results[0].geometry!=null)&&(results[0].geometry.viewport!=null)){
					map.fitBounds(results[0].geometry.viewport);
					$("approxd").innerHTML="<span class='topResult'>&rarr;" + results[0].address_components[0].long_name + " on Google Maps</span>";
				}
				var googResList=[];
				for(var googRes=0;googRes<results.length&&googRes<5;googRes++){
					var googName=""
					for(var gN=0;gN<results[googRes].address_components.length;gN++){
						if(gN!=0){googName+=", ";}
						googName+=results[googRes].address_components[gN].short_name;
					}
					googResList.push({name:googName,acceptance:"viewport " + results[googRes].geometry.viewport.toUrlValue()});
				}
				$("googMapSearch").innerHTML=writeSearchCat('Google Maps',googResList);
			}
			else{
				$("approxd").innerHTML="Choose a result";
			}
		}
	);

	var siteScript=document.createElement('script');
	siteScript.src="http://mapmeld.appspot.com/olpcMAP/search?q=" + search + "&out=js";
	$("head").appendChild(siteScript);

	if(approxd!=null){
		$("searchResBox").innerHTML="<div class='searchCat'><a href='#' onclick='closeSearch();'>&mdash;Close&mdash;</a></div><span id='approxd'>" + approxd + "</span><hr/><div id='olpcMAPsr'></div>" + searchCats + "<div id='googMapSearch'></div>";
	}
	else{
		$("searchResBox").innerHTML="<div class='searchCat'><a href='#' onclick='closeSearch();'>&mdash;Close&mdash;</a></div><span id='approxd'>Google Geocoding...</span><hr/><div id='olpcMAPsr'></div>" + searchCats + "<div id='googMapSearch'></div>";
	}
}
function closeSearch(){
	$("searchResBox").style.display="none";
	map.setOptions({navigationControlOptions:{style:google.maps.NavigationControlStyle.DEFAULT}});	
}
var lastOpen=null;
function addInfo(m,content){
	google.maps.event.clearInstanceListeners(m);
	google.maps.event.addListener(m,'click',function(){
		lastOpen=m;
		var manyMarkers=getNearbyMarkers(m.getPosition());
		if(manyMarkers.length > 1){
			var pageViewer;
			pageViewer="<div style='min-width:280px;'><div style='margin-left:auto;margin-right:auto;'>Many at this location: <a href='#' onclick='map.setOptions({center:new google.maps.LatLng(" + m.getPosition().lat() + ","+ m.getPosition().lng() + "),zoom:"+(map.getZoom()+2)+"});infoWindow.close();'>Zoom</a><br/>";
			var tablesOn=false;
			if(manyMarkers.length > 10){
				tablesOn=true;
				pageViewer+="<table><tr><td>";
			}
			pageViewer+="<ul>";
			for(var mPt=0;mPt<manyMarkers.length;mPt++){
				if((tablesOn)&&(mPt%10==0)&&(mPt!=0)){
						if(mPt > 30){break;}
						pageViewer+='</ul></td><td><ul>';
				}
				pageViewer+='<li><a href="#" onclick="loadNearby('+"'"+manyMarkers[mPt].id+"'"+')">'+manyMarkers[mPt].name+'</a></li>';
			}
			pageViewer+="</ul>";
			if(tablesOn){
				pageViewer+="</td></tr></table>";
			}
			infoWindow.setContent(pageViewer+"</div></div>");
		}
		else{
			infoWindow.setContent(content);
		}
		infoWindow.open(map,m);
	});\n''')
		if(self.request.get('view')=='alt'):
			self.response.out.write('''	google.maps.event.addListener(m,'mouseover',function(){
		try{
			var mID = content.substring(content.indexOf("mid='")+5);
			mID = mID.substring(0,mID.indexOf("'"));
			$("li-"+mID).style.backgroundColor="blue";
			$("li-"+mID).style.color="white";			
		}
		catch(e){}
	});
	google.maps.event.addListener(m,'mouseout',function(){
		try{
			var mID = content.substring(content.indexOf("mid='")+5);
			mID = mID.substring(0,mID.indexOf("'"));
			$("li-"+mID).style.backgroundColor="#aaaaff";
			$("li-"+mID).style.color="black";
		}
		catch(e){}
	});''')
		self.response.out.write('''}
function getNearbyMarkers(latlng){
	var nMarkers=[];
	var zoomFactor = 10 * Math.max(1, Math.pow(2,15-map.getZoom()) );
	for(var mPt=0;mPt<myPoints.length;mPt++){
		if(myPoints[mPt].marker==null){continue;}
		if( Math.abs(latlng.lat() - myPoints[mPt].marker.getPosition().lat()) < ( 0.0001 * zoomFactor )){
			if( Math.abs(latlng.lng() - myPoints[mPt].marker.getPosition().lng()) < ( 0.0001 * zoomFactor )){
				nMarkers.push(myPoints[mPt]);
			}
		}
	}
	return nMarkers;
}
function loadNearby(markId){
	var m,content;
	for(var mPt=0;mPt<myPoints.length;mPt++){
		if(myPoints[mPt].id == markId){
			m = myPoints[mPt].marker;
			content = setupContent(mPt);
			break;
		}
	}
	infoWindow.setContent(content);
	infoWindow.open(map,m);
}
function pS(pointObj){
	for(var mPt=0;mPt<myPoints.length;mPt++){
		if(myPoints[mPt].id==pointObj.id){
			myPoints[mPt]=pointObj;
			return;
		}
	}
	myPoints.push(pointObj);
}
function pU(pointObj){
	for(var mPt=0;mPt<myPoints.length;mPt++){
		if((myPoints[mPt].pt[0]==pointObj.pt[0])&&(myPoints[mPt].pt[1]==pointObj.pt[1])){
			return false;
		}
	}
	p(pointObj);
	return true;
}
function suggestEdit(){
	editorEmail=null;
	for(var mrk=0;mrk<myPoints.length;mrk++){
		if(myPoints[mrk].marker == lastOpen){
			openEditor(mrk,false);
			return;
		}
	}
}
function addQuery(mrkr,queryType){
	google.maps.event.addListener(mrkr,'click',function(){
		mrkr.setMap(null);
		var jsonScript=document.createElement("script")
		jsonScript.src="http://mapmeld.appspot.com/olpcMAP" + queryType + "&format=js";
		$("head").appendChild(jsonScript);
	});
}
function login(){
	$("coverwindow").style.display="block";
}
var joinNetwork=false;
var clickMoveMarker=null;
var editorEmail=null;
function joinNetworkMode(){
	joinNetwork=true;
	clickMoveMarker=new google.maps.Marker({
		position:map.getCenter(),
		draggable:true,
		map:map
	});
	var content="<div style='text-align:center'><h3>Join Our Network</h3>Click the map or drag this marker to set your position.<hr/>Email:<input id='editorEmail' onkeypress='plantMarkerShow()'/><input id='plantMarkerButton' style='display:none;' type='button' value='Plant Marker' onclick='plantMarker()'/></div><br/><hr/>";
	infoWindow.setContent(content);
	infoWindow.open(map,clickMoveMarker);	
	isEditor=true;
}
function plantMarkerShow(){
	$('plantMarkerButton').style.display="block";
	$('plantMarkerButton').style.display="inline";
}
function plantMarker(){
	editorEmail = $("editorEmail").value;
	p({marker:clickMoveMarker,group:"",pt:[clickMoveMarker.getPosition().lat(),clickMoveMarker.getPosition().lng()],icon:"DEFAULT",details:"Describe this place or person",name:"Edit Me"});
	openEditor(myPoints.length-1,true);
}
var fullIconList=["http://sites.google.com/site/olpcau/home/Orangesmall.png","http://sites.google.com/site/olpcau/home/Greensmall1.png","http://sites.google.com/site/olpcau/home/Bluesmall.png","http://sites.google.com/site/olpcau/home/Pinksmall.png","http://mapmeld.appspot.com/xo-red.png","http://mapmeld.appspot.com/xo-brown.png","http://mapmeld.appspot.com/xo-yellow.png","http://google-maps-icons.googlecode.com/files/computer.png","http://google-maps-icons.googlecode.com/files/world.png","http://google-maps-icons.googlecode.com/files/industrialmuseum.png","http://google-maps-icons.googlecode.com/files/music-classical.png","http://google-maps-icons.googlecode.com/files/postal.png","http://google-maps-icons.googlecode.com/files/housesolarpanel.png","http://google-maps-icons.googlecode.com/files/park.png","http://google-maps-icons.googlecode.com/files/laboratory.png","http://google-maps-icons.googlecode.com/files/university.png","http://google-maps-icons.googlecode.com/files/daycare.png","http://google-maps-icons.googlecode.com/files/school.png","http://google-maps-icons.googlecode.com/files/bookstore.png","http://google-maps-icons.googlecode.com/files/workoffice.png","http://google-maps-icons.googlecode.com/files/photo.png","http://google-maps-icons.googlecode.com/files/bigcity.png","http://google-maps-icons.googlecode.com/files/places-unvisited.png","http://google-maps-icons.googlecode.com/files/amphitheater-tourism.png","http://google-maps-icons.googlecode.com/files/flowers.png","http://google-maps-icons.googlecode.com/files/waterwellpump.png","http://google-maps-icons.googlecode.com/files/pyramid-southam.png","http://google-maps-icons.googlecode.com/files/glacier.png","http://google-maps-icons.googlecode.com/files/places-visited.png","http://google-maps-icons.googlecode.com/files/pagoda.png","http://google-maps-icons.googlecode.com/files/forest.png","http://google-maps-icons.googlecode.com/files/fossils.png","http://google-maps-icons.googlecode.com/files/animals.png","http://google-maps-icons.googlecode.com/files/pens.png","http://google-maps-icons.googlecode.com/files/doctor.png","http://google-maps-icons.googlecode.com/files/firstaid.png","http://google-maps-icons.googlecode.com/files/home.png","http://google-maps-icons.googlecode.com/files/cluster.png","http://google-maps-icons.googlecode.com/files/regroup.png","http://google-maps-icons.googlecode.com/files/recycle.png","http://google-maps-icons.googlecode.com/files/wifi.png","http://google-maps-icons.googlecode.com/files/fireworks.png","http://google-maps-icons.googlecode.com/files/music-rock.png","http://google-maps-icons.googlecode.com/files/museum.png","http://google-maps-icons.googlecode.com/files/zoo.png","http://google-maps-icons.googlecode.com/files/expert.png","http://google-maps-icons.googlecode.com/files/communitycentre.png","http://mapmeld.appspot.com/library.png"];
var fullIconString="<table><tr>";
for(var fi=0;fi<fullIconList.length;fi++){
	if(fi==0){
		fullIconString+="<td><img src='"+fullIconList[fi]+"' onclick='changeIcon(-1)'/>";	
	}
	else{
		if(fi%12==0){
			fullIconString+="</tr><tr>";
		}
		fullIconString+="<td><img src='"+fullIconList[fi]+"' onclick='changeIcon("+fi+")'/>";
	}
}
fullIconString+="</tr></table>";

function editorPg(gotoPg){
	$("editor-pg-"+(gotoPg-1)).style.display="none";
	$("editor-pg-"+gotoPg).style.display="block";
	$("editor-pg-button").onclick=function(event){ editorPg(gotoPg+1); }
	if(gotoPg < 3){
		$("editor-pg-button").innerHTML="> Photo >";
	}
	else{
		$("editor-pg-button").style.display="none";
	}
}
function changeIcon(num){
	if(num==-1){
		$("editorIcon").value=fullIconList[0];		
	}
	else{
		$("editorIcon").value=fullIconList[num];
	}
}
function openEditor(mIndex,isNew){
	isEditor=true;
	var m = myPoints[mIndex];
	var editorString="<div style='width:500px;height:370px;font-size:10pt;' width='500' height='450'>";
	if(isNew){
		editorString+="<div id='editor-pg-1' class='editPage'>Name<input id='editorTitle' style='width:70%;'/><hr/>";
		editorString+="<textarea id='editorText' style='width:80%;height:120px;'>Describe this place or person</textarea><hr/>";
		editorString+="Group name:<br/><input id='editorGroup' style='width:80%;height:18pt;'/></div>";
		editorString+="<div id='editor-pg-2' class='editPage' style='display:none;'>Select Icon<hr/><input id='editorIcon' style='width:70%;'/><br/>"+fullIconString+"</div>";
		editorString+="<div id='editor-pg-3' class='editPage' style='display:none;max-height:350px;'>Best photo:<br/><input id='editorPhoto' style='width:70%;border:1px solid #000;'/><br/><div id='editorUpDiv'><input type='button' onclick='upupload()' value='Upload'/></div><hr/>Photo album link<br/><input id='editorAlbum' style='width:70%;'/></div><div style='display:none;'></div>";
		editorString+="<button id='editor-pg-button' type='button' onclick='editorPg(2)'>&gt; Icon &amp; Photo &gt;</button>";
		editorString+="<hr/><input type='button' value='Save Edits' onclick='saveEdits("+mIndex+");'/></div></div>";
	}
	else{
		if(!myPoints[mIndex].photo){myPoints[mIndex].photo="";}
		if(!myPoints[mIndex].album){myPoints[mIndex].album="";}
		editorString+="<div id='editor-pg-1' class='editPage'><a href='http://olpcMAP.net/resetpoint?id="+myPoints[mIndex].id+"' target='_blank'>Change Name or Location</a><hr/>";
		editorString+="<textarea id='editorText' style='width:90%;height:150px;'>"+replaceEach(myPoints[mIndex].details,'<br>','\\n')+"</textarea><hr/>";
		editorString+="Group name:<br/><input id='editorGroup' style='width:80%;height:18pt;' value=\\""+replaceEach(myPoints[mIndex].group,'"',"'")+"\\"/></div>";
		editorString+="<div id='editor-pg-2' class='editPage' style='display:none;'>Select Icon<hr/><input id='editorIcon' style='width:70%;' value='"+myPoints[mIndex].icon+"'/><br/>"+fullIconString+"</div>";
		editorString+="<div id='editor-pg-3' class='editPage' style='display:none;max-height:350px;'>Best photo:<br/><input id='editorPhoto' style='width:70%;' value='"+myPoints[mIndex].photo+"'/><br/><div id='editorUpDiv'><input type='button' onclick='upupload()' value='Upload'/></div><hr/>Photo album link<br/><input id='editorAlbum' style='width:70%;' value='"+myPoints[mIndex].album+"'/></div><div style='display:none;'></div>";
		editorString+="<button id='editor-pg-button' type='button' onclick='editorPg(2)'>&gt; Icon &amp; Photo &gt;</button>";
		editorString+="<hr/><input type='button' value='Save Edits' onclick='saveEdits("+mIndex+");'/></div></div>";
	}
	infoWindow.setContent(editorString);
	infoWindow.open(map,m.marker);
	google.maps.event.addListener(infoWindow,'closeclick',function(){isEditor=false;ekey=null});
}
var ekey;
function upupload(){
	ekey=Math.random();
	$('editorUpDiv').innerHTML="<iframe src='http://mapmeld.appspot.com/olpcMAPimg?frame=i&ekey="+ekey+"' style='border:none;height:70px;width:350px;' height='70' width='350'></iframe>";
}
function contactMode(){
	$("coverwindow").style.display="block";
}
var sendPtIndex;
function saveEdits(mIndex){
	isEditor=false;
	var isNew=false;
	if(!myPoints[mIndex].id){
		isNew=true;
	}
	if($("editorTitle")){
		myPoints[mIndex].name=$("editorTitle").value;
	}
	myPoints[mIndex].details=replaceEach($("editorText").value,"\\n","<br/>");
	myPoints[mIndex].group=$("editorGroup").value;
	myPoints[mIndex].photo=$("editorPhoto").value;
	myPoints[mIndex].album=$("editorAlbum").value;
	myPoints[mIndex].email=editorEmail;
	var newIconMarkerIcon=$("editorIcon").value;
	if(newIconMarkerIcon != myPoints[mIndex].icon){
		var newIconMarker;
		if(myPoints[mIndex].marker){
			newIconMarker=new google.maps.Marker({
				position:myPoints[mIndex].marker.getPosition(),
				map:map,
				icon:new google.maps.MarkerImage(newIconMarkerIcon,defSize),
				title:myPoints[mIndex].name,
				draggable:isNew
			});
		}
		else{
			newIconMarker=new google.maps.Marker({
				position:new google.maps.LatLng(myPoints[mIndex].pt[0],myPoints[mIndex].pt[1]),
				map:map,
				icon:new google.maps.MarkerImage(newIconMarkerIcon,defSize),
				title:myPoints[mIndex].name,
				draggable:isNew
			});
		}
		myPoints[mIndex].icon=newIconMarkerIcon;
		myPoints[mIndex].marker.setMap(null);
		addInfo(newIconMarker,setupContent(mIndex));
		myPoints[mIndex].marker=newIconMarker;
	}
	if(isNew){var reopenListener=google.maps.event.addListener(myPoints[mIndex].marker,'dragend',function(){updatePosition(mIndex)})}
	sendPtIndex = mIndex;
	var sendPtScript=document.createElement("script");
	sendPtScript.src="http://mapmeld.appspot.com/olpcMAP/makePoint?id=" + myPoints[mIndex].id + "&point=" + myPoints[mIndex].marker.getPosition().lat() + "," + myPoints[mIndex].marker.getPosition().lng();
	sendPtScript.src+="&name="+myPoints[mIndex].name+"&details="+replaceEach(myPoints[mIndex].details,'&','~26')+"&group="+myPoints[mIndex].group+"&photo="+myPoints[mIndex].photo+"&album="+myPoints[mIndex].album + "&icon=" + myPoints[mIndex].icon + "&mail=" + myPoints[mIndex].email;
	if(ekey){
		sendPtScript.src+="&ekey="+ekey;
	}
	$("head").appendChild(sendPtScript);
	infoWindow.close();
	ekey=null;
	addInfo(myPoints[mIndex].marker,setupContent(mIndex));
}
function updatePosition(mIndex){
	var sendPtScript=document.createElement("script");
	sendPtScript.src="http://mapmeld.appspot.com/olpcMAP/makePoint?id=" + myPoints[mIndex].id + "&point=" + myPoints[mIndex].marker.getPosition().lat() + "," + myPoints[mIndex].marker.getPosition().lng();
	sendPtScript.src+="&cmd=loc";
	$("head").appendChild(sendPtScript);
}
function infoSlice(index,mIndex,tabid){
	for(var n=0;n<6;n++){
		var infoTab=$("infoWindow-"+n);
		if(infoTab){
			if(index==n){infoTab.style.display="block"}
			else{infoTab.style.display="none"}
		}
	}
	if(index==0){
		var markerData = myPoints[mIndex];
		$("infoWindow-0").innerHTML="Link to this point<br/><span style='font-size:10pt;'>http://olpcMAP.net?id=" + markerData.id + "</span><hr/>Link to profile page<br/><span style='font-size:10pt'>http://olpcMAP.net/page?id="+markerData.id+"</span><hr/>Link to nearby points:<br/><span style='font-size:10pt;'>http://olpcMAP.net?id="+markerData.id+"&km-distance=40</span><hr/>Share image of this zoom:<br/><span style='font-size:10pt'>http://olpcMAP.net?map=image&llregion=" + map.getBounds().getNorthEast().lat().toFixed(4) + "," + map.getBounds().getNorthEast().lng().toFixed(4) + "," + map.getBounds().getSouthWest().lat().toFixed(4) + "," + map.getBounds().getSouthWest().lng().toFixed(4) + "</span>";
	}
	else if(index==1){
		//contact form
		if(myPoints[mIndex].id.indexOf(":") == -1){
			$("infoWindow-contact").src="http://mapmeld.appspot.com/olpcMAP/contacter?id=" + myPoints[mIndex].id;
		}
		else{
			var myGroup = orgs[myPoints[mIndex].id.split(":")[1]];
			if(myGroup.website){
				$("infoWindow-contact").src="http://olpcMAP.net/contacter?web=" + myGroup.website;
			}
			else if(myGroup.name.indexOf("http") != -1){
				$("infoWindow-contact").src="http://olpcMAP.net/contacter?web=" + myGroup.name;
			}
			else{
				$("infoWindow-contact").src="http://olpcMAP.net/contacter?web="+escape("http://www.google.com/search?q="+myPoints[mIndex].name);
			}
		}
	}
	if(index > 2){
		$("infoFrame-"+index).src="http://mapmeld.appspot.com/olpcMAP/getTab?tid=" + tabid;
	}
}
function replaceEach(src,older,newer){
	while(src.indexOf(older)!=-1){
		src=src.replace(older,newer);
	}
	return src;
}
function linkify(unlinkedTxt){
	unlinkedTxt=replaceEach(unlinkedTxt,"Link:","link:");
	unlinkedTxt=replaceEach(unlinkedTxt,"link:"," link;");
	unlinkedTxt=replaceEach(unlinkedTxt," link;"," link:");	
	while(unlinkedTxt.indexOf("link:") != -1){
		linkUrl=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5,unlinkedTxt.length);
		linkAfter='';
		if(linkUrl.indexOf(" ")!=-1){
			linkUrl=linkUrl.substring(0,linkUrl.indexOf(" "));
			linkAfter=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5+linkUrl.length);
		}
		else if(linkUrl.indexOf("link:")!=-1){
			linkUrl=linkUrl.substring(0,linkUrl.indexOf("link:"));
			linkAfter=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5+linkUrl.length);
		}
		if(linkUrl.indexOf("http")==-1){
			linkUrl="http://"+linkUrl;
		}
		unlinkedTxt=unlinkedTxt.substring(0,unlinkedTxt.indexOf("link:")) + "<a target='_blank' href='" + linkUrl + "'>" + linkUrl + "</a>" + linkAfter;
	}
	return unlinkedTxt;
}
function setupContent(mIndex){
	var markerData = myPoints[mIndex];
	var contentString;
	contentString="<h4 style='font-size:11pt;'><a class='tab-select' mid='"+markerData.id+"' href='#' onclick='infoSlice(2,"+mIndex+",0)' style='font-size:12pt;'>"+markerData.name+"</a>";
	contentString+="<a class='tab' onclick='infoSlice(0,"+mIndex+",0)' href='#'>Bookmarks</a>";
	contentString+="<a class='tab' onclick='infoSlice(1,"+mIndex+",0)' href='#'>Contact</a>";
	var titles="";
	if(markerData.tabs){
		for(var mt=0;mt<markerData.tabs.length;mt++){
			if(titles.indexOf(markerData.tabs[mt].split("|")[0]+"|")==-1){
				contentString+="<a class='tab' onclick='infoSlice("+(mt*1+3)+","+mIndex+","+markerData.tabs[mt].split("|")[1]+")' href='#'>"+markerData.tabs[mt].split("|")[0]+"</a>";
				titles+=markerData.tabs[mt].split("|")[0]+"|";
			}
		}
	}
	contentString+="<a class='tab' href='#' onclick='openEditor("+mIndex+",false)'>Edit</a></h4>";
	//contentString+="<img src='http://mapmeld.appspot.com/plusIcon.gif' style='vertical-align:middle;margin-left:3px;' onclick='addTab("+mIndex+")'/>";
	contentString+="<div id='infoWindow-2' style='min-height:180px;'><table><tr>";
	var width="250";
	if(!markerData.photo){
		width="450";
	}
	contentString += "<td style='font-size:8pt;' width='"+width+"'>";
	if((markerData.group) && (markerData.group.length > 1)){
		contentString += "<span style='font-weight:bold'>From "+linkify(markerData.group)+"</span>";
	}
	contentString+="<hr/>";
	if(markerData.details){contentString += linkify(markerData.details)}
	else{contentString+="Please help us add details to this location"}
	contentString+="</td>";
	if(markerData.photo){
		if(markerData.album){
			contentString+="<td><div id='mediadiv'><a href='"+markerData.album+"' target='_blank'><img src='"+markerData.photo+"' style='max-height:150px;max-width:260px;' alt='BestPhoto'/><br/>View Photos</a></div></td>";		
		}
		else{
			contentString+="<td><div id='mediadiv'><img src='"+markerData.photo+"' style='max-height:150px;max-width:260px;'/></div></td>";
		}
	}
	else{
		if(markerData.album){
			contentString+="<td width='30pt'><a href='"+markerData.album+"' target='_blank'>View Photos</a></td>";
		}
		else{
			contentString+="<td width='10'></td>";
		}
	}
	contentString+="</tr></table></div>";
	contentString+="<div id='infoWindow-0' style='display:none;min-height:180px;'></div>";
	contentString+="<div id='infoWindow-1' style='display:none;min-height:180px;'><iframe id='infoWindow-contact' src='' style='border:none;' height='300' width='400'></iframe></div>";
	if(markerData.tabs){
		for(var mt=0;mt<markerData.tabs.length;mt++){
			contentString+="<div id='infoWindow-"+(mt*1+3)+"' style='display:none;min-height:180px;'></div>";
			contentString+="<div id='infoWindow-"+(mt*1+3)+"' style='display:none;min-height:180px;'><iframe id='infoFrame-"+(mt*1+3)+"' src='' style='border:none;' height='300' width='400'></iframe></div>";
		}
	}
	return contentString;
}
var openMarkerForTab;
function addTab(mIndex){
	openMarkerForTab=mIndex;
	myPoints[mIndex].tabs.push("Technical|new");
	var addTbScript=document.createElement("script");
	addTbScript.src="http://mapmeld.appspot.com/olpcMAP/addTab?id="+myPoints[mIndex].id+"&tid=new&type=Technical&content=";
	$("head").appendChild(addTbScript);
}
function bounce(mID){
	for(var m=0;m<myPoints.length;m++){
		if(mID==myPoints[m].id){
			myPoints[m].marker.setAnimation(google.maps.Animation.BOUNCE);
			return;
		}
	}
}
function unbounce(mID){
	for(var m=0;m<myPoints.length;m++){
		if(mID==myPoints[m].id){
			myPoints[m].marker.setAnimation(null);
			return;
		}
	}
}
function keyGoes(evt){if(event!=null){if(event.keyCode==13){searchSearchBox()}}}
function closeCoverWindow(){$("coverwindow").style.display="none"}
function $(id){return document.getElementById(id);}
	</script>
	<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:white;}
input{color:#000;}
h3{
	margin-bottom:0.5em;
}
button{
	vertical-align:middle;
	font-family:Arial,sans-serif;
	font-size:14px;
	font-weight:bold;
	padding:4px;
	color:#000000;
}
div.main{
	background-color:#DDDAA0;
}
span.navoption{
	color:#000000;
	text-decoration:none;
}
span.navoption a{
	color:#000000;
	text-decoration:none;
}
span.navoption:hover{
	color:#0000bb;
	text-decoration:underline;
}
span.navoption a:hover{
	color:#0000bb;
	text-decoration:underline;
}
a.tab{
	font-size:11pt;
	margin-left:8px;
	margin-right:8px;
	font-weight:normal;
}
a.tab-select{
	text-decoration:none;
	color:#500;
	font-weight:bold;
	margin-left:8px;
	margin-right:8px;
}
div.searchCat{
	background-color:#aaaaaa;
	font-weight:bold;
	padding:5px;
}
ul.searchList li{
	list-style-type:circle;
	font-size:10pt;
	padding:4px;
	margin-bottom:1px;
	cursor:pointer;
}
ul.searchList li:hover{
	background-color:#ccdddd;
}
span.topResult{
	font-size:11pt;
	background-color:#ccdddd;
}
li.prof{
	font-family:Arial,sans-serif;
	font-size:14px;
	border-bottom:1px solid black;
	cursor:pointer;
	padding:6px;
	list-style-type:none;
	margin-left:-30px;
	background-color:#aaaaff;
}
li.prof:hover{
	background-color:blue;
	color:white;
}
label{
	width:100%;
	margin-top:10px;
}
div.sBar{
  margin-top:-20px;
  -moz-box-shadow: 15px 15px 15px #ccc;
  -webkit-box-shadow: 15px 15px 15px #ccc;
  box-shadow: 15px 15px 15px #ccc;
}
	</style>
	<!--[if IE 6]><style type="text/css">li.prof{margin-left:0px;}</style><![endif]-->
	<!--[if IE 7]><style type="text/css">li.prof{margin-left:0px;}</style><![endif]-->
</head>
<body onload="init();">
	<div class="header">
		<h3><span style='font-size:1.7em;min-height:16pt;'>olpcMAP</span> - a geosocial network for Sugar and the XO <a href="http://www.facebook.com/pages/OlpcMAP/126840500716047" style="margin-left:8px;" target="_blank"><img src="http://facebook.com/favicon.ico" alt="Facebook Page" title="Facebook Page" style="height:16pt;"/></a><a href="http://twitter.com/olpcmap" style="margin-left:8px;" target="_blank"><img src="http://twitter.com/favicon.ico" title="Twitter Feed" alt="Twitter Feed" style="height:16pt;"/></a></h3>
		<noscript><h3>Enable JavaScript to view olpcMAP</h3></noscript>
		<br/>
	</div>
	<div class="nav">
		<span class="navoption"><a href="#" onclick="joinNetworkMode();">Join the Map Network</a></span>
		<span class="navoption"><a href="http://olpcMAP.net/home" target="_blank">Homepage</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/" target="_blank">Laptop Help</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">About Map</a></span>
		<span class="navoption"><a href="#" onclick="contactMode()">Contact</a></span>
	</div>\n''')
		if(self.request.get('view') == 'alt'):
			self.response.out.write('''	<table style="width:100%;height:100%;"><tr style="width:100%;vertical-align:top;">
		<td width="220" style="width:220px;">
			<div id="sidebar" class="sBar" style="width:225px;border-right:1px solid blue;margin-right:-6px;margin-top:10px;background-color:white;">
				<label style="border-bottom:1px solid silver;padding:4px;width:210px;"><input id="volCheck" type="checkbox" onclick="toggle(this)" checked/>Volunteers</label><br/><br/>
				<label style="border-bottom:1px solid silver;padding:4px;width:210px;"><input id="projCheck" type="checkbox" onclick="toggle(this)" checked/>Projects</label><br/><br/>
				<label style="padding:4px;width:210px;"><input id="newsCheck" type="checkbox" onclick="toggle(this)"/>News &amp; Updates</label>
				<hr/>
				<div style="background-color:white;padding:3px;padding-bottom:0px;cursor:pointer;text-align:center;max-width:250px;">
					<input id="searchbox" type="text" style="min-width:200px;width:200px;font-family:Arial,sans-serif;font-size:12pt;border:1px solid blue;" size="10" onkeypress="keyGoes(event);"/>
					<br/>
					<button onclick="searchSearchBox();" style="font-size:12pt;">
						<img src="https://sites.google.com/site/olpcau/home/Bluesmall.png" style="vertical-align:middle;height:10pt;width:10pt;"/>
						<span style="vertical-align:middle;">Find</span>
					</button>
				</div>
				<ul id="searchResBox" style="margin-left:-10px;width:194px;">\n''')
			if results is not None:
				topCount = 0
				for pt in results:
					myIcon = ''
					myIcon = myIcon + cgi.escape(pt.icon).replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000')
					if len(myIcon) < 3:
						myIcon = cgi.escape(pt.photo)
					if len(myIcon) < 3:
						continue
					myName = cgi.escape(pt.name)
					if(myName.find("privatized") != -1):
						fixname = myName.replace("privatized:","")
						sndNames = 0
						outname = ""
						for letter in fixname:
							if(sndNames == 0):
								outname = outname + letter
							elif(sndNames == -1):
								outname = outname + letter
								sndNames = 1
							if(letter == " "):
								sndNames = -1
								outname = outname + " "
						myName = outname
					if(len(myName) >= 25):
						myName = myName[0:25]+"..."
					myDetails = cgi.escape(pt.details[0:30])
					if(len(pt.details) >= 45):
						myDetails = myDetails + "..."
					if(myDetails.find('&lt;') == -1):
						myDetails = '<br/><span style="font-size:8pt;">'+myDetails+'</span>'
					else:
						myDetails = '<br/><span style="font-size:8pt;">'+myDetails[0:myDetails.find('&lt;')]+'...</span>'
					self.response.out.write('					<li id="li-' + str(pt.key().id()) + '" class="prof" onmouseover="bounce(\'' + str(pt.key().id()) + '\')" onmouseout="unbounce(\'' + str(pt.key().id()) + '\')" onclick="searchAccept(\'myPoint ' + str(pt.key().id()) + '\')"><img src="' + myIcon + '" style="max-width:20px;max-height:20px;vertical-align:top;float:left;position:float;"/><span style="vertical-align:middle;font-size:10pt;">' + myName + '</span>' + myDetails + '</li>\n')
					topCount = topCount + 1
					if(topCount >= 10):
						break
			else:
				self.response.out.write('''					<li class="prof">
						<img src="http://google-maps-icons.googlecode.com/files/red00.png" style="max-width:20px;max-height:20px;"/><span>Sample Result</span>
					</li>
					<li class="prof">
						<img src="http://google-maps-icons.googlecode.com/files/red01.png" style="max-width:20px;max-height:20px;"/><span>Sample Result</span>
					</li>
					<li class="prof">
						<img src="http://google-maps-icons.googlecode.com/files/red02.png" style="max-width:20px;max-height:20px;"/><span>Sample Result</span>
					</li>\n''')
			self.response.out.write('''				</ul>
			</div>
		</td><td>
			<div id="map" style="height:90%;width:100%;min-width:600px;min-height:700px;"></div>
		</td></tr></table>
		<div class="main">The goal of olpcMAP is to learn more about where education technology is in play - around the world and in our own neighborhoods. 

That means we would like to hear stories from you! Joining the network makes it easier for you to connect with technology projects near you,and makes it possible for experienced and enthusiastic volunteers to find your project and give their support. 

We are interested in opening up the network design process to embrace various strategies toward recruiting volunteers and sharing successes,trials,and tribulations of existing deployments.</div>\n''')
		else:
			self.response.out.write('''	<div id="map" style="height:90%;width:100%;margin:0px;padding:0px;"></div>
<div class="main">The goal of olpcMAP is to learn more about where education technology is in play - around the world and in our own neighborhoods. 

That means we would like to hear stories from you! Joining the network makes it easier for you to connect with technology projects near you,and makes it possible for experienced and enthusiastic volunteers to find your project and give their support. 

We are interested in opening up the network design process to embrace various strategies toward recruiting volunteers and sharing successes,trials,and tribulations of existing deployments.</div>\n''')
		self.response.out.write('''<div id="coverwindow" style="display:none;position:fixed;margin-left:auto;margin-right:auto;top:100px;border:1px solid black;font-size:16pt;text-align:right;background-color:#333333;">
		<input type="button" value="X" style="border:1px solid black;color:black;font-size:16pt;" onclick="closeCoverWindow();"/>
		<br/>
		<form id="signinform" style="width:100%;background-color:#ffffff; text-align:left; font-size:13pt;" action="http://mapmeld.appspot.com/olpcMAP/contact?id=you" method="POST">
			E-mail <input id="emaillogin" name="login"/><br/>
			<!--Password <input id="passwordlogin" type="password" name="password"/><hr/>-->
			Message<br/><textarea name="message" width="550" height="300"></textarea>
			<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Send"/>
		</form>
	</div>
	<div id="fb-root"></div>
	<!--<div id="fb-login-div" style="background-color:white;border:solid 2px #000;cursor:pointer;text-align:center;">
		<input type="button" value="Log In User" onclick="login();"/><br/><hr/><br/>
		<a href="''' + url + '''"><input type="button" value="Google SignIn"/></a><br/><hr/>
		<p><fb:login-button autologoutlink="true" onlogin="redirect()"></fb:login-button></p><br/>
	</div>
	<script type="text/javascript">
      window.fbAsyncInit = function() {
        FB.init({appId:'123994207657251',status:true,cookie:true,xfbml:true});
      };
	  function redirect(){
		//window.location="http://mapmeld.appspot.com/olpcMAP?fb_online";
		facebookUser=true;
		//FB_RequireFeatures(["XFBML"],function()
		//{
		//	FB.Facebook.init("541a5336e083acd2cc0b94c2fea7300d","http://mapmeld.appspot.com/xd_receiver.htm");
		//});
	  }
    </script>-->
</body>
</html>''')

class Offshoots(webapp.RequestHandler):
  def get(self):
	self.redirect('http://mapmeld.appspot.com/olpcmap-community.html')

class AddTab(webapp.RequestHandler):
  def get(self):
	return
	tabId = self.request.get('tid')
	content = self.request.get('content')
	if(tabId=='new'):
		newTab = PointTab()
		newTab.title=self.request.get('type')
		if(self.request.get('content')!=''):
			newTab.vars=[content.split('|')[0].split(',')]
			newTab.values=[content.split('|')[1].split(',')]
		else:
			newTab.vars=[]
			newTab.values=[]
		newTab.put()
		self.response.out.write('myPoints[openMarkerForTab].tabs[myPoints[openMarkerForTab].tabs.length-1]="'+self.request.get('type')+"|"+str(newTab.key().id())+'";infoWindow.close()')
		mrk = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
		mrk.tabs.append(self.request.get('type')+"|"+str(newTab.key().id()))
		mrk.put()
	else:
		newTab = PointTab.get_by_id(long(tabId))
		if(self.request.get('content')!=''):
			newTab.vars=[content.split('|')[0].split(',')]
			newTab.values=[content.split('|')[1].split(',')]
		else:
			newTab.vars=[]
			newTab.values=[]
		newTab.put()

class GetTab(webapp.RequestHandler):
  def get(self):
	tabId = self.request.get('tid')
	viewTab = PointTab.get_by_id(long(tabId))
	self.response.out.write('<table border="1">')
	for g in range(0,len(viewTab.vars)-1):
		self.response.out.write('<tr><td><b>' + viewTab.vars[g] + '</b></td><td>' + viewTab.values[g] + '</td></tr>')
	self.response.out.write('</table>')

class JSONin(webapp.RequestHandler):
  def get(self):
	sites = '''{}'''
	sites = sites.split('},')
	for site in sites:
		pt = GeoRefUsermadeMapPoint()
		pt.group = ""
		pt.country = ""
		#pt.region = "SouthCarolina"
		
		namelet = site[site.find("name:")+6:len(site)].replace("\\n","").replace("\n","").replace("\\r","").replace("\r","")
		namelet = namelet[0:namelet.find('"')]
		pt.name = "privatized:" + namelet
		
		center = site[site.find("pt:")+4:len(site)]
		pt.center = center[0:center.find(']')]
		
		email = site[site.find("email:")+7:len(site)]
		pt.email = email[0:email.find('"')].replace("\\n","").replace("\n","").replace("\\r","").replace("\r","")
		
		detailslet = site[site.find("details:")+9:len(site)]
		pt.details = detailslet[0:detailslet.find('"')]
		#pt.creator = users.get_current_user()

		#if(site.find("photo") != -1):
		#	pt.photo = site[site.find("photo:")+7:len(site)]
		#	pt.photo = pt.photo[0:pt.photo.find('"')]
		#else:
		pt.photo = ""
		
		#pt.album = site[site.find("album:")+7:len(site)]
		#pt.album = pt.album[0:pt.album.find('"')]
		pt.album = ""

		#pt.icon = site[site.find("icon:")+6:len(site)]
		#pt.icon = pt.icon[0:pt.icon.find('"')]
		iconSelect = random.randint(1,7)
		pt.icon = "DEFAULT"
		if(iconSelect==1):
			pt.icon = "http://sites.google.com/site/olpcau/home/Orangesmall.png"
		elif(iconSelect==2):
			pt.icon = "http://sites.google.com/site/olpcau/home/Greensmall1.png"
		elif(iconSelect==3):
			pt.icon ="http://sites.google.com/site/olpcau/home/Bluesmall.png"
		elif(iconSelect==4):
			pt.icon="http://sites.google.com/site/olpcau/home/Pinksmall.png"
		elif(iconSelect==5):
			pt.icon="http://mapmeld.appspot.com/xo-red.png"
		elif(iconSelect==6):
			pt.icon="http://mapmeld.appspot.com/xo-brown.png"
		elif(iconSelect==7):
			pt.icon="http://mapmeld.appspot.com/xo-yellow.png"
		pt.put()
	self.response.out.write('done-people')

class Contact(webapp.RequestHandler):
  def post(self):
   try:
	login = self.request.get('login')
	message = self.request.get('message')
	email = None
	if(self.request.get('id') == 'you'):
		email = "beautify@olpcMAP.net"
		if(login.find('@') == -1):
			return
		mail.send_mail(sender="beautify@olpcMAP.net",
			reply_to=(login or ''),
			to=email,
			subject="olpcMAP : Main Website Contact Form",
			body='Attached is a message from the main olpcMAP.net contact form.  E-mail ndoiron@mapmeld.com if you would prefer not to receive these e-mails.  Everything below the dashed line is FROM THE INTERNET and could be ANYONE. \n\n----------------------------\n\nAddress Given: ' + cgi.escape(login) + '\n\n' + cgi.escape(message))
	elif(self.request.get('id').find("http") != -1):
		self.response.out.write('Go to the group website at: ' + self.request.get('id'))
	else:
		myPt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
		email = myPt.email
		if(myPt.email == 'null'):
			email = myPt.creator.email()
		if(myPt.cc is not None):
			email = email + ";" + myPt.cc
		mail.send_mail(sender="beautify@olpcMAP.net",
			reply_to=(login or ''),
			to=email,
			subject="olpcMAP : New Message",
			body='''A user of http://olpcMAP.net sent a message to you through our contact form for -''' + myPt.name + '''-

If we should direct people to another e-mail address or a website, please write to us at beautify@olpcMAP.net  We hope that this service will allow networking between volunteers, teachers, programmers, and organizations.

We have not confirmed this user's identity or e-mail. Take caution with unfamiliar links.
-----------------------------------------------------------------------------------------

E-mail address given: ''' + cgi.escape(login) + '\n\n' + cgi.escape(message))
	self.response.out.write('<html style="height:100%"><body style="height:100%"><div height="120px" style="height:120px;">Message Sent</div>Message Sent</body></html>')
   except:
	self.response.out.write('<html>We apologize:<br/><br/>We don\'t know the contact information for this deployment.<br/><br/>Please try searching the internet, then use "Contact" to send a message to the website admin</html>')

  def get(self):
	if(self.request.get('web') != ''):
		self.response.out.write('''<!DOCTYPE html>
<html style="width:95%;font-size:10pt;">
	Link to group website:<br/><br/>
	<a href="''' + self.request.get('web') + '''" target="_blank">'''  + cgi.escape(self.request.get('web')) + '''</a>
</html>''')
	else:
		self.response.out.write('''<!DOCTYPE html>
<html style="width:95%;font-size:10pt;">
<form id="signinform" style="width:100%;background-color:#ffffff; text-align:left; font-size:13pt;" action="http://mapmeld.appspot.com/olpcMAP/contact?id=''' + cgi.escape(self.request.get('id')) + '''" method="POST">
	E-mail <input id="emaillogin" name="login"/><br/>
	Message<br/><textarea name="message" style="width:300px;height:200px;"></textarea>
	<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Send"/>
</form>
</html>''')

class JSONout(webapp.RequestHandler):
  def linkify(self,unlinkedTxt):
	unlinkedTxt=unlinkedTxt.replace('Link:','link:')
	unlinkedTxt=unlinkedTxt.replace('link:',' link:')
	while(unlinkedTxt.find("link:") != -1):
		linkUrl=unlinkedTxt[unlinkedTxt.find("link:")+5:len(unlinkedTxt)]
		linkAfter=''
		if(linkUrl.find("http")==-1):
			linkUrl="http://"+linkUrl
		if(linkUrl.find(" ")!=-1):
			linkUrl=linkUrl[0:linkUrl.find(" ")]
			linkAfter=unlinkedTxt[unlinkedTxt.find("link:")+5+len(linkUrl):len(unlinkedTxt)]
		unlinkedTxt=unlinkedTxt[0:unlinkedTxt.find("link:")] + "<a target='_blank' href='" + linkUrl + "'>" + linkUrl + "</a>" + linkAfter
	return unlinkedTxt
  def get(self):
	hiddenGeoResults = None
	geoPoints = None
	mapPoints = None
	if((self.request.get('format') == "js") or (self.request.get('format') == "ol-js")):
		self.response.out.write('var thisJSON=')

	if(self.request.get('byid') != ""):
		pt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('byid')))
		usename = cgi.escape(pt.name)
		if(usename.find("privatized") != -1):
			fixname = usename.replace("privatized:","")
			sndNames = 0
			outname = ""
			for letter in fixname:
				if(sndNames == 0):
					outname = outname + letter
				elif(sndNames == -1):
					outname = outname + letter
					sndNames = 1
				if(letter == " "):
					sndNames = -1
					outname = outname + " "
			usename = outname
		self.response.out.write('{"name":"' + cgi.escape(usename).replace('"','\\"') + '","id":"' + str(pt.key().id()) + '","pt":["' + str(pt.location.lat) + '","' + str(pt.location.lon) + '"],"icon":"' + pt.icon + '","details":"' + cgi.escape(pt.details).replace('"','\\"').replace("&lt;","<").replace("&gt;",">") + '","photo":"' + cgi.escape(pt.photo).replace('"','\\"') + '","album":"' + cgi.escape(pt.album).replace('"','\\"') + '","group":"' + self.linkify(cgi.escape(pt.group or "")).replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + '"}')
		return

	if(self.request.get('page') != ""):
		# divided into pages of up to 50 each
		# page 0 is static content and AJAX clusters
		pagenum = int(self.request.get('page'))
		if(pagenum == 0):
			# static content and AJAX clusters
			# issue: doesn't support lower counts per page
			self.response.out.write('''{
	"page":0,
	"pts":[
		{"group":"<a href='http://williamkamkwamba.typepad.com' target='_blank'>Moving Windmills</a>","name":"William Kamkwamba's Primary School","details":"1 XO,brought by William from TED in Arusha after telling the world about his homemade windmill.  Inspiring story.  <a href='http://williamkamkwamba.typepad.com/williamkamkwamba/2008/03/bringing-an-olp.html' target='_blank'>William's OLPC blog post</a>","pt":["-12.9829","33.6831"],"photo":"http://williamkamkwamba.typepad.com/williamkamkwamba/images/2008/03/21/img_0005.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"St. Anthony School,Dugawar,UP","details":"<a href='http://wiki.laptop.org/go/Oeuvre_des_pains' target='_blank'>School wiki page</a>","pt":["28.7168","78.5552"],"photo":"http://wiki.laptop.org/images/3/3c/OeuvreDesPains-Belgium-P1030833.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Auroville,TN","details":"<a href='http://wiki.laptop.org/go/OLPC_India/Auroville' target='_blank'>School wiki page</a>","pt":["12.0093","79.8102"],"photo":"http://wiki.laptop.org/images/4/44/The_Joy_of_Exploration.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Khairat School","pt":["18.917492","73.299408"],"details":"OLPC India's first pilot site<br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/Khairat_school' target='_blank'>School wiki page</a>","photo":"http://wiki.laptop.org/images/b/b8/P1060290.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Kikarwali","details":"India Foundation for Children Education and Care<br/><br/><a href='http://picasaweb.google.com/darshan2008/OLPCDeploymentProjectAtKikarwaliRajasthanIndiaOnMarch242010' target='_blank'>School Deployment Photos</a>","pt":["28.423199","75.60751"],"photo":"http://lh5.ggpht.com/_TKLjoqnmIB8/S6tmt8NyDhI/AAAAAAAAArA/6rZbCfBKDLQ/s512/DSC_0320.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Parikrma Center for Learning,Bangalore","details":"30 XO laptops were deployed at this center,run by the <a href='http://www.parikrmafoundation.org' target='_blank'>Parikrma Foundation</a><br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School-specific wiki page</a>","pt":["12.942348","77.585542"],"photo":"http://wiki.laptop.org/images/7/7b/Olpc-bangalore8.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Aradhna School, Bangalore","details":"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School wiki page</a>","pt":["12.885608","77.591865"],"photo":"http://wiki.laptop.org/images/6/66/Olpc-bangalore7.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Holy Mother School,Nashik","details":"<a href='http://wiki.laptop.org/go/OLPC_India/Nashik' target='_blank'>School wiki page</a>","pt":["20.00574","73.748186"],"photo":"http://wiki.laptop.org/images/9/9e/P1010444.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Mandal Parishad Primary School","details":"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Hyderabad-Mandal_Parishad_Primary_School' target='_blank'>School wiki page</a>","pt":["17.445319","78.38625"],"photo":"http://wiki.laptop.org/images/d/d5/DSC09954.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Our Lady of Merces High School","details":"wiki page under development","pt":["15.277893","73.924255"]},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Alag-Erdene soum","details":"one of three schools in Khovsgol district","pt":["50.1167","100.045"]},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Khatgal soum","details":"one of three schools in Khovsgol district","pt":["50.4425","100.1603"],"photo":"http://farm4.static.flickr.com/3233/2915260637_f5f0375063.jpg","details":"Photo CC-BY Elana Langer"},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"21 Ulanbaatar Schools","pt":["47.920484","106.925125"],"photo":"http://upload.wikimedia.org/wikipedia/commons/3/37/OLPC_Class_-_Mongolia_Ulaanbaatar.JPG"},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Khankh soum","details":"one of three schools in Khovsgol district","pt":["51.5023","100.6674"]},
		{"group":"<a href='http://www.olpc.asia/index.html' target='_blank'>OLPC Asia</a>","name":"Dujiangyan School,Sichuan","pt":["30.998285","103.619785"],"photo":"http://farm5.static.flickr.com/4138/4900464912_786490fed5_z.jpg","details":"Photo CC-BY OLPC"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Cambridge Friends School","details":"This XO pilot program is one of the first in the Boston area.  CFS is an independent K-8 Quaker school.  The XO is being introduced into the existing curriculum.","pt":["42.387","-71.1311"],"photo":"http://seeta.in/wiki/images/1/1e/DigiLit_at_CFS.JPG"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Mission Hill School","details":"This pilot program is DigiLit's first collaboration with the Boston Public School System.  The program is designed to help this charter school's 4th and 5th grades grow to a 1:1 laptop ratio","pt":["42.3306","-71.0993"],"photo":"http://seeta.in/wiki/images/3/3d/DigiLit_at_Mission_Hill.jpg"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Nicaragua Project","details":"In January 2010,DigiLit worked with the IADB to set up an XO laptop library at the Nicaraguan Deaf Association in Managua.  We are exploring how to close the education technology gap for these students.","pt":["12.1452","-86.2806"],"photo":"http://seeta.in/wiki/images/0/0d/DigiLit_in_Nicaragua_1.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Immokalee,Florida","details":"Held in one of the poorest towns in the US,this pilot partnered Waveplace,One by One Leadership Foundation,and Collier County's Migrant Student Summer Program. Waveplace was featured on NPR's All Things Considered.<br/><a href='http://waveplace.org/locations/florida' target='_blank'>Link</a>","pt":["26.4177","-81.413326"],"photo":"http://waveplace.com/mu/waveplace/item/tp122.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Buenos Aires, Nicaragua","details":"Our first pilot in Spanish,Waveplace worked with Campo Alegria to teach at arural elementary school without electricity. The government of Nicaragua was so impressed,they asked us to train 300 teachers throughout the country.<br/><a href='http://waveplace.org/locations/nicaragua' target='_blank'>Link</a>","pt":["11.455799","-85.759277"],"photo":"http://waveplace.com/mu/waveplace/item/tp166.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"St. John,US Virgin Islands","details":"Waveplace started our journey at Guy H. Benjamin Elementary School in Coral Bay with twenty fourth graders who received the world's first 20 production XOs from OLPC. The pilot was a true learning experience for all.<br/><a href='http://waveplace.org/locations/usvi' target='_blank'>Link</a>","pt":["18.360798","-64.74402"],"photo":"http://waveplace.com/mu/waveplace/item/tp16.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"St. Vincent Pilot","details":"<a href='http://waveplace.com/mu/waveplace/item/tp53' target='_blank'>Link</a> - please help us add details","pt":["13.235935","-61.180115"],"photo":"http://waveplace.com/mu/waveplace/item/tp51.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Port-au-Prince,Haiti","details":"Our first pilot in Haiti,taught in French,Waveplace trained teachers and orphans at Mercy & Sharing Foundation's John Branchizio School in Port-au-Prince. It was here we first felt our mission have a clear effect.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>","pt":["18.693001","-72.353511"],"photo":"http://waveplace.com/mu/waveplace/item/tp81.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Petite Rivere de Nippes,Haiti","details":"Partnering with the American Haitian Foundation,Waveplace trained four local mentors and three from the island of Lagonav. Petite Rivere remains our longest active pilot location in Haiti,with laptop classes continuing to this day.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>","pt":["18.473992","-73.23349"],"photo":"http://waveplace.com/mu/waveplace/item/tp2.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Cambridge","details":"<a href='http://waveplace.com/news/blog/archive/000850.jsp' target='_blank'>Link</a> - please help us add details","pt":["42.371988","-71.086693"],"photo":"http://waveplace.com/images/xoPrep.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"North Wahgi","pt":["-5.684658","144.49665"],"details":"250 XO laptops funded by PNGSDP","photo":"http://www.olpc.org.pg/images/stories/jim_taylor_primary1.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"Gaire","pt":["-9.676569","147.417297"],"details":"53 XO laptops,saturated 3rd grade class","photo":"http://wiki.laptop.org/images/d/d3/PNG-Nov08-2.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"Dreikikir","pt":["-3.57516","142.76946"],"details":"Dreikikir Admin Primary School is located in East Sepik Province,near Wewak. This school is participating in the EU-funded Improvement of Rural Primary Education Facilities (IRPEF) project,based in Madang. The IRPEF is collaborating with the Department of Education and OLPC Oceania to implement the trial."},
		{"group":"<a href='http://wiki.laptop.org/go/OLPC Birmingham' target='_blank'>OLPC Alabama</a>","name":"Birmingham","pt":["33.5271","-86.8229"],"details":"15000 XOs deployed? <a href='http://blog.laptop.org/2010/05/21/updates-from-alabama'>Latest update</a>","photo":"http://blog.laptop.org/wp-content/uploads/2010/05/westend-camp.jpg"},
		{"group":"Gureghian Family","name":"Chester Community Charter School","pt":["39.847031","-75.357971"],"details":"Deployment of 1400 laptops for students grades 3-8<br/><br/><a href='http://webcache.googleusercontent.com/search?q=cache:0yNNTyovLIcJ:wiki.laptop.org/images/9/9a/CCCS_12.10.08_Final.doc+olpc+chester&cd=1&hl=en&ct=clnk&gl=us' target='_blank'>Project Page</a>"},
		{"group":"<a href='http://amagezigemaanyi.blogspot.com' target='_blank'>Amagezi Gemaanyi Youth Association</a>","name":"Lubya Youth Education Centre","details":"Community center in Kampala; received XO laptops through Contributors Program project by USC","pt":["0.3289","32.5527"],"photo":"http://1.bp.blogspot.com/_3doFkXas3vs/TEy34ipYQbI/AAAAAAAABkU/XlMIvb3KrxA/S390/agya-olpc4.jpg"},
		{"group":"<a href='http://wiki.sugarlabs.org/go/Sugar_on_a_Stick_in_Delhi_India'>SEETA</a>","name":"Veda Vyasa DAV School","details":"Sugar on a Stick deployment in Delhi,India<br/>Our goal is to measure student learning improvements - students have a digital portfolio of their work and achievements. We will be publishing a case study in fall 2010 with a professor in Boston University's School of Education<br/><a href='http://theteamgoestoindia.wordpress.com' target='_blank'>Blog</a>","pt":["28.6384","77.0617"]},
		{"group":"<a href='http://sites.google.com/tecnotzotzil'>TecnoTzotzil</a>","name":"4 San Cristobal De Las Casas Schools","details":"SoaS deployment with 44 students,using Intel Classmate PCs. Photo CC-BY Jose I. Icaza","pt":["16.7404","-92.6307"],"photo":"http://farm3.static.flickr.com/2600/3979066854_e9fdf5c530.jpg"},
		{"group":"<a href='http://educalibre.cl'>Educa Libre</a>","name":"Florence Nightingale School","details":"SoaS deployment with 25 K-3 students in Macul,Chile. Acer netbooks and some PCs","pt":["-33.4871","-70.6048"],"photo":"http://educalibre.cl/wp-content/uploads/2010/07/alumno_piloto_memorice3.jpg"},
		{"group":"<a href='http://www.unitedactionforchildren.org'>United Action for Children</a>","name":"UPenn OLPCorps","details":"Students and teachers trained to use Scratch,Write,and more<br/><br/><a href='http://upennuac.blogspot.com/' target='_blank'>Blog</a>","pt":["4.061536","9.448242"],"photo":"http://1.bp.blogspot.com/_iSJqZVkttQc/SpM7e6-Qh_I/AAAAAAAAACc/YLR726R5GP0/s320/5848_237169645060_875880060_8375546_6766219_n%5B1%5D.jpg"},
		{"group":"<a href='http://www.ecbp.biz'>Ethiopia Engineering Capacity Building</a>","name":"OLPCorps:Dalarna U. and Royal IT","details":"<br/><br/><a href='http://wiki.laptop.org/go/OLPCorps_DKTH_ETHIO_PROPOSAL' target='_blank'>Wiki Page</a>","photo":"","pt":["7.939556","39.122314"]},
		{"group":"OLPCorps","name":"OLPCorps:Harvard and MIT","pt":["-24.20689","16.167669"]},
		{"group":"<a href='http://www.gmin.org' target='_blank'>GMin</a>","name":"OLPCorps Sahn Malen","details":"Princeton University and University of Maryland students<br/><br/><a href='http://olpcsm.blogspot.com/' target='_blank'>Wiki Page</a>","photo":"http://3.bp.blogspot.com/_I7lfwYcs8Jo/Sn871AI5K6I/AAAAAAAABpc/gzJ2XA-bed8/s400/DSC02252.JPG","pt":["8.063479","-11.42252"]},
		{"group":"<a href='http://www.one.org' target='_blank'>ONE</a>","name":"OLPCorps Senegal","details":"Students from U. Miami and U. Minnesota teamed up for this deployment<br/><br/><a href='http://www.one.org/blog/?p=7703' target='_blank'>Report from ONE.org</a><br/><br/><a href='http://africaxo.blogspot.com/' target='_blank'>Blog</a>","photo":"http://farm4.static.flickr.com/3500/3833004781_f0533a4c32.jpg","pt":["14.26638","-16.34697"]},
		{"group":"Intenge Development Foundation","name":"OLPCorps Namibia-Ngoma","details":"<br/><br/><a href='http://olpcorpsnamibiangoma.wordpress.com/' target='_blank'>Blog</a>","pt":["-20.131298","19.510431"]},
		{"group":"<a href='http://onehereonethere.org' target='_blank'>One Here One There</a>","name":"OLPCorps IU","details":"Students from Indiana University. Installed an electric generator and ran a short student newspaper-writing project.<br/><br/><a href='http://2009iuohot.blogspot.com/' target='_blank'>Blog</a>","pt":["-24.153019","29.351349"]},
		{"group":"OLPCorps","name":"OLPCorps:Niger","details":"University of Lagos,Royal Holloway University of London,and University of Salford students","pt":["8.762429","5.799923"]},
		{"group":"OLPCorps","name":"OLPCorps:Sierra Leone","details":"Tulane University and UC Davis students","pt":["8.760054","-12.572136"]},
		{"group":"OLPCorps","name":"OLPCorps:U of Education,Winneba","pt":["6.14128","-1.670179"]},
		{"group":"OLPCorps","name":"OLPCorps:U. Kinhasa","pt":["-1.710866","28.959188"]},
		{"group":"OLPCorps","name":"OLPCorps:U of Ibadan","details":"This project is targeted at empowering people with disabilities by improving their access to technology.<br/><br/><a href='http://abledisableinxo.blogspot.com' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_HbCc4VF-oTw/Splp_fs_JvI/AAAAAAAAADs/xI-fu0xLxWw/s320/teaching.jpg","pt":["9.277909","10.195785"]},
		{"group":"OLPCorps","name":"OLPCorps:CUNY Baruch","pt":["8.407168","0.087891"]},
		{"group":"OLPCorps","name":"OLPCorps:Soweto","details":"Deployment with detailed updates for the Global Post<br/><br/><a href='http://oplokhii.blogspot.com' target='_blank'>Blog</a>","pt":["-26.194877","27.993164"],"photo":"http://3.bp.blogspot.com/_jBm2wqTTQu8/SpX-ytitHwI/AAAAAAAAAQ4/PnIoAZ7bGME/s320/IMG_9629.JPG"},
		{"group":"OLPCorps","name":"OLPCorps:Mauritania","details":"Students from Cornell University","pt":["14.349548","-16.918945"]},
		{"group":"OLPCorps","name":"OLPCorps:Ungana Foundation","details":"Students from Utah State University supported the Ungana Foundation's effort to extend and support OLPC Rwanda<br/><br/><a href='http://unganafoundation.blogspot.com/'>Blog</a>","photo":"http://1.bp.blogspot.com/_EkMPu5bJnVU/Sqav0piu-cI/AAAAAAAAAPI/C3ZKbTbPpFA/s400/P1010406.JPG","pt":["-1.83406","29.486618"]},
		{"group":"OLPCorps","name":"OLPCorps:Heritage Nigeria","details":"Students from Texas A&M University<br/><br/><a href='http://olpcheritagenigeria.blogspot.com/' target='_blank'>Blog</a>","pt":["6.509768","3.537598"],"photo":"http://2.bp.blogspot.com/_ytQa4_LpsOk/SnfG0uka1-I/AAAAAAAAAFk/A5D3QoWvDkQ/s320/IMG_1478.JPG"},
		{"group":"OLPCorps","name":"OLPCorps:Zimbabwe","details":"Students from Macalester College,Midlands State University,and University of Zimbabwe - installed solar and then national grid power<br/><br/><a href='http://olpcorpszimbabwe09.blogspot.com' target='_blank'>Blog</a>","pt":["-17.137838","31.072083"]},
		{"group":"OLPCorps","name":"OLPCorps:Madagascar","details":"Students from GWU and U Maryland<br/><br/><a href='http://ampitso.wordpress.com/' target='_blank'>Blog</a>","photo":"http://ampitso.smugmug.com/photos/638764729_UCofq-M.jpg","pt":["-13.57024","49.306641"]},
		{"group":"OLPCorps","name":"OLPCorps:Laval University","details":"<br/><br/><a href='http://collabo.fse.ulaval.ca/olpc/' target='_blank'>Website</a>","photo":"http://collabo.fse.ulaval.ca/olpc/images/teach.jpg","pt":["3.387307","12.877007"]},
		{"group":"OLPCorps","name":"OLPCorps:Tanzania","details":"Students from Tumaini University.<br/><br/>The school was connected to the internet<br/><br/><a href='http://mot-tumaini.blogspot.com/' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_z6OVkOJNvTQ/SpvI0dyRxGI/AAAAAAAAAO4/ukhEnWkZXEg/s320/IMG0011A.jpg","pt":["-7.794677","35.690117"]},
		{"group":"OLPCorps","name":"OLPCorps:Vutakaka","details":"Students from U. Washington and the New School<br/><br/><a href='http://vutakakaolpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_C_wadBS6-ek/SmX5aiSypyI/AAAAAAAAIzg/XKbSjGgYCoo/s320/100_0057.jpg","pt":["-3.513421","39.835739"]},
		{"group":"OLPCorps","name":"OLPCorps:Kampala","details":"Still operating (though not online). Supported by MIT and Wellesley College<br/><br/><a href='http://uganda-olpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://2.bp.blogspot.com/_Sm-Wjgh0ZWk/SlCq2EOvw2I/AAAAAAAAABU/Xm_8bmDF7tY/s320/olpc_kps_10.JPG","pt":["0.29663","32.640381"]},
		{"group":"OLPCorps","name":"OLPCorps:GTech","details":"Students from Grahamstown and Gettysburg <a href='http://picasaweb.google.com/aimeegeorge/PicsFromGTECHSouthAfrica?feat=email#' target='_blank'>Photos Page</a><br/><br/><a href='http://gtech-olpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://lh3.ggpht.com/_7PSu0kxiZPQ/SrrntMYgpLI/AAAAAAAABFY/41saWNP1JNw/s640/P1080072.JPG","pt":["-33.315037","26.548634"]},
		{"group":"OLPCorps","name":"OLPCorps:Kwame Nkrumah U.","pt":["7.227441","-0.747414"]}
	],
	ajaxpts:[
		{"name":"OLPC South Carolina","pt":["33.767732","-80.507812"],"query":"http://maptonomy.appspot.com/json?state=SouthCarolina"},
		{"name":"OLPC Canada","pt":["55.786613","-98.885193"],"query":"http://maptonomy.appspot.com/json?country=Canada",icon:"http://lib.store.yahoo.net/lib/yhst-91918294864082/canada-flag.gif"},
		{"name":"OLPC Australia","pt":["-26.4312","121.6406"],"query":"http://maptonomy.appspot.com/json?country=Australia"},
		{"name":"OLE Nepal","pt":["27.3728","85.1897"],"query":"http://olpcMAP.net/json?country=Nepal"}
	]
}''')
			return
		else:
			pagePoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
			pageitems = 50
			if(self.request.get('per_page') != ""):
				try:
					pageitems = int(self.request.get('per_page'))
				except:
					pageitems = 50
			if((pageitems > 0) and (pageitems <= 50)):
				# accept lower count per page
				geoPoints = pagePoints.fetch(pageitems,(pagenum-1)*pageitems)
			else:
				# 50 maximum from pagePoints request
				geoPoints = pagePoints.fetch(50,(pagenum-1)*50)
			self.response.out.write('''{
	"page":"''' + str(pagenum) + '''",
	"per_page":"''' + str(pageitems) + '''",
	"pts":[''')
		
	if(self.request.get('country') != ""):
		self.response.out.write('''{
	"country":"''' + self.request.get('country') + '''",
	"pts":[''')
		mapPoints = GeoRefMapPoint.gql("WHERE country = :1 LIMIT 100",self.request.get('country'))
	
	elif(self.request.get('state') != ""):
		self.response.out.write('''{
	"state":"''' + cgi.escape(self.request.get('state')) + '''",
	"pts":[''')
		mapPoints = GeoRefMapPoint.gql("WHERE region = :1 LIMIT 100",self.request.get('state'))
	
	elif(self.request.get('center') != ""):
		ctr_lat = None
		ctr_lng = None
		suggestCtr = memcache.get("center:" + cgi.escape(self.request.get('center')))
		if(suggestCtr is not None):
			ctr_lat = suggestCtr.split(",")[0]
			ctr_lng = suggestCtr.split(",")[1]
		else:
			llcenter = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJ&q=" + self.request.get('center'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
			ctr_lat = llcenter[llcenter.find('latitude')+11:len(llcenter)]
			ctr_lat = ctr_lat[0:ctr_lat.find('"')]
			ctr_lng = llcenter[llcenter.find('longitude')+12:len(llcenter)]
			ctr_lng = ctr_lng[0:ctr_lng.find('"')]
			memcache.add("center:" + cgi.escape(self.request.get('center')),ctr_lat + "," + ctr_lng,500000)
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
				GeoRefUsermadeMapPoint.all(),
				geotypes.Point(float(ctr_lat),float(ctr_lng)),
				max_results=100,
				max_distance=1000 * radius)
		hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
				GeoRefMapPoint.all(),
				geotypes.Point(float(ctr_lat),float(ctr_lng)),
				max_results=100,
				max_distance=1000 * radius)
		self.response.out.write('''{
	"center":["''' + cgi.escape(ctr_lat) + '","' + cgi.escape(ctr_lng) + '''"],
	"kmdistance":"''' + str(radius) + '''",
	"pts":[''')
	
	elif(self.request.get('llcenter') != ""):
		ctr_lat = self.request.get('llcenter').replace('%20','').split(',')[0]
		ctr_lng = self.request.get('llcenter').replace('&20','').split(',')[1]
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Point(float(ctr_lat),float(ctr_lng)),
			max_results=100,
			max_distance=1000 * radius)
		self.response.out.write('''{
	"center":["''' + cgi.escape(ctr_lat) + '","' + cgi.escape(ctr_lng) + '''"],
	"kmdistance":"''' + str(radius) + '''",
	"pts":[''')
	
	elif(self.request.get('region') != ""):
		ne_lat=None
		ne_lng=None
		sw_lat=None
		sw_lng=None
		suggestRgn = memcache.get("region:" + cgi.escape(self.request.get('region')))
		if(suggestRgn is not None):
			# center was in memcache
			suggestRgn=suggestRgn.split(",")
			ne_lat = suggestRgn[0]
			ne_lng = suggestRgn[1]
			sw_lat = suggestRgn[2]
			sw_lng = suggestRgn[3]
		else:
			llregion = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJX&q=" + self.request.get('region'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
			ne_lat = llregion[llregion.find('north')+8:len(llregion)]
			ne_lat = ne_lat[0:ne_lat.find('"')]
			ne_lng = llregion[llregion.find('east')+7:len(llregion)]
			ne_lng = ne_lng[0:ne_lng.find('"')]
			sw_lat = llregion[llregion.find('south')+8:len(llregion)]
			sw_lat = sw_lat[0:sw_lat.find('"')]
			sw_lng = llregion[llregion.find('west')+7:len(llregion)]
			sw_lng = sw_lng[0:sw_lng.find('"')]
			memcache.add("region:" + cgi.escape(self.request.get('region')),ne_lat + "," + ne_lng + "," + sw_lat + "," + sw_lng,500000)
		geoPoints = GeoRefUsermadeMapPoint.bounding_box_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
			GeoRefMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100)
		self.response.out.write('''{
	"region":{"north":"''' + cgi.escape(ne_lat) + '","east":"' + cgi.escape(ne_lng) + '","south":"' + cgi.escape(sw_lat) + '","west":"' + cgi.escape(sw_lng) + '''"},
	"pts":[''')
	
	elif(self.request.get('llregion') != ""):
		ne_lat = self.request.get('llregion').replace('%20','').split(',')[0]
		ne_lng = self.request.get('llregion').replace('%20','').split(',')[1]
		sw_lat = self.request.get('llregion').replace('%20','').split(',')[2]
		sw_lng = self.request.get('llregion').replace('%20','').split(',')[3]
		geoPoints = GeoRefUsermadeMapPoint.bounding_box_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
			GeoRefMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		self.response.out.write('''{
	"region":{"north":"''' + cgi.escape(ne_lat) + '","east":"' + cgi.escape(ne_lng) + '","south":"' + cgi.escape(sw_lat) + '","west":"' + cgi.escape(sw_lng) + '''"},
	"pts":[''')
	
	elif((self.request.get('km-distance') != '') and (self.request.get('id') != '')):
		ctrPoint = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Point(ctrPoint.location.lat,ctrPoint.location.lon),
			max_results=100,
			max_distance=1000 * radius)
		hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
			GeoRefMapPoint.all(),
			geotypes.Point(ctrPoint.location.lat,ctrPoint.location.lon),
			max_results=100,
			max_distance=1000 * radius)
	drewPtPreviously = 0

	if mapPoints is not None:
		results = mapPoints.fetch(200)
		if results is not None:
			for pt in results:
				if(drewPtPreviously == 1):
					self.response.out.write(',')
				else:
					drewPtPreviously = 1
				usename = cgi.escape(pt.name)
				if(usename.find("privatized") != -1):
					fixname = usename.replace("privatized:","")
					sndNames = 0
					outname = ""
					for letter in fixname:
						if(sndNames == 0):
							outname = outname + letter
						elif(sndNames == -1):
							outname = outname + letter
							sndNames = 1
						if(letter == " "):
							sndNames = -1
							outname = outname + " "
					usename = outname
				self.response.out.write('		{"name":"' + cgi.escape(usename).replace('"','\\"') + '","id":"' + str(pt.key().id()) + '","pt":["' + str(pt.location.lat) + '","' + str(pt.location.lon) + '"],"icon":"' + pt.icon + '","details":"' + cgi.escape(pt.details).replace('"','\\"').replace("&lt;","<").replace("&gt;",">") + '","photo":"' + cgi.escape(pt.photo).replace('"','\\"') + '","album":"' + cgi.escape(pt.album).replace('"','\\"') + '","group":"' + self.linkify(cgi.escape(pt.group or "")).replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + '"}')
	
	if geoPoints is not None:
		for pt in geoPoints:
			if(drewPtPreviously == 1):
				self.response.out.write(',')
			else:
				drewPtPreviously = 1
			usename = cgi.escape(pt.name)
			if(usename.find("privatized") != -1):
				fixname = usename.replace("privatized:","")
				sndNames = 0
				outname = ""
				for letter in fixname:
					if(sndNames == 0):
						outname = outname + letter
					elif(sndNames == -1):
						outname = outname + letter
						sndNames = 1
					if(letter == " "):
						sndNames = -1
						outname = outname + " "
				usename = outname
			self.response.out.write('		{"name":"' + cgi.escape(usename).replace('"','\\"') + '","id":"' + str(pt.key().id()) + '","pt":["' + str(pt.location.lat) + '","' + str(pt.location.lon) + '"],"icon":"' + pt.icon + '","details":"' + cgi.escape(pt.details).replace('"','\\"').replace("&lt;","<").replace("&gt;",">") + '","photo":"' + cgi.escape(pt.photo).replace('"','\\"') + '","album":"' + cgi.escape(pt.album).replace('"','\\"') + '","group":"' + self.linkify(cgi.escape(pt.group or "")).replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + '"}')
	
	if hiddenGeoResults is not None:
		for pt in hiddenGeoResults:
			if(drewPtPreviously == 1):
				self.response.out.write(',')
			else:
				drewPtPreviously = 1
			usename = cgi.escape(pt.name)
			if(usename.find("privatized") != -1):
				fixname = usename.replace("privatized:","")
				sndNames = 0
				outname = ""
				for letter in fixname:
					if(sndNames == 0):
						outname = outname + letter
					elif(sndNames == -1):
						outname = outname + letter
						sndNames = 1
					if(letter == " "):
						sndNames = -1
						outname = outname + " "
				usename = outname
			self.response.out.write('		{"name":"' + cgi.escape(usename).replace('"','\\"') + '","id":"' + str(pt.key().id()) + '","pt":["' + str(pt.location.lat) + '","' + str(pt.location.lon) + '"],"icon":"' + pt.icon + '","details":"' + cgi.escape(pt.details).replace('"','\\"').replace("&lt;","<").replace("&gt;",">") + '","photo":"' + cgi.escape(pt.photo).replace('"','\\"') + '","album":"' + cgi.escape(pt.album).replace('"','\\"') + '","group":"' + self.linkify(cgi.escape(pt.group or "")).replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + '"}')

	self.response.out.write('''	]
}''')
	if((self.request.get('format') == "js") and (self.request.get('offmap') == '')):
		self.response.out.write(''';
for(var jsMrk=0;jsMrk<thisJSON.pts.length;jsMrk++){
	var cluSize=new google.maps.Size(16,24);
	if(clusters){
		var marker=new google.maps.Marker({
			position:new google.maps.LatLng(thisJSON.pts[jsMrk].pt[0],thisJSON.pts[jsMrk].pt[1]),
			icon:new google.maps.MarkerImage(thisJSON.pts[jsMrk].icon,cluSize,null,null,cluSize),
			title:thisJSON.pts[jsMrk].name
		});
		clusters.addMarker(marker);
	}
	else{
		var marker=new google.maps.Marker({
			position:new google.maps.LatLng(thisJSON.pts[jsMrk].pt[0],thisJSON.pts[jsMrk].pt[1]),
			map:map,
			icon:new google.maps.MarkerImage(thisJSON.pts[jsMrk].icon,cluSize,null,null,cluSize),
			title:thisJSON.pts[jsMrk].name
		});
	}
	thisJSON.pts[jsMrk].marker=marker;
	myPoints.push(thisJSON.pts[jsMrk]);
	var contentString=setupContent(myPoints.length-1);
	addInfo(marker,contentString);
}''')
	elif((self.request.get('format') == "js") and (self.request.get('offmap') == 'y')):
		self.response.out.write(';\nfor(var jsMrk=0;jsMrk<thisJSON.pts.length;jsMrk++){myPoints.push(thisJSON.pts[jsMrk])}')
	elif(self.request.get('format') == "ol-js"):
		self.response.out.write(''';
for(var jsMrk=0;jsMrk<thisJSON.pts.length;jsMrk++){
	myPoints.push(thisJSON.pts[jsMrk]);
	var point,pointFeature;
	point = new OpenLayers.Geometry.Point(thisJSON.pts[jsMrk].pt[1],thisJSON.pts[jsMrk].pt[0]).transform(map.displayProjection,map.projection);
	var myStyle=OpenLayers.Util.extend({},style_blue);
	myStyle.externalGraphic=thisJSON.pts[jsMrk].icon;
	pointFeature=new OpenLayers.Feature.Vector(point,null,myStyle);
	pointFeature.attributes={title:thisJSON.pts[jsMrk].name,description:setupContent(myPoints.length-1)};
	mapMrks.addFeatures([pointFeature]);
	myPoints[myPoints.length-1].marker=pointFeature;
	if(!myPoints[myPoints.length-1].group){myPoints[myPoints.length-1].group=""}
}''')
	if(self.request.get('act') != ""):
		if(self.request.get('act') == 'center'):
			self.response.out.write('''
if(thisJSON.pts.length > 0){
	var northMost=thisJSON.pts[0].pt[0];
	var southMost=thisJSON.pts[0].pt[0];
	var eastMost=thisJSON.pts[0].pt[1];
	var westMost=thisJSON.pts[0].pt[1];
	for(var jsMrk=1;jsMrk<thisJSON.pts.length-1;jsMrk++){
		if(thisJSON.pts[jsMrk].pt[0]>northMost){northMost=thisJSON.pts[jsMrk].pt[0]}
		if(thisJSON.pts[jsMrk].pt[0]<southMost){southMost=thisJSON.pts[jsMrk].pt[0]}
		if(thisJSON.pts[jsMrk].pt[1]>eastMost){eastMost=thisJSON.pts[jsMrk].pt[1]}
		if(thisJSON.pts[jsMrk].pt[1]<westMost){westMost=thisJSON.pts[jsMrk].pt[1]}
	}\n''')
			if(self.request.get('format') == 'js'):
				self.response.out.write('''	map.fitBounds(new google.maps.LatLngBounds(
		new google.maps.LatLng(southMost,westMost),
		new google.maps.LatLng(northMost,eastMost)
	));
}''')
			else:
				self.response.out.write('''	map.zoomToExtent(new OpenLayers.Bounds(eastMost,northMost,westMost,southMost).transform(map.displayProjection,map.projection));
}''')

class RSSout(webapp.RequestHandler):
  def linkify(self,unlinkedTxt):
	unlinkedTxt=unlinkedTxt.replace('Link:','link:')
	unlinkedTxt=unlinkedTxt.replace('link:',' link:')
	while(unlinkedTxt.find("link:") != -1):
		linkUrl=unlinkedTxt[unlinkedTxt.find("link:")+5:len(unlinkedTxt)]
		linkAfter=''
		if(linkUrl.find("http")==-1):
			linkUrl="http://"+linkUrl
		if(linkUrl.find(" ")!=-1):
			linkUrl=linkUrl[0:linkUrl.find(" ")]
			linkAfter=unlinkedTxt[unlinkedTxt.find("link:")+5+len(linkUrl):len(unlinkedTxt)]
		unlinkedTxt=unlinkedTxt[0:unlinkedTxt.find("link:")] + "<a target='_blank' href='" + linkUrl + "'>" + linkUrl + "</a>" + linkAfter
	return unlinkedTxt

  def get(self):
	self.response.out.write('''<?xml version="1.0"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss"> 
	<channel> 
		<title>olpcMAP.net GeoRSS Feed</title> 
		<link>http://olpcMAP.net/</link> 
		<pubDate>''' + str(datetime.now()) + '''</pubDate> 
		<description>Global updates feed of volunteer and deployment community</description> 
		<generator>Custom Google AppEngine Renderer</generator> 
		<atom:link href="http://mapmeld.appspot.com/olpcMAPolpc/feed" rel="self" type="application/rss+xml" />\n''')
	mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
	results = mapPoints.fetch(10)
	for pt in results:
		usename = cgi.escape(pt.name)
		if(usename.find("privatized") != -1):
			fixname = usename.replace("privatized:","")
			sndNames = 0
			outname = ""
			for letter in fixname:
				if(sndNames == 0):
					outname = outname + letter
				elif(sndNames == -1):
					outname = outname + letter
					sndNames = 1
				if(letter == " "):
					sndNames = -1
					outname = outname + " "
			usename = outname
		self.response.out.write('''		<item>
			<title>''' + usename + '''</title> 
			<link>http://olpcMAP.net?id=''' + str(pt.key().id()) + '''</link> 
			<description><![CDATA[''' + self.linkify(cgi.escape(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '<img style="float:right;" src="' + cgi.escape(pt.photo or "").replace('"','\\"') + '"/><br/><img src="http://mapmeld.appspot.com/olpcMAP?map=image&id=' + str(pt.key().id()) + '''&km-distance=80&w=550&h=100&z=10"/><br/><hr/><br/>]]></description> 
			<pubDate>''' + str(pt.lastUpdate) + '''</pubDate> 
			<guid>http://olpcMAP.net?id=''' + str(pt.key().id()) + '&amp;t=' + str(pt.lastUpdate.time()) + '''</guid> 
			<georss:point>''' + str(pt.location.lat) + ' ' + str(pt.location.lon) + '''</georss:point> 
		</item>\n''')
	self.response.out.write('''	</channel>
</rss>''')

class KMLout(webapp.RequestHandler):
  def linkify(self,unlinkedTxt):
	unlinkedTxt=unlinkedTxt.replace('Link:','link:')
	unlinkedTxt=unlinkedTxt.replace('link:',' link:')
	while(unlinkedTxt.find("link:") != -1):
		linkUrl=unlinkedTxt[unlinkedTxt.find("link:")+5:len(unlinkedTxt)]
		linkAfter=''
		if(linkUrl.find("http")==-1):
			linkUrl="http://"+linkUrl
		if(linkUrl.find(" ")!=-1):
			linkUrl=linkUrl[0:linkUrl.find(" ")]
			linkAfter=unlinkedTxt[unlinkedTxt.find("link:")+5+len(linkUrl):len(unlinkedTxt)]
		unlinkedTxt=unlinkedTxt[0:unlinkedTxt.find("link:")] + "<a target='_blank' href='" + linkUrl + "'>" + linkUrl + "</a>" + linkAfter
	return unlinkedTxt
  def get(self):
	self.response.headers['Content-Type'] = "application/vnd.google-earth.kml+xml"
	if(self.request.get('nl') != ''):
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP Latest Map</name>
		<NetworkLink>
			<name>olpcMAP Latest Map</name>
			<refreshVisibility>1</refreshVisibility>
			<Link>
				<href>''' + self.request.url.replace("nl=","lk=").replace("&","&amp;") + '''</href>
				<refreshMode>onChange</refreshMode>
				<flyToView>1</flyToView>
				<viewRefreshMode>never</viewRefreshMode>
			</Link>
		</NetworkLink>
	</Document>
</kml>''')
		return

	hiddenGeoResults = None
	geoPoints = None
	mapPoints = None
	if(self.request.get('byid') != ""):
		pt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('byid')))
		if(pt.icon==''):
			pt.icon='DEFAULT'
		usename = cgi.escape(pt.name)
		if(usename.find("privatized") != -1):
			fixname = usename.replace("privatized:","")
			sndNames = 0
			outname = ""
			for letter in fixname:
				if(sndNames == 0):
					outname = outname + letter
				elif(sndNames == -1):
					outname = outname + letter
					sndNames = 1
				if(letter == " "):
					sndNames = -1
					outname = outname + " "
			usename = outname
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP Marker</name>
		<Style id="style-''' + self.request.get('byid') + '''">
			<IconStyle>
				<Icon>
					<href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href>
				</Icon>
			</IconStyle>
		</Style>
		<Placemark>
			<id>''' + str(pt.key().id()) + '''</id>''')
		if(pt.group != ""):
			self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ' from ' + self.linkify(cgi.escape(pt.group or "")).replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + ']]></name>')
		else:
			self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ']]></name>')		
		self.response.out.write('			<styleUrl>#style-' + self.request.get('byid') + '''</styleUrl>
			<Icon><href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href></Icon>
			<Point>
				<coordinates>''' + str(pt.location.lon) + ',' + str(pt.location.lat) + ''',0</coordinates>
			</Point>\n''')
		if(pt.photo != ""):
			if(pt.album != ""):
				self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank"><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/><br/>View Photos</a></td></tr></table>]]></description>')					
			else:
				self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/></td></tr></table>]]></description>')
		elif(pt.album != ""):
			self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank">View Photos</a></td></tr></table>]]></description>')
			
		else:
			self.response.out.write('			<description><![CDATA[' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + ']]></description>')
		self.response.out.write('''		</Placemark>
	</Document>
</kml>''')
		return

	if(self.request.get('page') != ""):
		# divided into pages of up to 50 each
		# page 0 is static content and AJAX clusters
		pagenum = int(self.request.get('page'))
		if(pagenum == 0):
			# static content and AJAX clusters
			# issue: doesn't support lower counts per page
			self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP Page 0</name>''')
			staticdata =[
		{"group":"<a href='http://williamkamkwamba.typepad.com' target='_blank'>Moving Windmills</a>","name":"William Kamkwamba's Primary School","details":"1 XO,brought by William from TED in Arusha after telling the world about his homemade windmill.  Inspiring story.  <a href='http://williamkamkwamba.typepad.com/williamkamkwamba/2008/03/bringing-an-olp.html' target='_blank'>William's OLPC blog post</a>","pt":[-12.9829,33.6831],"photo":"http://williamkamkwamba.typepad.com/williamkamkwamba/images/2008/03/21/img_0005.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"St. Anthony School,Dugawar,UP","details":"<a href='http://wiki.laptop.org/go/Oeuvre_des_pains' target='_blank'>School wiki page</a>","pt":[28.7168,78.5552],"photo":"http://wiki.laptop.org/images/3/3c/OeuvreDesPains-Belgium-P1030833.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Auroville,TN","details":"<a href='http://wiki.laptop.org/go/OLPC_India/Auroville' target='_blank'>School wiki page</a>","pt":[12.0093,79.8102],"photo":"http://wiki.laptop.org/images/4/44/The_Joy_of_Exploration.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Khairat School","pt":[18.917492,73.299408],"details":"OLPC India's first pilot site<br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/Khairat_school' target='_blank'>School wiki page</a>","photo":"http://wiki.laptop.org/images/b/b8/P1060290.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Kikarwali","details":"India Foundation for Children Education and Care<br/><br/><a href='http://picasaweb.google.com/darshan2008/OLPCDeploymentProjectAtKikarwaliRajasthanIndiaOnMarch242010' target='_blank'>School Deployment Photos</a>","pt":[28.423199,75.60751],"photo":"http://lh5.ggpht.com/_TKLjoqnmIB8/S6tmt8NyDhI/AAAAAAAAArA/6rZbCfBKDLQ/s512/DSC_0320.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Parikrma Center for Learning,Bangalore","details":"30 XO laptops were deployed at this center,run by the <a href='http://www.parikrmafoundation.org' target='_blank'>Parikrma Foundation</a><br/><br/><a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School-specific wiki page</a>","pt":[12.942348,77.585542],"photo":"http://wiki.laptop.org/images/7/7b/Olpc-bangalore8.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Aradhna School, Bangalore","details":"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Bangalore.Parikrma' target='_blank'>School wiki page</a>","pt":[12.885608,77.591865],"photo":"http://wiki.laptop.org/images/6/66/Olpc-bangalore7.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Holy Mother School,Nashik","details":"<a href='http://wiki.laptop.org/go/OLPC_India/Nashik' target='_blank'>School wiki page</a>","pt":[20.00574,73.748186],"photo":"http://wiki.laptop.org/images/9/9e/P1010444.jpg"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Mandal Parishad Primary School","details":"<a href='http://wiki.laptop.org/go/OLPC_India/DBF/Hyderabad-Mandal_Parishad_Primary_School' target='_blank'>School wiki page</a>","pt":[17.445319,78.38625],"photo":"http://wiki.laptop.org/images/d/d5/DSC09954.JPG"},
		{"group":"<a href='http://www.digitalbridgefoundation.org' target='_blank'>DBF OLPC India</a>","name":"Our Lady of Merces High School","details":"wiki page under development","pt":[15.277893,73.924255]},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Alag-Erdene soum","details":"one of three schools in Khovsgol district","pt":[50.1167,100.045]},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Khatgal soum","details":"one of three schools in Khovsgol district","pt":[50.4425,100.1603],"photo":"http://farm4.static.flickr.com/3233/2915260637_f5f0375063.jpg","details":"Photo CC-BY Elana Langer"},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"21 Ulanbaatar Schools","pt":[47.920484,106.925125],"photo":"http://upload.wikimedia.org/wikipedia/commons/3/37/OLPC_Class_-_Mongolia_Ulaanbaatar.JPG"},
		{"group":"<a href='http://www.laptop.gov.mn' target='_blank'>OLPC Mongolia</a>","name":"Khankh soum","details":"one of three schools in Khovsgol district","pt":[51.5023,100.6674]},
		{"group":"<a href='http://www.olpc.asia/index.html' target='_blank'>OLPC Asia</a>","name":"Dujiangyan School,Sichuan","pt":[30.998285,103.619785],"photo":"http://farm5.static.flickr.com/4138/4900464912_786490fed5_z.jpg","details":"Photo CC-BY OLPC"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Cambridge Friends School","details":"This XO pilot program is one of the first in the Boston area.  CFS is an independent K-8 Quaker school.  The XO is being introduced into the existing curriculum.","pt":[42.387,-71.1311],"photo":"http://seeta.in/wiki/images/1/1e/DigiLit_at_CFS.JPG"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Mission Hill School","details":"This pilot program is DigiLit's first collaboration with the Boston Public School System.  The program is designed to help this charter school's 4th and 5th grades grow to a 1:1 laptop ratio","pt":[42.3306,-71.0993],"photo":"http://seeta.in/wiki/images/3/3d/DigiLit_at_Mission_Hill.jpg"},
		{"group":"<a href='http://www.digiliteracy.org' target='_blank'>Digital Literacy Project</a>","name":"Nicaragua Project","details":"In January 2010,DigiLit worked with the IADB to set up an XO laptop library at the Nicaraguan Deaf Association in Managua.  We are exploring how to close the education technology gap for these students.","pt":[12.1452,-86.2806],"photo":"http://seeta.in/wiki/images/0/0d/DigiLit_in_Nicaragua_1.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Immokalee,Florida","details":"Held in one of the poorest towns in the US,this pilot partnered Waveplace,One by One Leadership Foundation,and Collier County's Migrant Student Summer Program. Waveplace was featured on NPR's All Things Considered.<br/><a href='http://waveplace.org/locations/florida' target='_blank'>Link</a>","pt":[26.4177,-81.413326],"photo":"http://waveplace.com/mu/waveplace/item/tp122.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Buenos Aires, Nicaragua","details":"Our first pilot in Spanish,Waveplace worked with Campo Alegria to teach at arural elementary school without electricity. The government of Nicaragua was so impressed,they asked us to train 300 teachers throughout the country.<br/><a href='http://waveplace.org/locations/nicaragua' target='_blank'>Link</a>","pt":[11.455799,-85.759277],"photo":"http://waveplace.com/mu/waveplace/item/tp166.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"St. John,US Virgin Islands","details":"Waveplace started our journey at Guy H. Benjamin Elementary School in Coral Bay with twenty fourth graders who received the world's first 20 production XOs from OLPC. The pilot was a true learning experience for all.<br/><a href='http://waveplace.org/locations/usvi' target='_blank'>Link</a>","pt":[18.360798,-64.74402],"photo":"http://waveplace.com/mu/waveplace/item/tp16.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"St. Vincent Pilot","details":"<a href='http://waveplace.com/mu/waveplace/item/tp53' target='_blank'>Link</a> - please help us add details","pt":[13.235935,-61.180115],"photo":"http://waveplace.com/mu/waveplace/item/tp51.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Port-au-Prince,Haiti","details":"Our first pilot in Haiti,taught in French,Waveplace trained teachers and orphans at Mercy & Sharing Foundation's John Branchizio School in Port-au-Prince. It was here we first felt our mission have a clear effect.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>","pt":[18.693001,-72.353511],"photo":"http://waveplace.com/mu/waveplace/item/tp81.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Petite Rivere de Nippes,Haiti","details":"Partnering with the American Haitian Foundation,Waveplace trained four local mentors and three from the island of Lagonav. Petite Rivere remains our longest active pilot location in Haiti,with laptop classes continuing to this day.<br/><a href='http://waveplace.com/mu/locations/haiti' target='_blank'>Link</a>","pt":[18.473992,-73.23349],"photo":"http://waveplace.com/mu/waveplace/item/tp2.jpg"},
		{"group":"<a href='http://waveplace.org' target='_blank'>Waveplace</a>","name":"Cambridge","details":"<a href='http://waveplace.com/news/blog/archive/000850.jsp' target='_blank'>Link</a> - please help us add details","pt":[42.371988,-71.086693],"photo":"http://waveplace.com/images/xoPrep.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"North Wahgi","pt":[-5.684658,144.49665],"details":"250 XO laptops funded by PNGSDP","photo":"http://www.olpc.org.pg/images/stories/jim_taylor_primary1.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"Gaire","pt":[-9.676569,147.417297],"details":"53 XO laptops,saturated 3rd grade class","photo":"http://wiki.laptop.org/images/d/d3/PNG-Nov08-2.jpg"},
		{"group":"<a href='http://www.olpc.org.pg' target='_blank'>OLPC Papua New Guinea</a>","name":"Dreikikir","pt":[-3.57516,142.76946],"details":"Dreikikir Admin Primary School is located in East Sepik Province,near Wewak. This school is participating in the EU-funded Improvement of Rural Primary Education Facilities (IRPEF) project,based in Madang. The IRPEF is collaborating with the Department of Education and OLPC Oceania to implement the trial."},
		{"group":"<a href='http://wiki.laptop.org/go/OLPC Birmingham' target='_blank'>OLPC Alabama</a>","name":"Birmingham","pt":[33.5271,-86.8229],"details":"15000 XOs deployed? <a href='http://blog.laptop.org/2010/05/21/updates-from-alabama'>Latest update</a>","photo":"http://blog.laptop.org/wp-content/uploads/2010/05/westend-camp.jpg"},
		{"group":"Gureghian Family","name":"Chester Community Charter School","pt":[39.847031,-75.357971],"details":"Deployment of 1400 laptops for students grades 3-8<br/><br/><a href='http://webcache.googleusercontent.com/search?q=cache:0yNNTyovLIcJ:wiki.laptop.org/images/9/9a/CCCS_12.10.08_Final.doc+olpc+chester&cd=1&hl=en&ct=clnk&gl=us' target='_blank'>Project Page</a>"},
		{"group":"<a href='http://amagezigemaanyi.blogspot.com' target='_blank'>Amagezi Gemaanyi Youth Association</a>","name":"Lubya Youth Education Centre","details":"Community center in Kampala; received XO laptops through Contributors Program project by USC","pt":[0.3289,32.5527],"photo":"http://1.bp.blogspot.com/_3doFkXas3vs/TEy34ipYQbI/AAAAAAAABkU/XlMIvb3KrxA/S390/agya-olpc4.jpg"},
		{"group":"<a href='http://wiki.sugarlabs.org/go/Sugar_on_a_Stick_in_Delhi_India'>SEETA</a>","name":"Veda Vyasa DAV School","details":"Sugar on a Stick deployment in Delhi,India<br/>Our goal is to measure student learning improvements - students have a digital portfolio of their work and achievements. We will be publishing a case study in fall 2010 with a professor in Boston University's School of Education<br/><a href='http://theteamgoestoindia.wordpress.com' target='_blank'>Blog</a>","pt":[28.6384,77.0617]},
		{"group":"<a href='http://sites.google.com/tecnotzotzil'>TecnoTzotzil</a>","name":"4 San Cristobal De Las Casas Schools","details":"SoaS deployment with 44 students,using Intel Classmate PCs. Photo CC-BY Jose I. Icaza","pt":[16.7404,-92.6307],"photo":"http://farm3.static.flickr.com/2600/3979066854_e9fdf5c530.jpg"},
		{"group":"<a href='http://educalibre.cl'>Educa Libre</a>","name":"Florence Nightingale School","details":"SoaS deployment with 25 K-3 students in Macul,Chile. Acer netbooks and some PCs","pt":[-33.4871,-70.6048],"photo":"http://educalibre.cl/wp-content/uploads/2010/07/alumno_piloto_memorice3.jpg"},
		{"group":"<a href='http://www.unitedactionforchildren.org'>United Action for Children</a>","name":"UPenn OLPCorps","details":"Students and teachers trained to use Scratch,Write,and more<br/><br/><a href='http://upennuac.blogspot.com/' target='_blank'>Blog</a>","pt":[4.061536,9.448242],"photo":"http://1.bp.blogspot.com/_iSJqZVkttQc/SpM7e6-Qh_I/AAAAAAAAACc/YLR726R5GP0/s320/5848_237169645060_875880060_8375546_6766219_n%5B1%5D.jpg"},
		{"group":"<a href='http://www.ecbp.biz'>Ethiopia Engineering Capacity Building</a>","name":"OLPCorps:Dalarna U. and Royal IT","details":"<br/><br/><a href='http://wiki.laptop.org/go/OLPCorps_DKTH_ETHIO_PROPOSAL' target='_blank'>Wiki Page</a>","photo":"","pt":[7.939556,39.122314]},
		{"group":"OLPCorps","name":"OLPCorps:Harvard and MIT","pt":[-24.20689,16.167669]},
		{"group":"<a href='http://www.gmin.org' target='_blank'>GMin</a>","name":"OLPCorps Sahn Malen","details":"Princeton University and University of Maryland students<br/><br/><a href='http://olpcsm.blogspot.com/' target='_blank'>Wiki Page</a>","photo":"http://3.bp.blogspot.com/_I7lfwYcs8Jo/Sn871AI5K6I/AAAAAAAABpc/gzJ2XA-bed8/s400/DSC02252.JPG","pt":[8.063479,-11.42252]},
		{"group":"<a href='http://www.one.org' target='_blank'>ONE</a>","name":"OLPCorps Senegal","details":"Students from U. Miami and U. Minnesota teamed up for this deployment<br/><br/><a href='http://www.one.org/blog/?p=7703' target='_blank'>Report from ONE.org</a><br/><br/><a href='http://africaxo.blogspot.com/' target='_blank'>Blog</a>","photo":"http://farm4.static.flickr.com/3500/3833004781_f0533a4c32.jpg","pt":[14.26638,-16.34697]},
		{"group":"Intenge Development Foundation","name":"OLPCorps Namibia-Ngoma","details":"<br/><br/><a href='http://olpcorpsnamibiangoma.wordpress.com/' target='_blank'>Blog</a>","pt":[-20.131298,19.510431]},
		{"group":"<a href='http://onehereonethere.org' target='_blank'>One Here One There</a>","name":"OLPCorps IU","details":"Students from Indiana University. Installed an electric generator and ran a short student newspaper-writing project.<br/><br/><a href='http://2009iuohot.blogspot.com/' target='_blank'>Blog</a>","pt":[-24.153019,29.351349]},
		{"group":"OLPCorps","name":"OLPCorps:Niger","details":"University of Lagos,Royal Holloway University of London,and University of Salford students","pt":[8.762429,5.799923]},
		{"group":"OLPCorps","name":"OLPCorps:Sierra Leone","details":"Tulane University and UC Davis students","pt":[8.760054,-12.572136]},
		{"group":"OLPCorps","name":"OLPCorps:U of Education,Winneba","pt":[6.14128,-1.670179]},
		{"group":"OLPCorps","name":"OLPCorps:U. Kinhasa","pt":[-1.710866,28.959188]},
		{"group":"OLPCorps","name":"OLPCorps:U of Ibadan","details":"This project is targeted at empowering people with disabilities by improving their access to technology.<br/><br/><a href='http://abledisableinxo.blogspot.com' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_HbCc4VF-oTw/Splp_fs_JvI/AAAAAAAAADs/xI-fu0xLxWw/s320/teaching.jpg","pt":[9.277909,10.195785]},
		{"group":"OLPCorps","name":"OLPCorps:CUNY Baruch","pt":[8.407168,0.087891]},
		{"group":"OLPCorps","name":"OLPCorps:Soweto","details":"Deployment with detailed updates for the Global Post<br/><br/><a href='http://oplokhii.blogspot.com' target='_blank'>Blog</a>","pt":[-26.194877,27.993164],"photo":"http://3.bp.blogspot.com/_jBm2wqTTQu8/SpX-ytitHwI/AAAAAAAAAQ4/PnIoAZ7bGME/s320/IMG_9629.JPG"},
		{"group":"OLPCorps","name":"OLPCorps:Mauritania","details":"Students from Cornell University","pt":[14.349548,-16.918945]},
		{"group":"OLPCorps","name":"OLPCorps:Ungana Foundation","details":"Students from Utah State University supported the Ungana Foundation's effort to extend and support OLPC Rwanda<br/><br/><a href='http://unganafoundation.blogspot.com/'>Blog</a>","photo":"http://1.bp.blogspot.com/_EkMPu5bJnVU/Sqav0piu-cI/AAAAAAAAAPI/C3ZKbTbPpFA/s400/P1010406.JPG","pt":[-1.83406,29.486618]},
		{"group":"OLPCorps","name":"OLPCorps:Heritage Nigeria","details":"Students from Texas A&M University<br/><br/><a href='http://olpcheritagenigeria.blogspot.com/' target='_blank'>Blog</a>","pt":[6.509768,3.537598],"photo":"http://2.bp.blogspot.com/_ytQa4_LpsOk/SnfG0uka1-I/AAAAAAAAAFk/A5D3QoWvDkQ/s320/IMG_1478.JPG"},
		{"group":"OLPCorps","name":"OLPCorps:Zimbabwe","details":"Students from Macalester College,Midlands State University,and University of Zimbabwe - installed solar and then national grid power<br/><br/><a href='http://olpcorpszimbabwe09.blogspot.com' target='_blank'>Blog</a>","pt":[-17.137838,31.072083]},
		{"group":"OLPCorps","name":"OLPCorps:Madagascar","details":"Students from GWU and U Maryland<br/><br/><a href='http://ampitso.wordpress.com/' target='_blank'>Blog</a>","photo":"http://ampitso.smugmug.com/photos/638764729_UCofq-M.jpg","pt":[-13.57024,49.306641]},
		{"group":"OLPCorps","name":"OLPCorps:Laval University","details":"<br/><br/><a href='http://collabo.fse.ulaval.ca/olpc/' target='_blank'>Website</a>","photo":"http://collabo.fse.ulaval.ca/olpc/images/teach.jpg","pt":[3.387307,12.877007]},
		{"group":"OLPCorps","name":"OLPCorps:Tanzania","details":"Students from Tumaini University.<br/><br/>The school was connected to the internet<br/><br/><a href='http://mot-tumaini.blogspot.com/' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_z6OVkOJNvTQ/SpvI0dyRxGI/AAAAAAAAAO4/ukhEnWkZXEg/s320/IMG0011A.jpg","pt":[-7.794677,35.690117]},
		{"group":"OLPCorps","name":"OLPCorps:Vutakaka","details":"Students from U. Washington and the New School<br/><br/><a href='http://vutakakaolpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://4.bp.blogspot.com/_C_wadBS6-ek/SmX5aiSypyI/AAAAAAAAIzg/XKbSjGgYCoo/s320/100_0057.jpg","pt":[-3.513421,39.835739]},
		{"group":"OLPCorps","name":"OLPCorps:Kampala","details":"Still operating (though not online). Supported by MIT and Wellesley College<br/><br/><a href='http://uganda-olpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://2.bp.blogspot.com/_Sm-Wjgh0ZWk/SlCq2EOvw2I/AAAAAAAAABU/Xm_8bmDF7tY/s320/olpc_kps_10.JPG","pt":[0.29663,32.640381]},
		{"group":"OLPCorps","name":"OLPCorps:GTech","details":"Students from Grahamstown and Gettysburg <a href='http://picasaweb.google.com/aimeegeorge/PicsFromGTECHSouthAfrica?feat=email#' target='_blank'>Photos Page</a><br/><br/><a href='http://gtech-olpc.blogspot.com/' target='_blank'>Blog</a>","photo":"http://lh3.ggpht.com/_7PSu0kxiZPQ/SrrntMYgpLI/AAAAAAAABFY/41saWNP1JNw/s640/P1080072.JPG","pt":[-33.315037,26.548634]},
		{"group":"OLPCorps","name":"OLPCorps:Kwame Nkrumah U.","pt":[7.227441,-0.747414]}]
			for pt in staticdata:
				if(pt.icon==''):
					pt.icon='DEFAULT'
				groupprint = ""
				detailprint = "Please add details to this location"
				if(pt.has_key('group')):
					groupprint = " from " + pt["group"]
				if(pt.has_key('details')):
					detailprint = pt["details"]
				self.response.out.write('		<Placemark>\n			<name><![CDATA[' + pt["name"] + groupprint + ']]></name>\n')
				if(pt.has_key('photo')):
					if(pt.has_key('album')):
						self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + detailprint + '</td><td><a href="' + pt["album"] + '" target="_blank"><img src="' + pt["photo"] + '" style="width:300px;max-height:400px;"/><br/>View Photos</a></td></tr></table>]]></description>\n')
					else:
						self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + detailprint + '</td><td><img src="' + pt["photo"] + '" style="width:300px;max-height:400px;"/></td></tr></table>]]></description>\n')
				else:
					if(pt.has_key('album')):
						self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + detailprint + '</td><td><a href="' + pt["album"] + '" target="_blank">View Photos</a></td></tr></table>]]></description>\n')
					else:
						self.response.out.write('			<description><![CDATA[' + detailprint + ']]></description>\n')
				
				self.response.out.write('''			<Icon><href>http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000</href></Icon>
			<Point>
				<coordinates>''' + str(pt["pt"][1]) + "," + str(pt["pt"][0]) + ''',0</coordinates>
			</Point>
		</Placemark>\n''')
			#ajaxData = [
			#	{name:"OLPC South Carolina",pt:[33.767732,-80.507812],query:"http://olpcMAP.net/json?state=SouthCarolina"},
			#	{name:"OLPC Canada",pt:[55.786613,-98.885193],query:"http://olpcMAP.net/json?country=Canada",icon:"http://lib.store.yahoo.net/lib/yhst-91918294864082/canada-flag.gif"},
			#	{name:"OLPC Australia",pt:[-26.4312,121.6406],query:"http://olpcMAP.net/json?country=Australia"},
			#	{name:"OLE Nepal",pt:[27.3728,85.1897],query:"http://olpcMAP.net/json?country=Nepal"}
			#]
			self.response.out.write('	</Document>\n</kml>')
			return
		else:
			pagePoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
			pageitems = 50
			if(self.request.get('per_page') != ""):
				try:
					pageitems = int(self.request.get('per_page'))
				except:
					pageitems = 50
			if((pageitems > 0) and (pageitems <= 50)):
				# accept lower count per page
				geoPoints = pagePoints.fetch(pageitems,(pagenum-1)*pageitems)
			else:
				# 50 maximum from pagePoints request
				geoPoints = pagePoints.fetch(50,(pagenum-1)*50)
			self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP Page ''' + str(pagenum) + '</name>\n')
		
	if(self.request.get('country') != ""):
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP ''' + cgi.escape(self.request.get('country')) + '</name>\n')
		mapPoints = GeoRefMapPoint.gql("WHERE country = :1 LIMIT 100",self.request.get('country'))
	
	elif(self.request.get('state') != ""):
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP ''' + cgi.escape(self.request.get('state')) + '</name>\n')
		mapPoints = GeoRefMapPoint.gql("WHERE region = :1 LIMIT 100",self.request.get('state'))
	
	elif(self.request.get('center') != ""):
		ctr_lat = None
		ctr_lng = None
		suggestCtr = memcache.get("center:" + cgi.escape(self.request.get('center')))
		if(suggestCtr is not None):
			ctr_lat = suggestCtr.split(",")[0]
			ctr_lng = suggestCtr.split(",")[1]
		else:
			llcenter = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJ&q=" + self.request.get('center'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
			ctr_lat = llcenter[llcenter.find('latitude')+11:len(llcenter)]
			ctr_lat = ctr_lat[0:ctr_lat.find('"')]
			ctr_lng = llcenter[llcenter.find('longitude')+12:len(llcenter)]
			ctr_lng = ctr_lng[0:ctr_lng.find('"')]
			memcache.add("center:" + cgi.escape(self.request.get('center')),ctr_lat + "," + ctr_lng,500000)
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
				GeoRefUsermadeMapPoint.all(),
				geotypes.Point(float(ctr_lat),float(ctr_lng)),
				max_results=100,
				max_distance=1000 * radius)
		hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
				GeoRefMapPoint.all(),
				geotypes.Point(float(ctr_lat),float(ctr_lng)),
				max_results=100,
				max_distance=1000 * radius)
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP near ''' + cgi.escape(self.request.get('center')) + ' ' + ctr_lat + "," + ctr_lng + '</name>\n')
	
	elif(self.request.get('llcenter') != ""):
		ctr_lat = self.request.get('llcenter').replace('%20','').split(',')[0]
		ctr_lng = self.request.get('llcenter').replace('&20','').split(',')[1]
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Point(float(ctr_lat),float(ctr_lng)),
			max_results=100,
			max_distance=1000 * radius)
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP near ''' + ctr_lat + "," + ctr_lng + '</name>\n')
	
	elif(self.request.get('region') != ""):
		ne_lat=None
		ne_lng=None
		sw_lat=None
		sw_lng=None
		suggestRgn = memcache.get("region:" + cgi.escape(self.request.get('region')))
		if(suggestRgn is not None):
			# center was in memcache
			suggestRgn=suggestRgn.split(",")
			ne_lat = suggestRgn[0]
			ne_lng = suggestRgn[1]
			sw_lat = suggestRgn[2]
			sw_lng = suggestRgn[3]
		else:
			llregion = fetch("http://where.yahooapis.com/geocode?appid=M0hEoK7i&flags=CJX&q=" + self.request.get('region'), payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content
			ne_lat = llregion[llregion.find('north')+8:len(llregion)]
			ne_lat = ne_lat[0:ne_lat.find('"')]
			ne_lng = llregion[llregion.find('east')+7:len(llregion)]
			ne_lng = ne_lng[0:ne_lng.find('"')]
			sw_lat = llregion[llregion.find('south')+8:len(llregion)]
			sw_lat = sw_lat[0:sw_lat.find('"')]
			sw_lng = llregion[llregion.find('west')+7:len(llregion)]
			sw_lng = sw_lng[0:sw_lng.find('"')]
			memcache.add("region:" + cgi.escape(self.request.get('region')),ne_lat + "," + ne_lng + "," + sw_lat + "," + sw_lng,500000)
		geoPoints = GeoRefUsermadeMapPoint.bounding_box_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
			GeoRefMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100)
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP within ''' + cgi.escape(self.request.get('region')) + ' ' + ne_lat + "," + ne_lng + ',' + sw_lat + ',' + sw_lng + '</name>\n')
	
	elif(self.request.get('llregion') != ""):
		ne_lat = self.request.get('llregion').replace('%20','').split(',')[0]
		ne_lng = self.request.get('llregion').replace('%20','').split(',')[1]
		sw_lat = self.request.get('llregion').replace('%20','').split(',')[2]
		sw_lng = self.request.get('llregion').replace('%20','').split(',')[3]
		geoPoints = GeoRefUsermadeMapPoint.bounding_box_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		hiddenGeoResults = GeoRefMapPoint.bounding_box_fetch(
			GeoRefMapPoint.all(),
			geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
			max_results=100
		)
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP within ''' + ne_lat + "," + ne_lng + ',' + sw_lat + ',' + sw_lng + '</name>\n')

	
	elif((self.request.get('km-distance') != '') and (self.request.get('id') != '')):
		ctrPoint = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
		radius = float(self.request.get('km-distance'))
		geoPoints = GeoRefUsermadeMapPoint.proximity_fetch(
			GeoRefUsermadeMapPoint.all(),
			geotypes.Point(ctrPoint.location.lat,ctrPoint.location.lon),
			max_results=100,
			max_distance=1000 * radius)
		hiddenGeoResults = GeoRefMapPoint.proximity_fetch(
			GeoRefMapPoint.all(),
			geotypes.Point(ctrPoint.location.lat,ctrPoint.location.lon),
			max_results=100,
			max_distance=1000 * radius)
		self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP near marker ''' + self.request.get('id') + ' ' + str(ctrPoint.location.lat) + ',' + str(ctrPoint.location.lon) + '</name>\n')
	
	existingIcons = {}
	
	if mapPoints is not None:
		results = mapPoints.fetch(200)
		if results is not None:
			for pt in results:
				if(pt.icon==''):
					pt.icon='DEFAULT'
				usename = cgi.escape(pt.name)
				if(usename.find("privatized") != -1):
					fixname = usename.replace("privatized:","")
					sndNames = 0
					outname = ""
					for letter in fixname:
						if(sndNames == 0):
							outname = outname + letter
						elif(sndNames == -1):
							outname = outname + letter
							sndNames = 1
						if(letter == " "):
							sndNames = -1
							outname = outname + " "
					usename = outname
				if(not existingIcons.has_key(pt.icon)):
					existingIcons[pt.icon] = str(pt.key().id())
					self.response.out.write('''		<Style id="style-''' + str(pt.key().id()) + '''">
			<IconStyle>
				<Icon>
					<href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href>
				</Icon>
			</IconStyle>
		</Style>\n''')
				self.response.out.write('''		<Placemark>
			<id>''' + str(pt.key().id()) + '''</id>\n''')
				if(pt.group != ""):
					self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ' from ' + self.linkify(cgi.escape(pt.group or "")).replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + ']]></name>\n')
				else:
					self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ']]></name>\n')
				if(existingIcons.has_key(pt.icon)):
					self.response.out.write('			<styleUrl>#style-' + existingIcons[pt.icon] + '</styleUrl>\n')				
				else:
					self.response.out.write('			<styleUrl>#style-' + str(pt.key().id()) + '</styleUrl>\n')
				self.response.out.write('''			<Icon><href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href></Icon>
			<Point>
				<coordinates>''' + str(pt.location.lon) + ',' + str(pt.location.lat) + ''',0</coordinates>
			</Point>\n''')
				if(pt.photo != ""):
					if(pt.album != ""):
						self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td><div style=\'min-height:220px;\'>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</div></td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank"><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/><br/>View Photos</a></td></tr></table>]]></description>\n')
					else:
						self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td><div style=\'min-height:220px;\'>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</div></td><td><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/></td></tr></table>]]></description>\n')
				elif(pt.album != ""):
					self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank">View Photos</a></td></tr></table>]]></description>\n')			
				else:
					self.response.out.write('			<description><![CDATA[' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + ']]></description>\n')
			self.response.out.write('		</Placemark>\n')
	if geoPoints is not None:
		for pt in geoPoints:
			if((self.request.get('nid')=='true') and (str(pt.key().id()) == self.request.get('id'))):
				continue
			if(pt.icon==''):
				pt.icon='DEFAULT'
			usename = cgi.escape(pt.name)
			if(usename.find("privatized") != -1):
				fixname = usename.replace("privatized:","")
				sndNames = 0
				outname = ""
				for letter in fixname:
					if(sndNames == 0):
						outname = outname + letter
					elif(sndNames == -1):
						outname = outname + letter
						sndNames = 1
					if(letter == " "):
						sndNames = -1
						outname = outname + " "
				usename = outname
			if(not existingIcons.has_key(pt.icon)):
				existingIcons[pt.icon] = str(pt.key().id())
				self.response.out.write('''\n		<Style id="style-''' + str(pt.key().id()) + '''">
			<IconStyle>
				<Icon>
					<href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href>
				</Icon>
			</IconStyle>
		</Style>''')
			self.response.out.write('''		<Placemark>
			<id>''' + str(pt.key().id()) + '''</id>
			<Icon><href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href></Icon>\n''')
			if(pt.group != ""):
				self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ' from ' + self.linkify(cgi.escape(pt.group or "")).replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + ']]></name>\n')
			else:
				self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ']]></name>\n')
			if(existingIcons.has_key(pt.icon)):
				self.response.out.write('			<styleUrl>#style-' + existingIcons[pt.icon] + '</styleUrl>\n')				
			else:
				self.response.out.write('			<styleUrl>#style-' + str(pt.key().id()) + '</styleUrl>\n')
			self.response.out.write('''			<Point>
				<coordinates>''' + str(pt.location.lon) + ',' + str(pt.location.lat) + ''',0</coordinates>
			</Point>\n''')
			if(pt.photo != ""):
				if(pt.album != ""):
					self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td><div style=\'min-height:220px;\'>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</div></td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank"><img src="' + cgi.escape(pt.photo) + '" style="width:300px;max-height:400px;"/><br/>View Photos</a></td></tr></table>]]></description>\n')
				else:
					self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td><div style=\'min-height:220px;\'>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</div></td><td><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/></td></tr></table>]]></description>\n')
			elif(pt.album != ""):
				self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank">View Photos</a></td></tr></table>]]></description>\n')
			else:
				self.response.out.write('			<description><![CDATA[' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + ']]></description>\n')
			self.response.out.write('		</Placemark>\n')
	if hiddenGeoResults is not None:
		for pt in hiddenGeoResults:
			if((self.request.get('nid')=='true') and (str(pt.key().id()) == self.request.get('id'))):
				continue
			if(pt.icon==''):
				pt.icon='DEFAULT'
			usename = cgi.escape(pt.name)
			if(usename.find("privatized") != -1):
				fixname = usename.replace("privatized:","")
				sndNames = 0
				outname = ""
				for letter in fixname:
					if(sndNames == 0):
						outname = outname + letter
					elif(sndNames == -1):
						outname = outname + letter
						sndNames = 1
					if(letter == " "):
						sndNames = -1
						outname = outname + " "
				usename = outname
			if(not existingIcons.has_key(pt.icon)):
				existingIcons[pt.icon] = str(pt.key().id())
				self.response.out.write('''		<Style id="style-''' + str(pt.key().id()) + '''">
			<IconStyle>
				<Icon>
					<href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href>
				</Icon>
			</IconStyle>
		</Style>\n''')
			self.response.out.write('''		<Placemark>
			<id>''' + str(pt.key().id()) + '''</id>
			<Icon><href>''' + pt.icon.replace('https','http').replace('DEFAULT','http://chart.apis.google.com/chart?chst=d_map_pin_icon&amp;chld=location%7CFF0000') + '''</href></Icon>\n''')
			if(pt.group != ""):
				self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ' from ' + self.linkify(cgi.escape(pt.group or "")).replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + ']]></name>\n')
			else:
				self.response.out.write('			<name><![CDATA[' + cgi.escape(usename) + ']]></name>\n')
			if(existingIcons.has_key(pt.icon)):
				self.response.out.write('			<styleUrl>#style-' + existingIcons[pt.icon] + '</styleUrl>\n')				
			else:
				self.response.out.write('			<styleUrl>#style-' + str(pt.key().id()) + '</styleUrl>\n')
			self.response.out.write('''			<Point>
				<coordinates>''' + str(pt.location.lon) + ',' + str(pt.location.lat) + ''',0</coordinates>
			</Point>\n''')
			if(pt.photo != ""):
				if(pt.album != ""):
					self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank"><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/><br/>View Photos</a></td></tr></table>]]></description>\n')
				else:
					self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><img src="' + cgi.escape(pt.photo).replace('"','\\"') + '" style="width:300px;max-height:400px;"/></td></tr></table>]]></description>\n')
			elif(pt.album != ""):
				self.response.out.write('			<description><![CDATA[<table class=\'kml\'><tr><td>' + cgi.escape(self.linkify(pt.details)).replace('"','\'').replace("&lt;","<").replace("&gt;",">") + '</td><td><a href="' + cgi.escape(pt.album).replace('"','\\"') + '" target="_blank">View Photos</a></td></tr></table>]]></description>\n')			
			else:
				self.response.out.write('			<description><![CDATA[' + cgi.escape(self.linkify(pt.details)).replace('"','\\"').replace("&lt;","<").replace("&gt;",">") + ']]></description>\n')
			self.response.out.write('		</Placemark>\n')
	self.response.out.write('''	</Document>
</kml>''')

class ShareMain(webapp.RequestHandler):
  def post(self):
	myLink = None
	if(self.request.get('news') != ''):
		myLink = GeoNewsItem(location=self.request.get('scope'))
		myLink.update_location()
	else:
		myLink = SearchLink()
	myLink.sharer = self.request.get('email')
	myLink.href = self.request.get('link')
	myLink.title = self.request.get('artname')
	myLink.geoscope = self.request.get('scope')
	myLink.put()
	
	tags = self.request.get('tags').lower().replace(',',' ').replace('.',' ').replace('%20',' ').replace('  ',' ').split(' ')
	for tag in tags:
		myTag = SearchTag.gql("WHERE term = :1", tag).get()
		if(myTag is not None):
			# add to existing tag
			myTag.tagLinks.append(str(myLink.key().id()))
		else:
			# new tag
			myTag = SearchTag()
			myTag.term = tag
			myTag.tagLinks = [str(myLink.key().id())]
		myTag.put()
	self.redirect('http://mapmeld.appspot.com/olpcMAPolpc/share?posted=posted')

  def get(self):
	isNews = 0
	if(self.request.url.find('news')!=-1):
		isNews = 1
	self.response.out.write('''<!DOCTYPE html>
<html>
<head id="head">
	<title>Shared @ olpcMAP</title>
	<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
	<script type='text/javascript'>
function contactMode(){
	$("coverwindow").style.display="block";
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function searchOpt(){
	var sScript=document.createElement("script");
	sScript.src="http://mapmeld.appspot.com/olpcMAP/search?q=" + $("searchCheck").value;
	sScript.type="text/javascript";
	$("head").appendChild(sScript);
}
function keyGoes(evt){
	if(event!=null){
		if(event.keyCode==13){
			searchOpt();
		}
	}
}
function writeSearchCat(category,resultsList){
	if(resultsList.length==0){return ""}
	var searchCat='<ul class="searchList">';
	for(var sR=0;sR<resultsList.length;sR++){
		var provenName=resultsList[sR].name;
		while(provenName.indexOf("<")!=-1){
			provenName=provenName.replace("<","&lt;");
		}
		if(resultsList[sR].href){
			searchCat+='<li onclick="searchAccept('+"'"+resultsList[sR].acceptance+"'"+')">' + provenName + ' <a href="' + resultsList[sR].href + '" target="_blank">(Link)</a><br/>Shared by <a href="#">' + resultsList[sR].sharer + '</a></li>';
		}
		else{
			searchCat+='<li onclick="searchAccept('+"'"+resultsList[sR].acceptance+"'"+')">' + provenName + '</li>';
		}
	}
	searchCat+="</ul>"
	return searchCat;
}
function $(id){return document.getElementById(id);}
	</script>
	<style type='text/css'>
	<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:white;}
div.main{
	background-color:silver;
	border-left:1px solid #000000;
	border-right:1px solid #000000;
}
span.navoption a{
	color:#000000;
	text-decoration:none;
}
span.navoption a:hover{
	color:#0000bb;
	text-decoration:underline;
}
span.navoption:hover{
	color:#0000bb;
	text-decoration:underline;
}
a.tab{
	font-size:11pt;
	margin-left:8px;
	margin-right:8px;
	font-weight:normal;
}
a.tab-select{
	text-decoration:none;
	color:#500;
	font-weight:bold;
	margin-left:8px;
	margin-right:8px;
}
h4{
	margin-top:20pt;
}
div.mapdesc{
	min-height:200px;
}
button.submit{
	background: transparent url(http://mapmeld.appspot.com/bg_submit-report.png) repeat-x;
	border: solid #208A08;
	border-bottom: none;
	padding: 9px 12px 9px 12px;
}
ul.searchlist{
	width:90%;
	margin-left:5%;
	margin-right:5%;
	padding-top:30px;
	padding-bottom:30px;
	background-color:#cccccc;
}
ul.searchList li{
	padding:4px;
	margin-bottom:4px;
	border-bottom:1px solid black;
}
ul.searchList li:hover{
	background-color:#ffffff;
}
input.tform{
	font-size:14pt;
	padding:4px;
}
h3{
	margin-bottom:0.5em;
}
	</style>
</head>
<body>
	<div class="header">
		<h3><span style='font-size:1.7em;'>olpcMAP.net</span> geo-social network for the XO, Sugar, and ICT4E</h3>
		<br/>
	</div>
	<div class="nav" style="border-bottom:1px solid black;">
		<span class="navoption"><a href="http://olpcMAP.net/map">Live Map</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">Laptop Help</a></span>
		<span class="navoption"><a href="http://mapmeld.appspot.com/olpcMAP/community">Community-made Maps</a></span>
		<span class="navoption"><a href="#" onclick="contactMode()">Contact</a></span>
	</div>
	<div class="main" style="padding-top:20px;">
		<br/><br/>\n''')
	if(isNews == 0):
		self.response.out.write('		<span>Share best links for a topic (Sugar, solar, Somalia) to guide olpcMAP volunteers and deployments</span><br/>\n')
	else:
		self.response.out.write('		<span>Share news stories and geolocate them for our map</span><br/>\n')
	self.response.out.write('''		<span>Verify via e-mail to add them to olpcMAP search results</span>
		<br/><br/>
		<h4 style="color:#000000;">Shared @ olpcMAP</h4>
		<table><tr><td>
			<div style="background-color:white;padding:12px;border:2px solid blue;cursor:pointer;text-align:center;min-width:200px;">
				<h4>Search the "Shared @ olpcMAP" articles</h4>		
				<input id="searchCheck" type="text" style="padding-left:10px;padding-right:10px;margin:12px;font-size:15pt;min-width:200px;font-family:Arial,sans-serif;font-size:15pt;vertical-align:middle;" size="20" onkeypress="keyGoes(event);"/>
				<button onclick="searchOpt();" style="font-size:15pt;">
					<img src="http://sites.google.com/site/olpcau/home/Bluesmall.png" style="vertical-align:middle;"/>
					<span style="vertical-align:middle;">Search</span>
				</button>
			</div>
			<div id="olpcMAPsr" style="height:570px;">
			</div>
		</td><td>
			<form id="olpcMAPentry" style="max-width:350px;border:2px solid black;padding-left:10px;background-color:#cccccc;" action="http://mapmeld.appspot.com/olpcMAPolpc/share" method="POST">
				<h4>Your Name on olpcMAP</h4>
				<input class="tform" name="email" size="25" width="300"/><br/>
				<h4>Share a link URL</h4>
				<input class="tform" name="link" size="25" width="300"/><br/>
				<h4>Name of the article</h4>
				<input class="tform" name="artname" size="25" width="300"/><br/>\n''')
	if(isNews == 0):
		self.response.out.write('''				<h4>Geographic Scope (country or region name)</h4>
				<input class="tform" name="scope" size="25" width="300"/><br/>\n''')
	else:
		self.response.out.write('''				<h4>Geotag (latitude,longitude)</h4>
				<input class="tform" name="scope" size="25" width="300"/><br/>
				<input type="hidden" name="news" value="true"/>\n''')
	self.response.out.write('''				<h4>Tags (separate with spaces or commas)</h4>
				<input class="tform" name="tags" size="25" width="300"/><br/>
				<hr/>
				<h4><input type="submit" value="Submit Links"/></h4>
			</form>
		</td></tr></table>
	</div>
	<div id="coverwindow" style="display:none;position:fixed;margin-left:300px;top:100px;border:1px solid black;font-size:16pt;text-align:right;background-color:#333333;">
		<input type="button" value="X" style="border:1px solid black;color:black;font-size:16pt;" onclick="closeCoverWindow();"/>
		<br/>
		<form id="signinform" style="width:100%;background-color:#ffffff; text-align:left; font-size:13pt;" action="http://mapmeld.appspot.com/olpcMAP/contact?id=you" method="POST">
			E-mail <input id="emaillogin" name="login"/><br/>
			<!--Password <input id="passwordlogin" type="password" name="password"/><hr/>-->
			Message<br/><textarea name="message" width="300"></textarea>
			<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Send"/>
		</form>
		<div id="infoform"></div>
	</div>
</body>
</html>''')

class Search(webapp.RequestHandler):
  def get(self):
	self.response.out.write(self.snap(self.request.get('q')))

  def snap(self,q):
	q = q.lower()
	response=""
	if(q.find('addbatch') != -1):
		# add batch of tags and results at once here
		mnLink = SearchLink()
		#mnLink.title = "Ntugi School Solar"
		#mnLink.href = "http://www.olpcnews.com/countries/canada/canadian_kenyan_schools_solar_power.html"
		#mnLink.sharer = "Mark Battley"
		#mnLink.geoscope = "Kenya"
		#mnLink.put()
		#af = SearchTag()
		#af.term = "solar"
		#af.tagLinks = [str(mnLink.key().id())]
		#af.put()
		#rg = SearchTag()
		#rg.term = "power"
		#rg.tagLinks = [str(mnLink.key().id())]
		#rg.put()
	else:
		response=response+'omList=[];'
		try:
			# divide the search into individual terms
			q = q.replace(',',' ').replace('.',' ').replace('-',' ').replace('%20',' ').replace('  ',' ')
			foundTerms=[]
			if(q.find(' ')==-1):
				q = [q]
			else:
				q = q.split(' ')
			for qword in q:
				# locate tags for each individual term term
				tag = SearchTag.gql("WHERE term = :1", qword).get()
				if tag is not None:
					for res in tag.tagLinks:
						prevTerm = 0
						for prevTerm in foundTerms:
							if(prevTerm == res):
								prevTerm = -2
								break
						if(prevTerm != -2):
							# if not previously added to results, add into results
							foundTerms.append(res)
							link = SearchLink.get_by_id(long(res))
							response=response+('omList.push({name:"' + cgi.escape( link.title) + '",acceptance:"geoq ' + cgi.escape(link.geoscope.replace(","," ")) + '",href:"' + link.href.replace('"','') + '",sharer:"' + cgi.escape(link.sharer) + '"});')
			# once done listing results, add to search results div
			response=response+('$("olpcMAPsr").innerHTML=writeSearchCat("Shared @ olpcMAP <a href=\'http://mapmeld.appspot.com/olpcMAPolpc/share\' target=\'_blank\'><img src=\'http://mapmeld.appspot.com/plusIcon.gif\' height=\'13\' width=\'13\' style=\'vertical-align:middle;\' alt=\'Add\'/></a>",omList);')
		except:
			response=response+''
	return response

class SearchLink(db.Model):
	title = db.StringProperty()
	href = db.StringProperty()
	sharer = db.StringProperty()
	geoscope = db.StringProperty()

class SearchDoc(SearchLink):
	authors = db.StringProperty()

class SearchTag(db.Model):
	term = db.StringProperty()
	tagLinks = db.StringListProperty()

class Oldest(webapp.RequestHandler):
  def get(self):
	self.snap()

  def snap(self):
	mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate ASC")
	results = mapPoints.fetch(220)
	resultOut=u''
	for pt in results:
		resultOut = resultOut + u'p({name:"'
		usename = cgi.escape(pt.name)
		if(usename.find("privatized") != -1):
			fixname = usename.replace("privatized:","")
			sndNames = 0
			outname = ""
			for letter in fixname:
				if(sndNames == 0):
					outname = outname + letter
				elif(sndNames == -1):
					outname = outname + letter
					sndNames = 1
				if(letter == " "):
					sndNames = -1
					outname = outname + " "
			usename = outname
		resultOut = resultOut + cgi.escape(usename).replace('"','\\"') + u'",id:"' + str(pt.key().id()) + u'",pt:[' + str(pt.location.lat) + "," + str(pt.location.lon) + u'],icon:"' + cgi.escape(pt.icon or "") + u'",details:"'
		resultOut = resultOut + cgi.escape(pt.details or "").replace('"','\\"').replace("&lt;","<").replace("&gt;",">").replace('\\n','<br/>').replace('\\r','<br/>').replace('\n','<br/>').replace('\r','<br/>') + '"'
		if(pt.tabs is not None):
			resultOut = resultOut + u',tabs:["' + '","'.join(pt.tabs) + '"]'
		resultOut = resultOut + u',photo:"' + cgi.escape(pt.photo or "").replace('"','\\"') + u'",album:"' + cgi.escape(pt.album or "").replace('"','\\"') + u'",group:"' + cgi.escape(pt.group or "").replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + u'",icon:"' + cgi.escape(pt.icon or "") + u'"});\n'
	memcache.set('oldPoints',resultOut,48*60*60)
	return resultOut

class ResetPoint(webapp.RequestHandler):
  def get(self):
	pt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
	if pt is None:
		self.redirect('http://olpcMAP.net')
	self.response.out.write('''<!DOCTYPE html>
<html>
<head>
	<title>olpcMAP: Reset Name and Location</title>
	<meta name="viewport" content="initial-scale=1.0,user-scalable=no" />
	<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
	<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
	<script type="text/javascript">
var myPoints,isEditor,lastOpen;
function init(){
	var myOptions = {
		zoom:12,
		scaleControl:true,
		center:new google.maps.LatLng(''' + str(pt.location.lat) + "," + str(pt.location.lon) + '''),
		streetViewControl:false,
		mapTypeId:google.maps.MapTypeId.TERRAIN,
		mapTypeControlOptions:{mapTypeIds:[google.maps.MapTypeId.TERRAIN,google.maps.MapTypeId.ROADMAP,google.maps.MapTypeId.SATELLITE, 'OSM']}
	};
	defSize=new google.maps.Size(42,42);
	map = new google.maps.Map($("map"),myOptions);
	var osmMapLayer = new google.maps.ImageMapType({
		getTileUrl: function(coord, zoom) {
			return "http://tile.openstreetmap.org/" +
			zoom + "/" + coord.x + "/" + coord.y + ".png";
		},
		tileSize: new google.maps.Size(256, 256),
		isPng: true,
		alt: "OSM",
		name: "OSM",
		maxZoom: 19
	});
	map.mapTypes.set('OSM',osmMapLayer);
	myPoints=[{name:"''')
	usename = cgi.escape(pt.name)
	if(usename.find("privatized") != -1):
		fixname = usename.replace("privatized:","")
		sndNames = 0
		outname = ""
		for letter in fixname:
			if(sndNames == 0):
				outname = outname + letter
			elif(sndNames == -1):
				outname = outname + letter
				sndNames = 1
			if(letter == " "):
				sndNames = -1
				outname = outname + " "
		usename = outname	
	resultOut = cgi.escape(usename).replace('"','\\"') + u'",id:"' + str(pt.key().id()) + u'",pt:[' + str(pt.location.lat) + "," + str(pt.location.lon) + u'],icon:"' + cgi.escape(pt.icon or "") + u'",details:"'
	resultOut = resultOut + cgi.escape(pt.details or "").replace('"','\\"').replace("&lt;","<").replace("&gt;",">").replace('\\n','<br/>').replace('\\r','<br/>').replace('\n','<br/>').replace('\r','<br/>') + '"'
	if(pt.tabs is not None):
		resultOut = resultOut + u',tabs:["' + '","'.join(pt.tabs) + '"]'
	resultOut = resultOut + u',photo:"' + cgi.escape(pt.photo or "").replace('"','\\"') + u'",album:"' + cgi.escape(pt.album or "").replace('"','\\"') + u'",group:"' + cgi.escape(pt.group or "").replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + u'",icon:"' + cgi.escape(pt.icon or "") + u'"}];\n'
	self.response.out.write(resultOut + '''	infoWindow = new google.maps.InfoWindow();
	var myPt=0;
	var marker;
	google.maps.event.addListener(map,'click',function(){if(!isEditor){infoWindow.close()}});
	if(myPoints[myPt].icon.toLowerCase().indexOf("default") != -1){
		myPoints[myPt].icon="";
	}
	if(myPoints[myPt].icon.length > 6){
		marker=new google.maps.Marker({
			position:new google.maps.LatLng(myPoints[myPt].pt[0],myPoints[myPt].pt[1]),
			map:map,
			icon:new google.maps.MarkerImage(myPoints[myPt].icon,defSize),
			title:myPoints[myPt].name,
			draggable:true
		});
	}
	else{
		var myRandIcon=randIcon();
		marker=new google.maps.Marker({
			position:new google.maps.LatLng(myPoints[myPt].pt[0],myPoints[myPt].pt[1]),
			map:map,
			icon:new google.maps.MarkerImage(myRandIcon,defSize),
			title:myPoints[myPt].name,
			draggable:true
		});
	}
	if(!myPoints[myPt].group){myPoints[myPt].group="";}
	myPoints[myPt].marker=marker;
	contentString=setupContent(myPt);
	addInfo(marker,contentString);
}
function randIcon(){
	var randIcon;
	var randIconI=Math.floor(Math.random()*18);
	switch(randIconI){
		case 0:
			randIcon="http://google-maps-icons.googlecode.com/files/computer.png";
			break;
		case 1:
			randIcon="http://google-maps-icons.googlecode.com/files/world.png";
			break;
		case 2:
			randIcon="http://google-maps-icons.googlecode.com/files/industrialmuseum.png";
			break;
		case 3:
			randIcon="http://google-maps-icons.googlecode.com/files/music-classical.png";
			break;
		case 4:
			randIcon="http://google-maps-icons.googlecode.com/files/postal.png";
			break;
		case 5:
			randIcon="http://google-maps-icons.googlecode.com/files/housesolarpanel.png";
			break;
		case 6:
			randIcon="http://google-maps-icons.googlecode.com/files/park.png";
			break;
		case 7:
			randIcon="http://google-maps-icons.googlecode.com/files/laboratory.png";
			break;
		case 8:
			randIcon="http://google-maps-icons.googlecode.com/files/university.png";
			break;
		case 9:
			randIcon="http://google-maps-icons.googlecode.com/files/daycare.png";
			break;
		case 10:
			randIcon="http://google-maps-icons.googlecode.com/files/school.png";
			break;
		case 11:
			randIcon="http://google-maps-icons.googlecode.com/files/bookstore.png";
			break;
		case 12:
			randIcon="http://google-maps-icons.googlecode.com/files/workoffice.png";
			break;
		case 13:
			randIcon="http://google-maps-icons.googlecode.com/files/photo.png";
			break;
		case 14:
			randIcon="http://google-maps-icons.googlecode.com/files/bigcity.png";
			break;
		case 15:
			randIcon="http://google-maps-icons.googlecode.com/files/places-unvisited.png";
			break;
		case 16:
			randIcon="http://google-maps-icons.googlecode.com/files/amphitheater-tourism.png";
			break;
		case 17:
			randIcon="http://google-maps-icons.googlecode.com/files/flowers.png";
			break;
	}
	return randIcon;
}
function nameEdited(){
	myPoints[0].name = $("nameEditor").value;
	infoWindow.close();
	contentString=setupContent(0);
	addInfo(marker,contentString);
}
function setupContent(mIndex){
	var markerData = myPoints[mIndex];
	var contentString;
	if(markerData.name==""){markerData.name="unnamed"}
	contentString='<input id="nameEditor" mid="'+markerData.id+'" style="font-size:12pt;" value="'+markerData.name+'"/>';
	var titles="";
	contentString+="<a class='tab' href='#' onclick='nameEdited();'>Save</a></h4>";
	//contentString+="<img src='http://mapmeld.appspot.com/plusIcon.gif' style='vertical-align:middle;margin-left:3px;' onclick='addTab("+mIndex+")'/>";
	contentString+="<div id='infoWindow-2' style='min-height:180px;'><table><tr>";
	var width="250";
	if(!markerData.photo){
		width="450";
	}
	contentString += "<td style='font-size:8pt;' width='"+width+"'>";
	if((markerData.group) && (markerData.group.length > 1)){
		contentString += "<span style='font-weight:bold'>From "+linkify(markerData.group)+"</span>";
	}
	contentString+="<hr/>";
	if(markerData.details){contentString += linkify(markerData.details)}
	else{contentString+="Please help us add details to this location"}
	contentString+="</td>";
	if(markerData.photo){
		if(markerData.album){
			contentString+="<td><div id='mediadiv'><a href='"+markerData.album+"' target='_blank'><img src='"+markerData.photo+"' style='max-height:150px;max-width:260px;' alt='BestPhoto'/><br/>View Photos</a></div></td>";		
		}
		else{
			contentString+="<td><div id='mediadiv'><img src='"+markerData.photo+"' style='max-height:150px;max-width:260px;'/></div></td>";
		}
	}
	else{
		if(markerData.album){
			contentString+="<td width='30pt'><a href='"+markerData.album+"' target='_blank'>View Photos</a></td>";
		}
		else{
			contentString+="<td width='10'></td>";
		}
	}
	contentString+="</tr></table></div>";
	contentString+="<div id='infoWindow-0' style='display:none;min-height:180px;'></div>";
	contentString+="<div id='infoWindow-1' style='display:none;min-height:180px;'><iframe id='infoWindow-contact' src='' style='border:none;' height='300' width='400'></iframe></div>";
	if(markerData.tabs){
		for(var mt=0;mt<markerData.tabs.length;mt++){
			contentString+="<div id='infoWindow-"+(mt*1+3)+"' style='display:none;min-height:180px;'></div>";
			contentString+="<div id='infoWindow-"+(mt*1+3)+"' style='display:none;min-height:180px;'><iframe id='infoFrame-"+(mt*1+3)+"' src='' style='border:none;' height='300' width='400'></iframe></div>";
		}
	}
	return contentString;
}
function linkify(unlinkedTxt){
	unlinkedTxt=replaceEach(unlinkedTxt,"Link:","link:");
	unlinkedTxt=replaceEach(unlinkedTxt,"link:"," link;");
	unlinkedTxt=replaceEach(unlinkedTxt," link;"," link:");	
	while(unlinkedTxt.indexOf("link:") != -1){
		linkUrl=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5,unlinkedTxt.length);
		linkAfter='';
		if(linkUrl.indexOf(" ")!=-1){
			linkUrl=linkUrl.substring(0,linkUrl.indexOf(" "));
			linkAfter=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5+linkUrl.length);
		}
		else if(linkUrl.indexOf("link:")!=-1){
			linkUrl=linkUrl.substring(0,linkUrl.indexOf("link:"));
			linkAfter=unlinkedTxt.substring(unlinkedTxt.indexOf("link:")+5+linkUrl.length);
		}
		if(linkUrl.indexOf("http")==-1){
			linkUrl="http://"+linkUrl;
		}
		unlinkedTxt=unlinkedTxt.substring(0,unlinkedTxt.indexOf("link:")) + "<a target='_blank' href='" + linkUrl + "'>" + linkUrl + "</a>" + linkAfter;
	}
	return unlinkedTxt;
}
function replaceEach(src,older,newer){
	while(src.indexOf(older)!=-1){
		src=src.replace(older,newer);
	}
	return src;
}
function addInfo(m,content){
	google.maps.event.clearInstanceListeners(m);
	google.maps.event.addListener(m,'click',function(){
		lastOpen=m;
		infoWindow.setContent(content);
		infoWindow.open(map,m);
	});
}
function clickToConfirm(){
	window.location="http://mapmeld.appspot.com/olpcMAP/makePoint?newname="+myPoints[0].name+"&id=" + myPoints[0].id + "&point=" + myPoints[0].marker.getPosition().lat() + "," + myPoints[0].marker.getPosition().lng() + "&cmd=email";
}
function $(id){return document.getElementById(id)}
	</script>
	<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:white;}
input{color:#000;}
h3{
	margin-bottom:0.5em;
}
button{
	vertical-align:middle;
	font-family:Arial,sans-serif;
	font-size:14px;
	font-weight:bold;
	padding:4px;
	color:#000000;
}
div.main{
	background-color:#DDDAA0;
}
span.navoption{
	color:#000000;
	text-decoration:none;
}
span.navoption a{
	color:#000000;
	text-decoration:none;
}
span.navoption:hover{
	color:#0000bb;
	text-decoration:underline;
}
span.navoption a:hover{
	color:#0000bb;
	text-decoration:underline;
}
a.tab{
	font-size:11pt;
	margin-left:8px;
	margin-right:8px;
	font-weight:normal;
}
a.tab-select{
	text-decoration:none;
	color:#500;
	font-weight:bold;
	margin-left:8px;
	margin-right:8px;
}
div.searchCat{
	background-color:#aaaaaa;
	font-weight:bold;
	padding:5px;
}
ul.searchList li{
	list-style-type:circle;
	font-size:10pt;
	padding:4px;
	margin-bottom:1px;
	cursor:pointer;
}
ul.searchList li:hover{
	background-color:#ccdddd;
}
span.topResult{
	font-size:11pt;
	background-color:#ccdddd;
}
li.prof{
	font-family:Arial,sans-serif;
	font-size:14px;
	border-bottom:1px solid black;
	cursor:pointer;
	padding:6px;
	list-style-type:square;
	margin-left:-30px;
	background-color:#aaaaff;
}
li.prof:hover{
	background-color:blue;
}
label{
	width:100%;
	margin-top:10px;
}
div.sBar{
  margin-top:-20px;
  -moz-box-shadow: 15px 15px 15px #ccc;
  -webkit-box-shadow: 15px 15px 15px #ccc;
  box-shadow: 15px 15px 15px #ccc;
}
	</style>
</head>
<body onload="init();">
	<div class="header">
		<h3><span style='font-size:1.7em;'>olpcMAP</span> - a geosocial network for Sugar and the XO <a href="http://www.facebook.com/pages/OlpcMAP/126840500716047" style="margin-left:8px;" target="_blank"><img src="http://facebook.com/favicon.ico" alt="Facebook Page" title="Facebook Page" style="height:16pt;"/></a><a href="http://twitter.com/olpcmap" style="margin-left:8px;" target="_blank"><img src="http://twitter.com/favicon.ico" title="Twitter Feed" alt="Twitter Feed" style="height:16pt;"/></a></h3>
		<noscript><h3>Enable JavaScript to view olpcMAP</h3></noscript>
		<br/>
	</div>
	<div class="nav" style="border-bottom:1px solid black;">
		<span class="navoption"><a href="#" onclick="joinNetworkMode();">Join the Map Network</a></span>
		<span class="navoption"><a href="http://olpcMAP.net/home" target="_blank">Homepage</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/" target="_blank">Laptop Help</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">About Map</a></span>
		<span class="navoption"><a href="#" onclick="contactMode()">Contact</a></span>
	</div>
	<div id="main" class="main" style="height:28px;min-height:30px;background-color:black;color:white;margin-left:auto;margin-right:auto;text-align:center;padding-top:10px;">
		Drag the marker to a new location | Click the marker to edit its name |
		<a href="#" onclick="clickToConfirm()" style="display:inline;">
			Click to confirm by e-mail
		</a>.
	</div>
	<div id="map" style="height:80%;width:100%;margin:0px;padding:0px;"></div>
	<div id="coverwindow" style="display:none;position:fixed;margin-left:auto;margin-right:auto;top:100px;border:1px solid black;font-size:16pt;text-align:right;background-color:#333333;">
		<input type="button" value="X" style="border:1px solid black;color:black;font-size:16pt;" onclick="closeCoverWindow();"/>
		<br/>
		<form id="signinform" style="width:100%;background-color:#ffffff; text-align:left; font-size:13pt;" action="http://mapmeld.appspot.com/olpcMAP/contact?id=you" method="POST">
			E-mail <input id="emaillogin" name="login"/><br/>
			<!--Password <input id="passwordlogin" type="password" name="password"/><hr/>-->
			Message<br/><textarea name="message" width="550" height="300"></textarea>
			<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Send"/>
		</form>
	</div>
</body>
</html>''')

class MapImage(webapp.RequestHandler):
  def get(self):
	if(self.request.get('frame')=='i'):
		self.response.out.write('''<form action="http://mapmeld.appspot.com/olpcMAPimg/post" method="POST" enctype="multipart/form-data">
	<input id='editorPhotoUpload' type='file' name='img' enctype='multipart/form-data'/>
	<input name='ekey' type='hidden' value="''' + self.request.get('ekey') + '''"/>
	<input type='submit' value='&rarr;Upload'/>
</form>''')
	elif(self.request.get('frame')=='show'):
		self.response.out.write('http://mapmeld.appspot.com/olpcMAPimg?pic=' + self.request.get('pic'))
	else:
		callphoto = PhotoUpload.get_by_id(int(self.request.get('pic')))
		if callphoto is not None:
			if(callphoto.redirectUrl == ''):
				self.response.headers['Content-Type'] = "image/jpeg"
				self.response.out.write(callphoto.photo)
			else:
				# photo has been moved to flickr or something to save space locally
				self.redirect(callphoto.redirectUrl)
		else:
			#no photo found
			self.response.out.write('')
  def post(self):
	imgdata = self.request.get('img')
	upload = PhotoUpload()
	upload.redirectUrl = ''
	upload.photo = db.Blob(str(imgdata))
	upload.ekey = self.request.get('ekey')
	logging.info('ekey ' + self.request.get('ekey'))
	upload.put()
	self.redirect('http://mapmeld.appspot.com/olpcMAPimg?frame=show&pic=' + str(upload.key().id()))

class Newest(webapp.RequestHandler):
  def get(self):
	self.snap()
  def snap(self):
	mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate ASC")
	results = mapPoints.fetch(220,220)
	resultOut=u''
	for pt in results:
		resultOut = resultOut + u'pS({name:"'
		usename = cgi.escape(pt.name)
		if(usename.find("privatized") != -1):
			fixname = usename.replace("privatized:","")
			sndNames = 0
			outname = ""
			for letter in fixname:
				if(sndNames == 0):
					outname = outname + letter
				elif(sndNames == -1):
					outname = outname + letter
					sndNames = 1
				if(letter == " "):
					sndNames = -1
					outname = outname + " "
			usename = outname
		resultOut = resultOut + cgi.escape(usename).replace('"','\\"') + u'",id:"' + str(pt.key().id()) + u'",pt:[' + str(pt.location.lat) + "," + str(pt.location.lon) + u'],icon:"' + cgi.escape(pt.icon or "") + u'",details:"'
		resultOut = resultOut + cgi.escape(pt.details or "").replace('"','\\"').replace("&lt;","<").replace("&gt;",">").replace('\\n','<br/>').replace('\\r','<br/>').replace('\n','<br/>').replace('\r','<br/>') + '"'
		if(pt.tabs is not None):
			resultOut = resultOut + u',tabs:["' + '","'.join(pt.tabs) + '"]'
		resultOut = resultOut + u',photo:"' + cgi.escape(pt.photo or "").replace('"','\\"') + u'",album:"' + cgi.escape(pt.album or "").replace('"','\\"') + u'",group:"' + cgi.escape(pt.group or "").replace('"','\\"').replace("&lt;a","<a").replace("&lt;/a","</a").replace("&gt;",">") + u'",icon:"' + cgi.escape(pt.icon or "") + u'"});\n'
	memcache.set('newPoints',resultOut,48*60*60)
	return resultOut

class MakePoint(webapp.RequestHandler):
  def get(self):
	pt = None
	try:
		pt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
	except:
		try:
			pt = MapPoint.get_by_id(long(self.request.get('id')))
		except:
			pt = GeoRefUsermadeMapPoint(location=self.request.get('point'))
			if(self.request.get('mail') == ''):
				pt.creator = users.get_current_user()
			elif(self.request.get('mail') == 'null'):
				pt.creator = users.User("suggestEdit@mapmeld.com")
			else:
				pt.creator = users.User(self.request.get('mail'))
	if(self.request.get('cmd')=='loc'):
		pt.location = self.request.get('point')
		pt.update_location()
		pt.put()
		return
	if(self.request.get('cmd')=='email'):
		thisMail = EmailConfirm()
		thisMail.ekey = str(random.randint(100000,1000000))
		thisMail.mlocation = self.request.get('point')
		thisMail.mname = self.request.get('newname')
		thisMail.mid = str(pt.key().id())
		thisMail.put()
		email = pt.email
		if(pt.email == 'null'):
			email = pt.creator.email()
		if(pt.cc is not None):
			email = email + ";" + pt.cc
		mail.send_mail(sender="beautify@olpcMAP.net",
			to=email,
			subject="olpcMAP : Rename or Move Marker?",
			body='Hi ! This is a message from olpcMAP.net.\n\nSomeone asked us to move your marker and/or change its name.  You can CONFIRM by clicking this link: http://olpcMAP.net/confirm?id=' + str(thisMail.key().id()) + '&key=' + thisMail.ekey + "\n\n You can see a preview of where the marker will be: http://olpcMAP.net?q=" + thisMail.mlocation + " \n\n If you don't want to move the marker, just delete this e-mail.\n\n Thanks!\nolpcMAP Team")
		self.redirect('http://mapmeld.appspot.com/olpcMAPolpc/home')
		return
	pt.name = self.request.get('name')
	pt.details = db.Text(self.request.get('details').replace('~26','&'))
	pt.group = self.request.get('group')
	if(self.request.get('ekey')!=''):
		logging.info('checking ekey ' + self.request.get('ekey'))
		uploaded = PhotoUpload.gql('WHERE ekey = :1', self.request.get('ekey')).get()
		if(uploaded is not None):
			logging.info('matching ekey')
			pt.photo = "http://mapmeld.appspot.com/olpcMAPimg?pic=" + str(uploaded.key().id())
			self.response.out.write('myPoints[sendPtIndex].photo="'+pt.photo+'";')
		else:
			logging.info('no match')
			pt.photo=""
	else:
		logging.info('no ekey')
		pt.photo = self.request.get('photo')
	pt.photo = self.request.get('photo')
	pt.album = self.request.get('album')
	pt.icon = self.request.get('icon')
	pt.email = self.request.get('mail')
	pt.tabs = []
	pt.update_location()
	pt.put()
	# send ID back to creator
	self.response.out.write('try{myPoints[sendPtIndex].id="' + str(pt.key().id()) + '";}catch(e){identifyNewMarker("' + str(pt.key().id()) + '")}')

class EmailConfirming(webapp.RequestHandler):
  def get(self):
	confirm = EmailConfirm.gql("WHERE ekey = :1", cgi.escape(self.request.get('key'))).get()
	if confirm is not None:
		if(self.request.get('id') != str(confirm.key().id())):
			self.response.out.write('Confirmation code or ID did not match')
			return
	else:
		self.response.out.write('Confirmation code or ID did not match')		
		return
	pt = None
	try:
		pt = GeoRefUsermadeMapPoint.get_by_id(long(confirm.mid))
	except:
		pt = MapPoint.get_by_id(long(confirm.mid))
	pt.location = confirm.mlocation
	pt.name = confirm.mname
	pt.update_location()
	pt.put()
	confirm.delete()
	self.redirect('http://mapmeld.appspot.com/olpcMAPolpc?id=' + str(pt.key().id()))

class EmailConfirm(db.Model):
	mid = db.StringProperty(multiline=False)
	mname = db.StringProperty(multiline=False)
	mlocation = db.StringProperty(multiline=False)
	ekey = db.StringProperty(multiline=False)

class MapPoint(db.Model):
	name = db.StringProperty()
	blog = db.StringProperty()
	details = db.TextProperty()
	group = db.StringProperty()
	photo = db.StringProperty()
	album = db.StringProperty()
	icon = db.StringProperty()
	country = db.StringProperty()
	region = db.StringProperty()
	email = db.StringProperty()	
	lastUpdate = db.DateTimeProperty(auto_now=True)
	center = db.GeoPtProperty()
	creator = db.UserProperty()

class UsermadeMapPoint(MapPoint):
	username = db.StringProperty()

class GeoRefMapPoint(GeoModel):
  name = db.StringProperty()
  blog = db.StringProperty()
  details = db.TextProperty()
  group = db.StringProperty()
  photo = db.StringProperty()
  album = db.StringProperty()
  icon = db.StringProperty()
  tabs = db.StringListProperty()
  country = db.StringProperty()
  region = db.StringProperty()
  email = db.StringProperty()
  cc = db.StringProperty()
  lastUpdate = db.DateTimeProperty(auto_now=True)
  creator = db.UserProperty()
  @staticmethod
  def public_attributes():
    """Returns a set of simple attributes on public school entities."""
    return ['description','author','updated']

  def _get_latitude(self):
    return self.location.lat if self.location else None

  def _set_latitude(self, lat):
    if not self.location:
      self.location = db.GeoPt()

    self.location.lat = lat

  latitude = property(_get_latitude, _set_latitude)

  def _get_longitude(self):
    return self.location.lon if self.location else None

  def _set_longitude(self, lon):
    if not self.location:
      self.location = db.GeoPt()

    self.location.lon = lon

  longitude = property(_get_longitude, _set_longitude)

class GeoNewsItem(SearchLink,GeoModel):
  # title
  # href
  # sharer
  # geoscope
  added = db.DateTimeProperty(auto_now=True)
  @staticmethod
  def public_attributes():
    return ['description','author','updated']

  def _get_latitude(self):
    return self.location.lat if self.location else None

  def _set_latitude(self, lat):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lat = lat
  latitude = property(_get_latitude, _set_latitude)

  def _get_longitude(self):
    return self.location.lon if self.location else None

  def _set_longitude(self, lon):
    if not self.location:
      self.location = db.GeoPt()
    self.location.lon = lon
  longitude = property(_get_longitude, _set_longitude)

class GeoRefUsermadeMapPoint(GeoRefMapPoint):
	username = db.StringProperty()

class PhotoUpload(db.Model):
	photo = db.BlobProperty()
	redirectUrl = db.StringProperty()
	ekey = db.StringProperty(multiline=False)

class PointTab(db.Model):
	title = db.StringProperty()
	vars = db.StringListProperty()
	values = db.StringListProperty()

application = webapp.WSGIApplication([('/olpcMAP/makePoint.*',MakePoint),
									('/olpcMAPolpc/makePoint.*',MakePoint),
									('/olpcMAPolpc/share.*',ShareMain),
									('.*olpcMAP.*/addTab.*',AddTab),
									('.*olpcMAP.*/getTab.*',GetTab),
									('.*olpcMAPolpc/img.*',MapImage),
									('.*olpcMAPimg.*',MapImage),
									('/olpcMAP/community.*',Offshoots),
									('/olpcMAPolpc/community.*',Offshoots),
									('/olpcMAP/json.*',JSONout),
									('/olpcMAP/search.*',Search),
									('/olpcMAPolpc/search.*',Search),
									('/olpcMAPolpc/json.*',JSONout),
									('/olpcMAP/kml.*',KMLout),
									('/olpcMAPolpc/kml.*',KMLout),
									('/olpcMAPolpc/feed.*',RSSout),
									('/olpcMAP/import.*',JSONin),
									('.*contact.*',Contact),
									('/olpcMAP/oldest.*',Oldest),
									('/olpcMAP/newest.*',Newest),
									('/olpcMAPolpc/resetpoint.*',ResetPoint),
									('/olpcMAPolpc/confirm.*',EmailConfirming),
									('/olpcMAP.*',Home)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()