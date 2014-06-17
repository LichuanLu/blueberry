define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'doctorSite/show/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getDoctorSiteLayoutView();

			this.show(this.layoutView, {
				name: "doctorSiteLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorSiteLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getDoctorSiteLayoutView: function() {
			return new View.DoctorSiteLayoutView();
		}

	});

	return ShowController;

});