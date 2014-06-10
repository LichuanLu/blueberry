define(['utils/reqcmd', 'lodash', 'marionette', 'templates','dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var DoctorListLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorListView");
			this.bindUIElements();
		},
		regions: {},
		el: "",
		ui: {
			
		},
		events: {},
		attachEndHandler: function() {

		}

	});

	return {
		DoctorListLayoutView: DoctorListLayoutView
	}
});