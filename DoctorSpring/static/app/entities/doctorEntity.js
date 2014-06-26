define(["backbone", "marionette", "config/base/constant", "utils/reqcmd"], function(Backbone, Marionette, Constant, ReqCmd) {
	// body...
	"use strict";
	//for applyDiagnose page

	//for page number , init page number
	var DoctorPageModel = Backbone.Model.extend({
		success: function(data, textStatus, jqXHR) {
			console.dir(data);

		},
		onError: function(data) {
			console.dir(data);
		},
		parse: function(resp) {
			//this.pageNumber = resp.data.pageNumber;
			//console.log(resp.data);
			return resp.data
		}
	});

	var RecommandedDoctorModel = Backbone.Model.extend({
		success: function(data, textStatus, jqXHR) {
			console.dir(data);

		},
		onError: function(data) {
			console.dir(data);
		},
		parse: function(resp) {
			//this.pageNumber = resp.data.pageNumber;
			//console.log(resp.data);
			return resp.data
		}
	});


	var DoctorModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var DoctorCollection = Backbone.Collection.extend({
		model: DoctorModel
	});

	var API = {
		getDoctorPageModel: function(params) {
			if (!params) {
				params = {
					hospitalId: 0,
					skillId: 0,
					pageNumber: 1,
					pageSize: 6
				};
				params = $.param(params);
			}
			var doctorPageModel = new DoctorPageModel();

			doctorPageModel.url = "/doctors/list.json";
			doctorPageModel.fetch({
				success: function() {
					console.log("fetch success");
					ReqCmd.reqres.request("doctorPageModel:fetched");
				},
				data: params
			});

			return doctorPageModel
		},
		getRecommandedDoctorModel: function(params) {
			if (!params) {
				params = {}
			}
			var recommandedDoctorModel = new RecommandedDoctorModel();
			recommandedDoctorModel.url = "/doctor/recommanded";
			recommandedDoctorModel.fetch({
				success: function() {
					console.log("fetch success");
					ReqCmd.reqres.request("recommandedDoctorModel:fetched");
				},
				data: params
			});
			return recommandedDoctorModel
		}
	};

	//end for applyDiagnose page

	return {
		API: API,
		DoctorCollection: DoctorCollection

	}

});