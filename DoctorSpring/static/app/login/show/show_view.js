define(['utils/reqcmd', 'lodash', 'marionette', 'templates','login/login_app' ,'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates, LoginApp) {
	// body...
	"use strict";
	var LoginPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init LoginPageLayoutView");
			this.returnuri = $.getUrlVar('returnuri');
			this.bindUIElements();
		},
		regions: {},
		el: "#loginpage-content",
		ui: {
		},
		events: {},
		attachEndHandler: function() {
		    LoginApp.loginAction(this.returnuri);
		}

	});

	return {
		LoginPageLayoutView: LoginPageLayoutView
	}
});