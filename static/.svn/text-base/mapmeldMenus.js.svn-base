var opensubmenu=-1;
var submenus=[];
submenus.push(["Own Your Map","Presentation","Outreach","Social Media","Mobile"]);
submenus.push(["Travel","Government","Environment","Research","Crowdsourcing"]);
submenus.push(["Data","Web I/O","Interactions","Geo-Analytics","Consulting"]);
submenus.push(["GPS Positioning","Live GPS","StreetView","Balloon"]);
submenus.push(["Contact"]);

function init(){}
function loadNav(num){
	if(opensubmenu==num){return;}
	opensubmenu=num;
	if(submenus[num].length==1){
		$("submenu").style.display="none";
		return;
	}
	$("submenu").innerHTML="";
	var subhtml="";
	for(var sm=0;sm<submenus[num].length;sm++){
		subhtml+="<a class='smenu' href='http://mapmeld.appspot.com/"+submenus[num][sm]+"'>"+ submenus[num][sm] +"</a>";
		subhtml+="<br/>";
	}
	$("submenu").innerHTML=subhtml;
	$("submenu").style.left = $("nav"+num).offsetLeft + "px";
	$("submenu").style.display="block";
}
function submenuSelected(which){
	switch(which.id.replace("sm_","")){
		case "nav4":
			//contact
			$("coverframe").src="http://mapmeld.appspot.com/contact.html";
			$("coverwindow").style.display="block";
			break;
	}
}
function hideNav(){
	$("submenu").style.display="none";
	opensubmenu=-1;
}
function closeCoverWindow(){
	$("coverwindow").style.display="none";
}
function $(id){return document.getElementById(id);}