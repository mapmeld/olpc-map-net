import cgi,logging,geotypes
from datetime import datetime, date, time, timedelta

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users, memcache, mail
from google.appengine.api.urlfetch import fetch,GET
from geomodel import GeoModel
from olpcmap import GeoRefMapPoint, GeoRefUsermadeMapPoint, Search, GeoNewsItem

class MyMapHome(webapp.RequestHandler):
  def get(self):
	self.response.out.write('''<!DOCTYPE html> 
<html> 
<head> 
	<title>olpcMAP.net - a geosocial network</title>
	<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="RSS2"/>
	<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="GeoRSS"/>
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/crowdmap-default.css" /> 
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/terra.css" /> 
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/themeroller.css" /> 
	<!--[if lte IE 7]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/iehacks.css" />
	<![endif]--><!--[if IE 7]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/ie7hacks.css" />
	<![endif]--><!--[if IE 6]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/ie6hacks.css" />
	<![endif]-->
	<script type="text/javascript"> 
function contactMode(){
	$("coverwindow").style.display="block";
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function $(id){return document.getElementById(id)}
	</script> 
	<style type='text/css'> 
div.map img{
	border:4px solid white;
}
div.map img:hover{
	border:4px solid blue;
}
a.banner{
	color:white;
	background-color:black;
	text-decoration:none;
	4px solid black;
}
a.banner:hover{
	text-decoration:underline;
	border:4px solid blue;
}
	</style> 
</head> 
<body id="page"> 
	<div class="rapidxwpr floatholder"> 
		<div id="middle"> 
			<div class="background layoutleft">
				<div id="mainmenu" class="clearingfix"> 
					<ul> 
						<li><a href="http://mapmeld.appspot.com/olpcMAPolpc/home" class="active">olpcMAP.net</a></li> 
						<li><a href="http://mapmeld.appspot.com/olpcMAP">Main Map</a></li> 
						<li><a href="http://mapmeld.appspot.com/olpcMAPolpc/share">Share Links</a></li> 
						<li><a href="http://mapmeld.appspot.com/olpcMAPolpc/community">Map Hacks</a></li> 
						<li><a href="#" onclick="contactMode()">Contact Us</a></li>
						<li>
							<form method="GET" id="search" action="http://mapmeld.appspot.com/olpcMAPolpc/map" style="background-color:#EEEEEE;padding-left:10px;padding-right:10px;"> 
								<input type="text" name="q" value="" class="text" style="display:inline;vertical-align:middle;max-width:150px;"/>
								<button class="searchbtn" onclick="document.getElementById('search').submit()" style="font-family:Arial,Helvetica,sans-serif;font-weight:bold;font-size:120%"><img src="http://mapmeld.appspot.com/xo-red-search.png" style="display:inline;vertical-align:middle;"/>Find</button>
								<input type="hidden" name="view" value="alt"/> 
							</form>
						</li>
					</ul> 
				</div> 
<div id="main" class="clearingfix" style="width:100%;margin-left:-3%;margin-right:-8%;min-width:80%;background-color:white;"> 
	<div id="mainmiddle" class="floatbox withright"> 
	<table><tr style="vertical-align:top;"><td><div id="mainleft" class="clearingfix" style="max-width:200px;">
		<h5>Featured</h5>
		<div class="mainbanner" style="width:200px;font-size:14pt;color:white;font-weight:bold;background-color:black;font: normal normal bold 16px/19px arial, Helvetica, Utkal, sans-serif;text-align:center;">''')
	featured = memcache.get('featured')
	if(featured is None):
		topFour = FeatureArticle.gql("ORDER BY postDate DESC").fetch(4)
		isFirst = 1
		for art in topFour:
			if(isFirst == 1):
				isFirst = 0
				myLink = art.href
				if(art.href.find('olpcmapmakers') != -1):
					myLink = "http://olpcMAP.net?id=" + art.mapID
				featured = '			<img class="mainbanner" src="' + art.photo + '''" style="width:200px;border-bottom:1px solid #444444;"/><br/>
			<span class="mainbanner" style='padding:12px;'><a href="''' + myLink + '" target="_blank">' + art.title + '''</a></span>
		</div>
		<ul class="category-filters nonspecial" style="list-style-type:square;border:none;">'''
				for bullet in art.bullets:
					featured = featured + '			<li class="nonspecial" style="list-style-type:square;">' + bullet + '</li>'
				featured = featured + '			<br/><a href="http://olpcMAP.net?id=' + art.mapID + '''" target="_blank">To the Map</a></li>
		</ul>
		<hr/>
		<h5>Previous</h5>
		<ul class="category-filters nonspecial" style='list-style-type:square;border:none;'>'''
			else:
				myLink = art.href
				if(art.href.find('olpcmapmakers') != -1):
					myLink = "http://olpcMAP.net?id=" + art.mapID
				featured = featured + '<li class="nonspecial" style="list-style-type:square;"><a href="' + myLink + '" target="_blank">' + art.title + '</a></li>'
		memcache.set('featured',featured,240)
	self.response.out.write(featured)
	self.response.out.write('''		</ul>
		</div>
	</td><td>
	<div class="floatbox" style="height:650px;max-width:490px;margin-top:-20px;"> 
		<div class="filters clearingfix"> 
		</div> 
		<div class="map" id="map" style="width:460px;margin-left:15px;margin-right:15px;"> 
			<a href="http://mapmeld.appspot.com/olpcMAP"><img src="http://mapmeld.appspot.com/staticmap.png" width="456" height="253" title="Go to Community Map" alt="Go to Community Map"/></a> 
			<br/>
			<div style="width:456px;background-color:black;font-weight:bold;font-size:16pt;text-align:center;padding-top:2px;padding-bottom:2px;"><a class="banner" href="http://wiki.laptop.org/images/0/0e/Tutorial_for_olpcMAP.pdf" target="_blank">Click for Step-by-Step PDF Guide</a></div>
			<br/>
			<a href="http://megaswf.com/simple_serve/103098/" target="_blank"><img src="http://mapmeld.appspot.com/addstuff.png" width="456" height="254" alt="Watch Video Introduction" title="Watch Video Introduction"/></a> 
		</div> 
		<div style="clear:both;"></div> 
		<div style="clear:both;"></div> 
	</div> 
	</td><td>
		<ul class="category-filters" style="max-width:240px;"> 
			<div class="submit-incident clearingfix" style="position:static;display:block;float:none;margin:0px;padding:0px;margin-left:-100px;"> 
				<a href="http://mapmeld.appspot.com/olpcMAP?add=volunteer" style="width:120px;border-bottom:2px solid white;">Add Volunteer</a> 
				<a href="http://mapmeld.appspot.com/olpcMAP?add=project" style="width:120px;">Add Project</a> 
			</div><br/>
			<h5>Latest Updates</h5> 
			<table class="table-list"> 
				<thead> 
					<tr> 
						<th scope="col" class="icon">Icon </th> 
						<th scope="col" class="title">Name </th> 
						<th scope="col" class="date">Time </th> 
					</tr> 
				</thead>
				<tbody>\n''')
	recentPts = memcache.get('recentPts')
	if(recentPts is None):
		recentPts = ''
		mapPoints = GeoRefUsermadeMapPoint.gql("ORDER BY lastUpdate DESC")
		results = mapPoints.fetch(10)
		for pt in results:
			if(len(pt.name) < 3):
				continue
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
			namewords = usename.split(" ")
			for nw in range(0,len(namewords)):
				if(len(namewords[nw]) > 20):
					namewords[nw]=namewords[nw][0:20]+" "+namewords[nw][20:len(namewords[nw])]
			modName=' '.join(namewords)
			if((pt.icon=='') or (pt.icon=='DEFAULT')):
				pt.icon = 'http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=location|FF0000'
			mytimedelta = datetime.now() - pt.lastUpdate
			mytime = "Recent"
			if(mytimedelta.days == 0):
				myseconds = mytimedelta.seconds
				if(myseconds < 60):
					if(myseconds != 1):
						mytime = str(myseconds) + " seconds ago"
					else:
						mytime = "1 second ago"
				elif(myseconds < 60*60):
					if(int(myseconds/60) != 1):
						mytime = str(int(myseconds/60)) + " minutes ago"
					else:
						mytime = '1 minute ago'
				else:
					if(int(myseconds/60/60) != 1):
						mytime = str(int(myseconds/60/60)) + " hours ago"
					else:
						mytime = '1 hour ago'
			else:
				if(mytimedelta.days==1):
					mytime = "1 day ago"
				else:
					mytime = str(mytimedelta.days) + " days ago"
			recentPts = recentPts + '''		<tr>
			<td><img src="''' + cgi.escape(pt.icon.replace('https','http')) + '''" style="max-height:14pt;max-width:14pt;"></td>
			<td><a href="http://mapmeld.appspot.com/olpcMAPolpc?id=''' + str(pt.key().id()) + '" alt="' + cgi.escape(usename) +  '" title="' + cgi.escape(usename) + '">' + modName + '''</a></td>
			<td>''' + mytime + '''</td>
		</tr>\n'''
		memcache.set('recentPts',recentPts,240)
	self.response.out.write(recentPts)
	self.response.out.write('''					</tbody> 
				</table> 
			</ul>
		</td></tr></table>
	</div> 
</div> 
<div class="content-container"> 
</div> 
			</div> 
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
	</div> 
	</body> 
</html>''')

