define(['backbone', 'marionette', 'utils/reqcmd'], function(Backbone, Marionette, Reqcmd) {
	// body...
	//only used when want to run callback when entities updated at first time , before it demonstrate on views or other place,
	//if not neccesary , please use success in fetch function
	"use strict";
	Reqcmd.commands.setHandler("when:fetched", function(entities, callback) {
		var xhrs;
		xhrs = _.chain([entities]).flatten().pluck("_fetch").value();
		return $.when.apply($, xhrs).done(function() {
			return callback();
		});
	});
});