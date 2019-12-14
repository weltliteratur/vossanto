
// colors used for event markers reflect the desk/category of the article
var colors = ["blueviolet", "darkgreen", "coral", "gold", "maroon", "mediumblue", "fuchsia", "firebrick"];

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
function getColor (colorClasses, desk) {
    // new desk -> new color
    if (! (desk in colorClasses)) {
	colorClasses[desk] = colors.pop();
    }
    return colorClasses[desk];
}

// callback to create dateline given the events
function initDateline(events) {
    let dlevents = [];
    let colClasses = {}; // to store the used classes

    // convert our events into dateline events
    events.forEach(p => {
        dlevents.push({
	    id : p.id,
	    start : p.date,
	    text : p.sourceLabel,
	    sentence : p.text,
	    aUrl : p.aUrl,
	    fId : p.fId
	    //,	    "class" : "col-" + getColor(colClasses, p.desk)
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
    for (let key in colClasses) {
	let li = document.createElement('li');
	li.appendChild(document.createTextNode(key));
	li.setAttribute("class", "col-" + colClasses[key]);
	ul.appendChild(li);
    }
}

// creates info bubble for an event
function createInfo(event) {
    // convert sentence into HTML
    let re = /\*([^\*]+)\* \/([^\/]+)\//;
    let sentence = event.sentence.replace(re, "<b>$1</b> <em>$2</em>");

    let imgurl = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Goethe_%28Stieler_1828%29.jpg/195px-Goethe_%28Stieler_1828%29.jpg";
    let result = "<img src='" + imgurl + "'/>" + sentence;

    return sentence + "<p/>source: <a href='" + event.aUrl + "'>" + event.fId + "</a></p>"; //result;
}
