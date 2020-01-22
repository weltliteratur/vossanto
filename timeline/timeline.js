// colors for the 20 most frequent desks
var colors = {
    "Sports Desk"				: "red",
    "Metropolitan Desk"				: "green",
    "Book Review Desk"				: "yellow",
    "National Desk"				: "blue",
    "The Arts/Cultural Desk"			: "orange",
    "Arts and Leisure Desk"			: "purple",
    "Magazine Desk"				: "cyan",
    "Editorial Desk"				: "magenta",
    "Cultural Desk"				: "lime",
    "Movies, Performing Arts/Weekend Desk"	: "pink",
    "Business/Financial Desk"			: "teal",
    "Foreign Desk"				: "lavender",
    "Weekend Desk"				: "brown",
    "Leisure/Weekend Desk"			: "beige",
    "Long Island Weekly Desk"			: "maroon",
    "Style Desk"				: "aquamarine",
    "Financial Desk"				: "olive",
    "Arts & Leisure Desk"			: "bisque",
    "The City Weekly Desk"			: "navy",
    "Connecticut Weekly Desk"			: "grey",
    "other"                                     : "black"  // default
};

// load events from JSON file
request = new XMLHttpRequest();
request.open('GET', "vossantos.json", true);
request.onloadend = function() {
    if (this.status >= 200 && this.status < 400) {
	initDateline(JSON.parse(this.responseText));
    }
};
request.send();

// return a color for each desk
function getColor (key) {
    if (! (key in colors)) return colors["other"];
    return colors[key];
}

// callback to create dateline given the events
function initDateline(events) {
    let dlevents = [];
    let colClasses = {length: 0}; // to store the used classes

    // convert our events into dateline events
    events.forEach(p => {
        dlevents.push({
	    id : p.id,
	    start : p.date,
	    text : p.sourceLabel,
	    sId : p.sourceId,
	    sImId : p.sourceImId,
	    sImTh : p.sourceImThumb,
	    sImLi : p.sourceImLicense,
	    sentence : p.text,
	    aUrlId : p.aUrlId,
	    fId : p.fId,
	    author : p.author,
	    desk : p.desk,
	    "class" : "col-" + getColor(p.desk)
	});
    });

    // create dateline
    var dl = dateline('dl', {
	size: '500px',
	bands: [
	    {
		size: '85%',
		scale: Dateline.MONTH,
		interval: 180
	    },
	    {
		size: '15%',
		scale: Dateline.YEAR,
		interval: 180,
		layout: 'overview'
	    }
	],
	rememberCursor: false,
	events: dlevents,
	func: createInfo,
	cursor: "1997-01-01",
	begin: "1987-01-01",
	end: "2007-12-31"
    });

    // create legend
    let legend = document.getElementById('legend');
    let ul = document.createElement('ul');
    legend.appendChild(ul);
    for (let key in colors) {
	let li = document.createElement('li');
	li.appendChild(document.createTextNode(key));
	li.setAttribute("class", "col-" + colors[key]);
	ul.appendChild(li);
    }

    initSearch(dlevents, dl);
    scrollToFragment(dl);
}

function htmlize(s, url) {
    if (url) 
	return s.replace(/\*(\w+) ([^\*]+) (\w+)\* \/([^\/]+)\//, "<b>$1 <a href='" + url + "'>$2</a> $3</b> <em>$4</em>");
    return s.replace(/\*(\w+) ([^\*]+) (\w+)\* \/([^\/]+)\//, "<b>$1 $2 $3</b> <em>$4</em>");
}

// creates info bubble for an event
function createInfo(e) {
    let meta = "<li>NYT <a href='http://query.nytimes.com/gst/fullpage.html?res=" + e.aUrlId + "'>" + e.fId + "</a></li>";
    if (e.author) meta += "<li>by " + e.author + "</li>";
    if (e.desk)   meta += "<li>" + e.desk   + "</li>";

    let image = "";
    if (e.sImId)  {
	image += "<a href='https://commons.wikimedia.org/wiki/File:" + e.sImId + "'>" +
	    "<img src='https://upload.wikimedia.org/wikipedia/commons/" + e.sImTh + "'/></a>";
	meta += "<li>image: <a href='https://commons.wikimedia.org/wiki/File:" + e.sImId + "'>Wikimedia Commons</a>";
	if (e.sImLi)  meta += ", license: " + e.sImLi;
	meta +=  "</li>";
    }
    meta += "<li><a href='#" + e.id + "'>perma link</a></li>";
    return image + htmlize(e.sentence, "https://www.wikidata.org/wiki/" + e.sId) + "<ul>" + meta + "</ul>";
}
