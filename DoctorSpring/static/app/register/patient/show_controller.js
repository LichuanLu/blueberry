define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'register/patient/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getPatientRegisterPageLayoutView();

			this.show(this.layoutView, {
				name: "patientRegisterPageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("patientRegisterPageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getPatientRegisterPageLayoutView: function() {
			return new View.PatientRegisterPageLayoutView();
		}

	});

	return ShowController;

});