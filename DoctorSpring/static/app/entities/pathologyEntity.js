define(["backbone", "marionette", "config/base/constant", "utils/reqcmd"], function(Backbone, Marionette, Constant, ReqCmd) {
	// body...
	"use strict";
	//using at diagnose page , get exist dicom related info
	var DicomInfoModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data
		}
	});


	var PathlogyModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var PathlogyCollection = Backbone.Collection.extend({
		model: PathlogyModel,
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
		getDicomInfo: function(params) {
			if (!params) {
				params = {};
			}
			var dicomInfoModel= new DicomInfoModel();
			dicomInfoModel.url = "/pathlogy/dicominfo.json";
			dicomInfoModel.fetch({
				success: function() {
					console.log("dicomInfoModel fetch success");
				},
				data: params
			});

			return dicomInfoModel
		},
		getPathologyList:function (params) {
			if (!params) {
				params = {};
			}
			var pathlogyCollection = new PathlogyCollection();
			pathlogyCollection.url = "/pathlogy/list.json";
			pathlogyCollection.fetch({
				success: function() {
					console.log("pathlogyCollection fetch success");
					ReqCmd.reqres.request('getPathologyList:Done');

				},
				data: params
			});

			return pathlogyCollection;
		}
	};
	return {
		API: API
	}

});


