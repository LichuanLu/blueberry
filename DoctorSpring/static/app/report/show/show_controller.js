define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'report/show/show_view', 'utils/reqcmd'], function(Lodash, CONSTANT, BaseController, View, ReqCmd) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getReportPreviewView();

			this.show(this.layoutView, {
				name: "reportPreviewView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("reportPreviewView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			},this));
			
			console.log('follow controller init end');

		},
		getReportPreviewView: function() {
			return new View.ReportPreviewView();
		}

	});

	return ShowController;

});