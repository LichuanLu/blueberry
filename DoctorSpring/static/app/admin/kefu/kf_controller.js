define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'admin/kefu/kf_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var KfController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getKfPageLayoutView();
			this.appInstance = require('app');


			this.show(this.layoutView, {
				name: "kefuPageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("kefuPageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("kefuPageLayoutView attached end");
				this.layoutView.attachEndHandler();
			}, this));


			ReqCmd.commands.setHandler("payLinkHandler:KfPageLayoutView", Lodash.bind(function(data) {
				if(data.paylink){
					var TempModel = Backbone.Model.extend({});
					var tempModel = new TempModel();
					tempModel.set('paylink',data.paylink);
					var modalview = this.getDisplayPayLinkModalView(tempModel);
					this.appInstance.modalRegion.show(modalview);

				}
				
			}, this));


		},
		getKfPageLayoutView: function() {
			return new View.KfPageLayoutView();
		},
		getDisplayPayLinkModalView: function(model) {
			return new View.DisplayPayLinkModalView({
				model: model
			});
		}

	});

	return KfController;

});