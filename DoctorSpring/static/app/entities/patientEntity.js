define(["backbone", "marionette", "config/base/constant", "utils/reqcmd"], function(Backbone, Marionette, Constant, ReqCmd) {
	// body...
	"use strict";
	var PatientProfileModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data
		}
	});


	var API = {
		getPatientProfile: function(params) {
			if (!params) {
				params = {};
			}
			var patientProfileModel= new PatientProfileModel();
			patientProfileModel.url = "/patient/profile.json";
			patientProfileModel.fetch({
				success: function() {
					console.log("patientProfileModel fetch success");
				},
				data: params
			});

			return patientProfileModel
		}
	};
	return {
		API: API
	}

});


