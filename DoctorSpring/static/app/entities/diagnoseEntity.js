define(["backbone", "marionette", "config/base/constant", "utils/reqcmd"], function(Backbone, Marionette, Constant, ReqCmd) {
	// body...
	"use strict";
	var DiagnoseModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var DiagnoseCollection = Backbone.Collection.extend({
		model: DiagnoseModel,
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
			return resp.data
		}
	});


	var DiagnoseDetailModel = Backbone.Model.extend({
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
			return resp.data
		}
	});

	var API = {
		getDiagnoseList: function(params) {
			if (!params) {
				params = {};
			}
			var diagnoseCollection = new DiagnoseCollection();
			diagnoseCollection.url = "/diagnose/list";
			diagnoseCollection.fetch({
				success: function() {
					console.log("fetch success");
				},
				data: $.param(params)
			});

			return diagnoseCollection
		},
		getExistsDiagnose: function(params) {
			if (!params) {
				params = {};
			}
			var diagnoseModel = new DiagnoseDetailModel();
			diagnoseModel.url = "/diagnose/exsits";
			diagnoseModel.fetch({
				success: function() {
					console.log("fetch success");
				},
				data: $.param(params)
			});

			return diagnoseModel
		}
	};

	return {
		API: API
	}

});