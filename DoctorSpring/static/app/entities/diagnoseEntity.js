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
			if (typeof params === 'object') {
				params = $.param(params);
			}
			diagnoseCollection.fetch({
				success: function() {
					console.log("fetch success");
				},
				data: params
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
		},
		getAdminAllDiagnose: function(params, collection) {
			if (!params) {
				params = {};
			}
			if (typeof params === 'object') {
				params = $.param(params);
			}
			if (collection) {
				collection.reset();
				collection.fetch({
					success: function() {
						console.log("fetch success");
					},
					data: params
				});
				return
			} else {
				var diagnoseCollection = new DiagnoseCollection();
				diagnoseCollection.url = "/admin/diagnose/list/all";
				diagnoseCollection.fetch({
					success: function() {
						console.log("fetch success");
					},
					data: params
				});
			}

			return diagnoseCollection
		},
		getAdminMyDiagnose: function(params, collection) {
			if (!params) {
				params = {};
			}
			if (typeof params === 'object') {
				params = $.param(params);
			}
			if (collection) {
				collection.reset();
				collection.fetch({
					success: function() {
						console.log("fetch success");
					},
					data: params
				});
				return
			} else {
				var diagnoseCollection = new DiagnoseCollection();
				diagnoseCollection.url = "/admin/diagnose/list/my";
				diagnoseCollection.fetch({
					success: function() {
						console.log("fetch success");
					},
					data: params
				});

			}


			return diagnoseCollection
		},
		getDiagnoseDetail: function(params) {
			if (!params) {
				params = {};
			}
			var diagnoseModel = new DiagnoseDetailModel();
			diagnoseModel.url = "/diagnose/reportdetail";
			diagnoseModel.fetch({
				success: function() {
					console.log("getDiagnoseDetail fetch success");
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