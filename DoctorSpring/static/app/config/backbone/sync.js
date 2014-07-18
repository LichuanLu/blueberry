require(["backbone"], function(Backbone) {
	// body...
	//for jsonp callback, normal case can use successful call back of fetch
	"use strict";
	// var _sync = Backbone.sync;


	// Backbone.sync = function(method, entity, options) {
	// 	// body...
	// 	var sync;
	// 	if (options === null) {
	// 		options = {};
	// 	}
	// 	sync = _sync(method, entity, options);
	// 	if (!entity._fetch && method === "read") {
	// 		entity._fetch = sync;
	// 	}
	// 	return sync
	// }

	// var _fetch = Backbone.Collection.prototype.fetch;

	Backbone.Collection.prototype.fetch = function(options) {
		options = options ? _.clone(options) : {};
		if (options.parse === void 0) options.parse = true;
		var success = options.success;
		var collection = this;
		options.success = function(resp) {
			if (resp.status == 2) {
				window.location.replace('/loginPage')

			} else if (resp.status == 4) {
				window.location.replace('/error')

			}
			var method = options.reset ? 'reset' : 'set';
			collection[method](resp, options);
			if (success) success(collection, resp, options);
			collection.trigger('sync', collection, resp, options);
		};
		wrapError(this, options);
		return this.sync('read', this, options);

	}
	var wrapError = function(model, options) {
		var error = options.error;
		options.error = function(resp) {
			if (error) error(model, resp, options);
			model.trigger('error', model, resp, options);
		};
	};


});