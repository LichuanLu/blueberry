define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'doctorList/show/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getDoctorListLayoutView();

			this.show(this.layoutView, {
				name: "doctorListLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorListLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getDoctorListLayoutView: function() {
			return new View.DoctorListLayoutView();
		}

	});

	return ShowController;

});