class MyMapNews(webapp.RequestHandler):
  def post(self):
	if(self.request.get('topic') == 'new'):
		s = ComUpdate()
		s.title = self.request.get('olpcMapQ')
		s.description = db.Text("Edit this Description")
		s.type = "unknown"
		s.postExpire = datetime.now() + timedelta(7)
		s.put()
		self.redirect('http://mapmeld.appspot.com/olpcMAPolpc/news?time=edit&topic=' + str(s.key().id()))

  def get(self):
	if(self.request.get('topic') != ''):
		comUpdate = ComUpdate.get_by_id(long(self.request.get('topic')))
		if comUpdate is None:
			self.redirect('http://olpcMAP.net/news')
			return
		if(comUpdate.type == 'unknown'):
			# edit menu
			self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>olpcMAP Topic ''' + cgi.escape(comUpdate.title[0:15]) + '''...</title>
		<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts RSS2"/>
		<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts GeoRSS"/>
		<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
		<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:#00275E;}
div.main{
	background-color:#e9e9ff;
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
div.desc{background-color:white;padding:12px;min-height:300px;width:90%;}
button.submit{
	background: transparent url(http://mapmeld.appspot.com/bg_submit-report.png) repeat-x;
	border: solid #208A08;
	border-bottom: none;
	padding: 9px 12px 9px 12px;
}
textarea{font-family:arial;}
		</style>
		<script type='text/javascript'>
function contactMode(){
	$("coverwindow").style.display="block";
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function $(id){return document.getElementById(id);}
		</script>
	</head>
	<body>
		<div class="header">
			<h3><span style='font-size:1.7em;'>olpcMAP Community</span> - topics</h3>
			<br/>
		</div>
		<div class="nav" style="border-bottom:1px solid black;">
			<span class="navoption"><a href="http://olpcMAP.net/home">Homepage</a></span>
			<span class="navoption"><a href="http://olpcMAP.net">Community Map</a></span>
			<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">About the Map</a></span>
			<span class="navoption"><a href="#" onclick="contactMode()">Contact</a></span>
		</div>
		<div class="main">
			<br/><br/>
			<table style="width:100%;"><tr style="vertical-align:top;"><td style="vertical-align:top;">\n''')
			mytimedelta = datetime.now() - comUpdate.postDate
			mytime = "Recent"
			if(mytimedelta.days == 0):
				myseconds = mytimedelta.seconds
				if(myseconds < 60):
					if(myseconds != 1):
						mytime = str(myseconds) + " seconds ago"
					else:
						mytime = "1 second ago"
				elif(myseconds < 60*60):
					if(int(myseconds/60) != 1):
						mytime = str(int(myseconds/60)) + " minutes ago"
					else:
						mytime = '1 minute ago'
				else:
					if(int(myseconds/60/60) != 1):
						mytime = str(int(myseconds/60/60)) + " hours ago"
					else:
						mytime = '1 hour ago'
			else:
				if(mytimedelta.days==1):
					mytime = "1 day ago"
				else:
					mytime = str(mytimedelta.days) + " days ago"
			self.response.out.write('<h4>' + cgi.escape(comUpdate.title or '') + '</h4><hr/><div class="desc">Your topic<textarea style="height:30%;width:100%;min-height:70px;"></textarea><br/>Your description<textarea style="height:70%;width:100%;min-height:300px;">' + cgi.escape(comUpdate.description or '') + "</textarea></div><hr/>Posted by " + cgi.escape(comUpdate.postedBy or '') + '<input name="postBy" style="width:250px;" size=35/> - ' + mytime)
			self.response.out.write('''		<br/><br/>
			</td><td style="vertical-align:top;">
				<!-- right sidebar -->
				<div style="background-color:#ffffff;width:100px;min-height:300px;">
					<u>Recent topics</u>:
					<br/><br/>
					<u>Similar topics</u>:
					<br/><br/>
				</div>
			</td></tr></table>
		</div>
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
			return
		self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>olpcMAP Topic ''' + cgi.escape(comUpdate.title[0:15]) + '''...</title>
		<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts RSS2"/>
		<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts GeoRSS"/>
		<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
		<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:#00275E;}
div.main{
	background-color:#e9e9ff;
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
div.desc{background-color:white;padding:12px;min-height:300px;width:90%;}
textarea{font-family:arial;}
		</style>
		<script type='text/javascript'>
function contactMode(){
	$("coverwindow").style.display="block";
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function $(id){return document.getElementById(id);}
		</script>
	</head>
	<body>
		<div class="header">
			<h3><span style='font-size:1.7em;'>olpcMAP Community</span> - topics</h3>
			<br/>
		</div>
		<div class="nav" style="border-bottom:1px solid black;">
			<span class="navoption"><a href="http://olpcMAP.net/home">Homepage</a></span>
			<span class="navoption"><a href="http://olpcMAP.net">Community Map</a></span>
			<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">About the Map</a></span>
			<span class="navoption"><a href="#" onclick="contactMode()">Contact</a></span>
		</div>
		<div class="main">
			<br/><br/>
			<table style="width:100%;"><tr style="vertical-align:top;"><td style="vertical-align:top;">\n''')
		mytimedelta = datetime.now() - comUpdate.postDate
		mytime = "Recent"
		if(mytimedelta.days == 0):
			myseconds = mytimedelta.seconds
			if(myseconds < 60):
				if(myseconds != 1):
					mytime = str(myseconds) + " seconds ago"
				else:
					mytime = "1 second ago"
			elif(myseconds < 60*60):
				if(int(myseconds/60) != 1):
					mytime = str(int(myseconds/60)) + " minutes ago"
				else:
					mytime = '1 minute ago'
			else:
				if(int(myseconds/60/60) != 1):
					mytime = str(int(myseconds/60/60)) + " hours ago"
				else:
					mytime = '1 hour ago'
		else:
			if(mytimedelta.days==1):
				mytime = "1 day ago"
			else:
				mytime = str(mytimedelta.days) + " days ago"
		self.response.out.write('<h4>' + cgi.escape(comUpdate.title) + '</h4><hr style="color:black;"/><div class="desc">' + cgi.escape(comUpdate.description) + "</div><hr style='color:black;'/>Posted by " + cgi.escape(comUpdate.postedBy) + " - " + mytime)
		self.response.out.write('''		<br/><br/>
				<h4>Responses</h4>
				<form id="replyform" style="text-align:left;font-size:12pt;" action="http://mapmeld.appspot.com/olpcMAPolpc/news?reply=''' + str(comUpdate.key().id()) + '''" method="POST">
					<div style="width:450px;background-color:#ffffff;padding:8px;text-align:center;">Write a response<br/><textarea style="width:450px;height:200px;font-family:arial;"></textarea><br/><br/></div>
					<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Post"/>
				</form>
			</td><td style="vertical-align:top;">
				<!-- right sidebar -->
				<div style="background-color:#ffffff;width:100px;min-height:300px;">
					<u>Recent topics</u>:
					<br/><br/>
					<u>Similar topics</u>:
					<br/><br/>
				</div>
			</td></tr></table>
		</div>
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
	else:
		self.response.out.write('''<!DOCTYPE html>
<html>
<head>
	<title>olpcMAP News Concept</title>
	<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts RSS2"/>
	<link rel="alternate" type="application/rss+xml" href="http://mapmeld.appspot.com/olpcMAPolpc/feed" title="Map Posts GeoRSS"/>
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/crowdmap-default.css" /> 
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/terra.css" /> 
	<link rel="stylesheet" type="text/css" href="http://mapmeld.appspot.com/themeroller.css" /> 
	<!--[if lte IE 7]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/iehacks.css" />
	<![endif]--><!--[if IE 7]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/ie7hacks.css" />
	<![endif]--><!--[if IE 6]><link rel="stylesheet" type="text/css" href="http://olpcmap.crowdmap.com/media/css/ie6hacks.css" />
	<![endif]-->
	<style type="text/css">
tr.postItem{border:1px solid white;color:black;font-size:14pt;}
tr.postItem a{color:black}
tr.postItem:hover{background-color:#FFFFFF;color:black;border:1px solid black;}
tr.postItem:hover a{color:blue;}
tr.postItem a:hover{color:blue;}
	</style>
</head>
<body style="background-color:#00275E;"><div id="main" class="clearingfix" style="width:85%;margin-left:auto;margin-right:auto;min-width:80%;background-color:#e9e9ff;"><div id="mainmiddle" class="floatbox withright"> 
<div class="content-block-left" style="position:static;margin-left:100px;">
	<h5>Community Connections</h5>
	<table class="table-list">
		<thead>
			<tr>
				<th scope="col">TYPE </th>
				<th scope="col">TOPIC </th>
				<th scope="col">DATE </th>
			</tr>
		</thead>
		<tbody>\n''')
		postIcons={'event':'http://google-maps-icons.googlecode.com/files/friends.png','job':'http://google-maps-icons.googlecode.com/files/workoffice.png'}
		postColors={'event':'#FFFF66','job':'#99CCFF'}
		comData = ComUpdate.gql("ORDER BY postDate DESC")
		if(comData is not None):
			comUpdates = comData.fetch(20)
			for comUpdate in comUpdates:
				if(comUpdate.type == 'unknown'):
					continue
				mytimedelta = datetime.now() - comUpdate.postDate
				mytime = "Recent"
				if(mytimedelta.days == 0):
					myseconds = mytimedelta.seconds
					if(myseconds < 60):
						if(myseconds != 1):
							mytime = str(myseconds) + " seconds ago"
						else:
							mytime = "1 second ago"
					elif(myseconds < 60*60):
						if(int(myseconds/60) != 1):
							mytime = str(int(myseconds/60)) + " minutes ago"
						else:
							mytime = '1 minute ago'
					else:
						if(int(myseconds/60/60) != 1):
							mytime = str(int(myseconds/60/60)) + " hours ago"
						else:
							mytime = '1 hour ago'
				else:
					if(mytimedelta.days==1):
						mytime = "1 day ago"
					else:
						mytime = str(mytimedelta.days) + " days ago"
				self.response.out.write('<tr class="postItem" style="background-color:' + postColors[comUpdate.type] + '"><td><img src="' + postIcons[comUpdate.type] + '" style="max-width:20pt;max-height:20pt;"/></td><td><a href="http://mapmeld.appspot.com/olpcMAPolpc/news?topic=' + str(comUpdate.key().id()) + '" alt="' + cgi.escape(comUpdate.title) + '" title="' + cgi.escape(comUpdate.title) + '"><span style="font-size:13pt;">' + cgi.escape(comUpdate.title[0:25]) + '</span></a></td><td><span style="font-size:10pt;">' + mytime + '</span></td></tr>')
		self.response.out.write('''		</tbody>
	</table>
	<form id="addPost" action="http://mapmeld.appspot.com/olpcMAPolpc/news?topic=new" method="POST">
		<input name="olpcMapQ" style="width:300px;font-size:14pt;"/>
		<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;font-size:14pt;" value="Post"/>
	</form>
</div>
<div class="content-block-right">
	<h5>News Aggregator - <a href="http://mapmeld.appspot.com/olpcMAPolpc/feed/community" target="_blank">RSS</a></h5>
	<table class="table-list">
		<thead>
			<tr>
				<th scope="col">TITLE </th>
				<th scope="col">SOURCE </th>
				<th scope="col">DATE </th>
			</tr>
		</thead>
		<tbody>\n''')
		news = memcache.get('news')
		if((news is not None) and (self.request.get('show') != "news")):
			self.response.out.write(news.decode('utf8'))
		else:
			newsFeed = " "
			try:
				newsSrc = cgi.escape(fetch("http://olpcmap.crowdmap.com/feeds", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content)
				newsSrc = newsSrc.split('report_row1')
				for newsI in range(1,11):
					newsItem = newsSrc[newsI]
					modLink = newsItem[newsItem.find('&lt;h3&gt;&lt;a href=')+22:len(newsItem)]
					fullTitle = modLink[modLink.find('"&gt;')+5:modLink.find('&lt;/a&gt;&lt;/h3&gt')]
					modLink = modLink[0:modLink.find('"&gt;')]
					if(len(fullTitle) > 40):
						modTitle = fullTitle[0:40]+"..."
					else:
						modTitle = fullTitle
					srcDate=newsItem[newsItem.find('report_date report_col3')+28:len(newsItem)]
					srcDate=srcDate[0:srcDate.find('&lt;/div')]#.strip()
					srcName=newsItem[newsItem.find('report_location report_col4')+32:len(newsItem)]
					srcName=srcName[0:srcName.find('&lt;/div')]#.strip()
					newsFeed = newsFeed + '<tr><td><a href="' + modLink + '" target="_blank" alt="' + fullTitle + '" title="' + fullTitle + '">' + modTitle + '</a></td>\n<td>'+ srcName + '</td>\n<td>' + srcDate + '</td></tr>'
				memcache.set('news',newsFeed,180)
				self.response.out.write(newsFeed.decode('utf8'))
			except:
				newsFeed = 'Newsfeed - an error occurred'
		self.response.out.write('''		</tbody>
	</table>
	<a class="more" href="http://olpcmap.crowdmap.com/feeds">View More</a>
</div>
</div></div>
</body>
</html>''')

class Profiles(webapp.RequestHandler):
  def get(self):
	pt = None
 	try:
		pt = GeoRefUsermadeMapPoint.get_by_id(long(self.request.get('id')))
	except:
		try:
			pt = MapPoint.get_by_id(long(self.request.get('id')))
		except:
			self.response.out.write('''<!DOCTYPE html>
<html>Point not found</html>''')
	openUser = users.get_current_user()
	googSI=''
	if(openUser is not None):
		googSI=users.create_logout_url(self.request.url)
		googSI='<a href="'+googSI+'">Sign Out</a>'
	else:
		googSI=users.create_login_url(self.request.url)
		googSI='<a href="'+googSI+'">Sign In (OpenID)</a>'
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
	self.response.out.write('''<!DOCTYPE html>
<html>
<head>
	<title>''' + usename + ''' on olpcMAP.net</title>
	<link rel='stylesheet' type='text/css' href='http://mapmeld.appspot.com/mapmeldStyles.css'/>
	<script type='text/javascript'>
function contactMode(){
	$("coverwindow").style.display="block";
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function $(id){return document.getElementById(id);}
	</script>
	<style type='text/css'>
html{width:100%;height:100%;}
body{width:100%;height:100%;margin:0px;padding:0px;background-color:#black;}
div.main{
	background-color:#e9e9ff;
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
	</style>
</head>
<body>
	<div class="header">
		<h3><span style='font-size:1.7em;'>olpcMAP Pages</span> - get to know - &nbsp;&nbsp;&nbsp;''' + googSI + '''</h3>
		<br/>
	</div>
	<div class="nav" style="border-bottom:1px solid black;">
		<span class="navoption"><a href="http://mapmeld.appspot.com/olpcMAPolpc/home" target="_blank">Home</a></span>
		<span class="navoption"><a href="http://mapmeld.appspot.com/olpcMAP">Community Map</a></span>
		<span class="navoption"><a href="http://wiki.laptop.org/go/OlpcMAP" target="_blank">Wiki Guide</a></span>
		<span class="navoption"><a href="#" onclick="contactMode()">Contact olpcMAP</a></span>
	</div>
	<div class="main">
		<br/><br/>
		<form style="background-color:white;padding:12px;display:inline;" action="http://mapmeld.appspot.com/olpcMAPolpc/page/search" method="GET">
			<input id="searchCheck" name="q" type="text" style="padding-left:10px;padding-right:10px;margin:12px;font-size:15pt;min-width:200px;font-family:Arial,sans-serif;font-size:15pt;vertical-align:middle;display:inline;background-color:#f9f9ff;" size="20" onkeypress="keyGoes(event);"/>
			<button onclick="searchOpt();" style="font-size:14pt;cursor:pointer;margin-left:-12px;margin-right:50%;">
				<img src="https://sites.google.com/site/olpcau/home/Bluesmall.png" style="vertical-align:middle;margin-right:-5px;width:20px;height:20px;"/>
				<span style="vertical-align:middle;">Search</span>
			</button>
		</form><br/>
		<span style="font-size:15pt;font-weight:bold;">''' + usename + '''</span><br/>
		<table><tr>
			<td>\n''')
	if(pt.album != ''):
		self.response.out.write('''				<a href="''' + cgi.escape(pt.album) + '''" target="_blank">
					<img src="''' + cgi.escape(pt.photo) + '''" style="max-width:500px;max-height:400px;float:left;"/><br/>
					<span style="margin-top:20px;">View Photos</span>
				</a>\n''')
	else:
		self.response.out.write('''				<img src="''' + cgi.escape(pt.photo) + '''" style="max-width:500px;max-height:400px;float:left;"/><br/>
				<br/>\n''')
	self.response.out.write('''				<br/><br/>
				<a href="#contact"><button class="submit" onclick="$('contactHidden').style.display='block';"><span style="color:#ffffff;">Contact Me</span></button></a>
				<br/><br/><br/><br/>
			</td>
			<td>
				<div class="mapgrp">
					<p><b>From:</b> '''+ self.linkify(cgi.escape(pt.group).replace('&lt;a','<a').replace('&lt;/a','</a').replace('&gt;','>')) + '''</p>
				</div>
				<div>
					<p>'''+self.linkify(cgi.escape(pt.details).replace('&lt;br&gt;','</p><p>').replace('&lt;br/&gt;','</p><p>').replace('&lt;a','<a').replace('&lt;/a','</a').replace('&gt;','>'))+'''</p>
				</div>
				<iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fmapmeld.appspot.com%2FolpcMAPolpc%2Fpage%3Fid%3D'''+str(pt.key().id())+'''&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font=arial&amp;colorscheme=light&amp;height=80" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:80px;" allowTransparency="true"></iframe>
			</td>
		</tr>
		</table>
		<div style="width:100%;text-align:center;">\n''')
	if((openUser == users.User(pt.email)) or (openUser == users.User('ndoiron@andrew.cmu.edu'))):
		self.response.out.write('''			<iframe src="http://mapmeld.appspot.com/olpcMAPolpc/page/titlemap?id=''' + str(pt.key().id()) + '&ll=' + str(pt.location.lat) + ','	+ str(pt.location.lon) + '&icon=' + cgi.escape(pt.icon) + '''" style="border:none;margin-left:auto;margin-right:auto;text-align:center;width:650px;height:200px;" width="650" height="200"></iframe>
			<img src="http://mapmeld.appspot.com/plusIcon.gif" onclick="expandMapFrame()"/>
			<br/>
			<a href="http://mapmeld.appspot.com/olpcMAP?id=''' + str(pt.key().id()) +'''">Full Map</a>\n''')
	else:
		self.response.out.write('''			<a href="http://mapmeld.appspot.com/olpcMAP?id=''' + str(pt.key().id()) +'''">
				<img src="http://mapmeld.appspot.com/olpcMAP?map=image&id=''' + str(pt.key().id()) + '''&km-distance=40&w=650&h=100&z=10" style="margin-left:auto;margin-right:auto;text-align:center;width:650px;height:100px;" width="650" height="100"/>
			</a>\n''')
	self.response.out.write('''
		</div>
		<table><tr>
			<td>
				<h4>Links</h4>
				<b>Link to this point</b><br/>
				<span style='font-size:10pt;'>http://olpcMAP.net?id=''' + str(pt.key().id()) + '''</span><hr/>
				<b>Link to profile page</b><br/>
				<span style='font-size:10pt;'>http://olpcMAP.net/page?id=''' + str(pt.key().id()) + '''</span><hr/>
				<b>Link to nearby points</b><br/>
				<span style='font-size:10pt;'>http://olpcMAP.net?id=''' + str(pt.key().id()) + '''&km-distance=40</span><hr/>
				<b>Quick Map for low-bandwidth users</b><br/>
				<span style='font-size:10pt'>http://olpcMAP.net?map=quick&id=''' + str(pt.key().id()) + '''&km-distance=40</span>
			</td>
			<td>
				<a name="contact"></a>
				<div id="contactHidden" style="display:none;">
					<h4>Contact</h4>
					<iframe src="http://mapmeld.appspot.com/olpcMAP/contacter?id='''+str(pt.key().id())+'''" style="border:none;" width="350" height="350"></iframe>
				</div>
			</td>
		</tr>''')
	if(len(pt.tabs)>0):
		for tab in pt.tabs:
			self.response.out.write('''<tr><td span="2">
			<span>''' + cgi.escape(tab) + '''</span>
		</td></tr>''')
	self.response.out.write('''\n		</table>
		<br/>
	</div>
	<div id="coverwindow" style="display:none;position:fixed;margin-left:auto;margin-right:auto;top:100px;border:1px solid black;font-size:16pt;text-align:right;background-color:#333333;">
		<input type="button" value="X" style="border:1px solid black;color:black;font-size:16pt;" onclick="closeCoverWindow();"/>
		<br/>
		<form id="signinform" style="width:100%;background-color:#ffffff; text-align:left; font-size:13pt;" action="http://mapmeld.appspot.com/olpcMAP/contact?id=you" method="POST">
			E-mail <input id="emaillogin" name="login"/><br/>
			<!--Password <input id="passwordlogin" type="password" name="password"/><hr/>-->
			Message<br/><textarea name="message" width="550" height="300"></textarea>
			<input type="submit" style="width:50%;text-align:center;margin-left:auto;margin-right:auto;" value="Send"/>
		</form>
		<div id="infoform"></div>
	</div>
</body>
</html>''')
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

class GeoNews(webapp.RequestHandler):
  def get(self):
	self.response.headers['Content-Type'] = "application/vnd.google-earth.kml+xml"
	self.response.out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
	<Document>
		<name>olpcMAP.net geotagged news</name>
		<Style id="newsItem">
			<IconStyle>
				<Icon>
					<href>http://maps.google.com/mapfiles/kml/shapes/snowflake_simple.png</href>
				</Icon>
			</IconStyle>
		</Style>\n''')
	points = None
	if(self.request.get('llregion') != ''):
		ne_lat = self.request.get('llregion').split(',')[0]
		ne_lng = self.request.get('llregion').split(',')[1]
		sw_lat = self.request.get('llregion').split(',')[2]
		sw_lnt = self.request.get('llregion').split(',')[3]
		points = GeoNewsItem.bounding_box_fetch(
					GeoNewsItem.gql("ORDER BY added DESC"),
					geotypes.Box(float(ne_lat),float(ne_lng),float(sw_lat),float(sw_lng)),
					max_results=100
				)
	else:
		points = GeoNewsItem.gql('ORDER BY added DESC')
		points.fetch(100)
	for pt in points:
		self.response.out.write('''		<Placemark>
			<styleUrl>#newsItem</styleUrl>
			<name>''' + cgi.escape(pt.title) + '''</name>
			<description>&lt;hr/&gt;&lt;a href=\'''' + cgi.escape(pt.href) + "' target='_blank'&gt;" + cgi.escape(pt.href) + cgi.escape('</a><br/><br/>Article from ') + cgi.escape(pt.sharer) + '''</description>
			<Point>
				<coordinates>'''+str(pt.location.lon)+","+str(pt.location.lat)+''',0</coordinates>
			</Point>
		</Placemark>\n''')
	self.response.out.write('	</Document>\n</kml>')

class DoomsdayBlog(webapp.RequestHandler):
  def get(self):
	lastBlogPost = FeatureArticle.gql("ORDER BY postDate DESC").get()
	if( (datetime.now() - lastBlogPost.postDate) > timedelta(days=7) ):
		# doomsday blog
		lastBlogPost.postDate = datetime.now()
		lastBlogPost.put()
		mail.send_mail(sender="beautify@olpcMAP.net",
			to='beautify@olpcMAP.net',
			subject="olpcMAP Blog - 7 days since last update",
			body='Please help update olpcMAP with a new blog post.  It has been 7 days since the last post was made.')
	blogSrc = fetch("http://olpcmapmakers.blogspot.com/feeds/posts/default", payload=None, method=GET, headers={}, allow_truncated=False, follow_redirects=True).content.split('<entry>')
	postTotal = range(1,len(blogSrc))
	postTotal.reverse()
	skip = 0
	for a in postTotal:
		blogID = blogSrc[a][blogSrc[a].find('<id>')+4:blogSrc[a].find('</id>')]
		if(skip == 0):
			if(blogID == lastBlogPost.blogID):
				skip = 1
			continue
		logging.info('adding blog post')
		blog = FeatureArticle()
		blog.title = blogSrc[a][blogSrc[a].find('<title')+4:blogSrc[a].find('</title>')]
		blog.title = blog.title[blog.title.find('>')+1:len(blog.title)]
		blog.photo = blogSrc[a][blogSrc[a].find('&lt;img')+7:len(blogSrc[a])]
		blog.photo = blog.photo[blog.photo.find('src="')+5:len(blog.photo)]
		blog.photo = blog.photo[0:blog.photo.find('"')]
		blog.href = blogSrc[a][blogSrc[a].rfind("<a rel='alternate' type='text/html' href='")+42:len(blogSrc[a])]
		blog.href = blog.href[0:blog.href.find("'")]
		findBullets = blogSrc[a][blogSrc[a].find('<content'):blogSrc[a].find('</content>')]
		findBullets = findBullets[findBullets.find('~')+1:findBullets.rfind('~')]
		blog.bullets = findBullets.split('~')
		blog.mapID = blogSrc[a][blogSrc[a].find('id=')+3:len(blogSrc[a])]
		if(blog.mapID.find('&') != -1):
			blog.mapID = blog.mapID[0:blog.mapID.find('&')]
		if(blog.mapID.find(' ') != -1):
			blog.mapID = blog.mapID[0:blog.mapID.find(' ')]
		if(blog.mapID.find('"') != -1):
			blog.mapID = blog.mapID[0:blog.mapID.find('"')]
		blog.blogID = blogID
		blog.put()

class ProfileSearch(webapp.RequestHandler):
  def get(self):
	searcher = Search()
	exactName = GeoRefUsermadeMapPoint.gql("WHERE name = :1",self.request.get('q')).get()
	if(exactName is not None):
		self.redirect('http://mapmeld.appspot.com/olpcMAPolpc/page?id=' + str(exactName.key().id()))
	else:
		self.response.out.write('''<!DOCTYPE html>
<html>
	<head>
		<title>olpcMAP Profile Search</title>
		<script type="text/javascript">
function writeSearchCat(category,resultsList){
	if(resultsList.length==0){
		window.location="http://mapmeld.appspot.com/olpcMAP?q=''' + cgi.escape(self.request.get('q')).replace('"',"'") + '''";
		return "";
	}
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
function showResults(){\n''' + searcher.snap(self.request.get('q')) + '''\n}
		</script>
	</head>
	<body onload="showResults()">
		<div id="olpcMAPsr" style="height:570px;">
		</div>
		<div id="olpcMAPnoresults" style="display:none;">
			No results found.
		</div>
	</body>
</html>''')

class TitleMap(webapp.RequestHandler):
  def get(self):
	self.response.out.write('''<!DOCTYPE html>
<html><head id="head"><script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
var moveablePt;
function startMap(){
var mymap=new google.maps.Map(document.getElementById("map_div"),{
zoom:12,
streetViewControl:false,
center:new google.maps.LatLng(''' + cgi.escape(self.request.get('ll')) + '''),
mapTypeId:google.maps.MapTypeId.ROADMAP
});
kmllayer=new google.maps.KmlLayer("http://mapmeld.appspot.com/olpcMAP/kml?km-distance=40&id=''' + cgi.escape(self.request.get('id')) + '''&nid=true",{map:mymap,clickable:false,preserveViewport:true});
moveablePt=new google.maps.Marker({
position:new google.maps.LatLng(''' + cgi.escape(self.request.get('ll')) + '''),
icon:unescape("''' + cgi.escape(self.request.get('icon').replace('https','http')) + '''"),
draggable:true,
map:mymap
});
google.maps.event.addListener(moveablePt,'dragend',function(){
updatePosition()
});
}
function updatePosition(){
var sendPtScript=document.createElement("script");
sendPtScript.src="http://mapmeld.appspot.com/olpcMAP/makePoint?id=''' + cgi.escape(self.request.get('id')) + '''&point=" + moveablePt.getPosition().lat() + "," + moveablePt.getPosition().lng();
sendPtScript.src+="&cmd=loc";
document.getElementById("head").appendChild(sendPtScript)
}
</script>
<style type="text/css">
html{width:96%;height:94%;}
body{width:100%;height:95%;}
</style></head>
<body onload="startMap()"><div id="map_div" style="width:100%;height:100%;"></div></body></html>''')

# SearchTag has term string, tagLinks array

class ComUpdate(db.Model):
	title = db.StringProperty(multiline=False)
	type = db.StringProperty(multiline=False)
	description = db.TextProperty()
	postedBy = db.StringProperty(multiline=False)
	postedByMail = db.EmailProperty()
	postDate = db.DateTimeProperty(auto_now=True)
	postExpire = db.DateTimeProperty()

class FeatureArticle(db.Model):
	title = db.StringProperty(multiline=False)
	photo = db.StringProperty(multiline=False)
	href = db.StringProperty(multiline=False)
	postDate = db.DateTimeProperty(auto_now=True)
	bullets = db.StringListProperty()
	mapID = db.StringProperty(multiline=False)
	blogID = db.StringProperty(multiline=False)

application = webapp.WSGIApplication([('/olpcMAPolpc/home.*',MyMapHome),
									('/olpcMAPolpc/news/refresh.*',DoomsdayBlog),
									('/olpcMAPolpc/news.*',MyMapNews),
									('/olpcMAPolpc/geonews.*',GeoNews),
									('/olpcMAPolpc/page/titlemap.*',TitleMap),
									('/olpcMAPolpc/page/search.*',ProfileSearch),
									('/olpcMAPolpc/page.*',Profiles)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()