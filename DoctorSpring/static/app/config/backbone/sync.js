require(["backbone"], function(Backbone) {
	// body...
	//for jsonp callback, normal case can use successful call back of fetch
	"use strict";
	var _sync = Backbone.sync;

	Backbone.sync = function(method, entity, options) {
		// body...
		var sync;
		if (options === null) {
			options = {};
		}
		sync = _sync(method, entity, options);
		if (!entity._fetch && method === "read") {
			entity._fetch = sync;
		}
		return sync
	}
});