define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'register/doctor/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getDoctorRegisterPageLayoutView();

			this.show(this.layoutView, {
				name: "doctorRegisterPageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorRegisterPageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getDoctorRegisterPageLayoutView: function() {
			return new View.DoctorRegisterPageLayoutView();
		}

	});

	return ShowController;

});