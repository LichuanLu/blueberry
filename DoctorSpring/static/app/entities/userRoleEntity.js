define(["backbone", "marionette", "utils/reqcmd"], function(Backbone, Marionette, ReqCmd) {
	// body...
	"use strict";
	var UserRoleModel = Backbone.Model.extend({
		set: function(attributes, options) {
			if (attributes.languageRoleList !== undefined && !(attributes.languageRoleList instanceof LanguageRoleCollection)) {
				attributes.languageRoleList = new LanguageRoleCollection(attributes.languageRoleList);
			}
			return Backbone.Model.prototype.set.call(this, attributes, options);
		},
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data
		},
		success: function(data, textStatus, jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function(data) {
			// body...
			console.dir(data);
		}
	});

	var LanguageRoleModel = Backbone.Model.extend({});

	var LanguageRoleCollection = Backbone.Collection.extend({
		model: LanguageRoleModel
	});


	var UserRoleHtmlModel = Backbone.Model.extend({
		success: function(data, textStatus, jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function(data) {
			// body...
			console.dir(data);
		}
	});
	var API = {
		getUserRoles: function(params) {
			if (!params) {
				params = {};
			}
			var userRoleModel = new UserRoleHtmlModel();
			userRoleModel.url = "/role/user";
			userRoleModel.fetch({
				success: function() {
					//ReqCmd.reqres.request("userrole:fetch:success");
					console.log("fetch success");
				},
				data: params
			});

			return userRoleModel
		}
	};
	
	ReqCmd.commands.setHandler("userrole:entities", function(data) {
		var temp = API.getUserRoles(data);
		return temp

	});
	return {
		LanguageRoleCollection: LanguageRoleCollection
	}

});