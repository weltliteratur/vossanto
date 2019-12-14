
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
request.open('GET', "timeline/vossantos.json", true);
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
	    sentence : p.text,
	    aUrl : "http://query.nytimes.com/gst/fullpage.html?res=" + p.aUrlId,
	    fId : p.fId,
	    author : p.author,
	    desk : p.desk,
	    "class" : "col-" + getColor(p.desk)
	});
    });

    // create dateline
    dateline('dl', {
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
}

// creates info bubble for an event
function createInfo(event) {
    // convert sentence into HTML
    let sentence = event.sentence.replace(/\*([^\*]+)\* \/([^\/]+)\//, "<b>$1</b> <em>$2</em>");
    let meta = "<li>source: NYT <a href='" + event.aUrl + "'>" + event.fId + "</a></li>";
    if (event.author) meta += "<li>author(s): " + event.author + "</li>";
    if (event.desk)   meta += "<li>desk: "      + event.desk   + "</li>";
    return sentence + "<ul>" + meta + "</ul>";
}
