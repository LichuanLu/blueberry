define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var DoctorRegisterPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorRegisterPageLayoutView");
			this.bindUIElements();
		},
		regions: {},
		el: "#register-doctor-content",
		ui: {
			
		},
		events: {},
		attachEndHandler: function() {
			

		}

	});

	return {
		DoctorRegisterPageLayoutView: DoctorRegisterPageLayoutView
	}
});