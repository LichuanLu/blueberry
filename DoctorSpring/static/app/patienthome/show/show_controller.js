define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'patienthome/show/show_view', 'utils/reqcmd', 'entities/diagnoseEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DiagnoseEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getPatientHomePageLayoutView();

			this.show(this.layoutView, {
				name: "patientHomePageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("patientHomePageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();

			}, this));


			//click left menu , change view , send from view 
			ReqCmd.commands.setHandler("patientHomePageLayoutView:changeContentView", Lodash.bind(function(viewName) {
				console.log("patientHomePageLayoutView changeContentView");
				this.changeContentView(viewName);
			}, this));

			//diagnose list , change type , click search, send from view
			ReqCmd.commands.setHandler("DiagnoseListView:searchDiagnose", Lodash.bind(function(type) {
				console.log("DiagnoseListView searchDiagnose");
				var params = {
					type: type
				};
				console.dir(params);
				this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList(params);
			}, this));

			


			console.log('show controller init end');

		},
		changeContentView: function(viewName) {
			if (viewName === 'diagnoseLink') {
				this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList();
				this.contentView = this.getDiagnoseListView(this.diagnoseCollection);

			} else if (viewName === 'accountLink') {
				this.contentView = this.getAccountManageLayoutView();
			}
			// var that = this;
			this.show(this.contentView, {
				region: this.layoutView.contentRegion,
				client: true
			});
		},
		getPatientHomePageLayoutView: function() {
			return new View.PatientHomePageLayoutView();
		},
		getDiagnoseListView: function(collection) {
			var view = new View.DiagnoseListView({
				collection: collection,
				itemView: View.DiagnoseTableItemView
			});
			return view;
		},
		getAccountManageLayoutView: function() {
			return new View.AccountManageLayoutView();
		}

	});

	return ShowController;

});