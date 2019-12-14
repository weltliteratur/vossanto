function initSearch(events, dl) {
    $( "#search-source" ).autocomplete({
	minLength: 0,
	source: function(request, response) {
	    var re = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
	    response($.grep(events, function(item) {
		return re.test(item.sentence);
	    }));
	},
	focus: function( event, ui ) {
            $( "#source" ).val( ui.item.text );
            return false;
	},
	select: function( event, ui ) {
            $( "#source" ).val( ui.item.text );
	    dl.find(ui.item.id);
            return false;
	}
    })
	.autocomplete( "instance" )._renderItem = function( ul, item ) {
	    var re = new RegExp($.ui.autocomplete.escapeRegex(this.term), "i");
	    var text = htmlize(item.sentence).replace(re, "<span class='ui-match'>" + this.term + "</span>");
	    return $( "<li>" )
		.append(
		    "<div>" +
			"<span class='ui-source'>" + item.text + "</span> " +
			"<span class='ui-meta'>" + item.start.toLocaleDateString(undefined, {month:"long", day:"numeric", year:"numeric"}) + "</span>" +
			"<br/>" +
			"<span class='ui-sent'>" + text + "</span>" +
		    "</div>" )
		.appendTo( ul );
	};
}
