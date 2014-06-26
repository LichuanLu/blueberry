define(["backbone", "marionette", "utils/reqcmd"], function(Backbone, Marionette, ReqCmd) {
	// body...
	"use strict";
	var UserActivityModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var UserActivityCollection = Backbone.Collection.extend({
		model: UserActivityModel,
		success: function(data, textStatus, jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function(data) {
			// body...
			console.dir(data);
		},
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data;
		}
	});

	var API = {
		getUserActivity: function(params, collection) {
			if (!params) {
				params = {};
			}
			var userActivityCollection = collection !== '' ? collection : new UserActivityCollection();
			userActivityCollection.url = "/userActivities";
			userActivityCollection.fetch({
				add: true,
				update: true,
				remove: false,
				success: function() {
					//ReqCmd.reqres.request("getTranslateStrings:success");
					console.log("fetch success");
				},
				data: $.param(params)
			});

			return userActivityCollection;
		}
	};

	return {
		API: API
	};

});