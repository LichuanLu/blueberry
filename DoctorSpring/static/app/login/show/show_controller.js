define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'login/show/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getLoginPageLayoutView();

			this.show(this.layoutView, {
				name: "loginPageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("loginPageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getLoginPageLayoutView: function() {
			return new View.LoginPageLayoutView();
		}

	});

	return ShowController;

});