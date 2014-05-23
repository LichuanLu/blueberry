define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'doctorhome/show/show_view', 'utils/reqcmd', 'entities/diagnoseEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DiagnoseEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getDoctorHomePageLayoutView();

			this.show(this.layoutView, {
				name: "doctorHomePageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorHomePageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			}, this));

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorHomePageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();

			}, this));


			//click left menu , change view , send from view 
			ReqCmd.commands.setHandler("doctorHomePageLayoutView:changeContentView", Lodash.bind(function(viewName) {
				console.log("doctorHomePageLayoutView changeContentView");
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

			//doctor click the action link , e.g. add diagnose
			ReqCmd.commands.setHandler("DiagnoseTableItemView:actionHandler", Lodash.bind(function(model) {
				console.log("DiagnoseTableItemView actionHandler");
				var statusId = model.get('statusId');
				if (statusId == 4) {
					if (typeof this.diagnoseActionView !== 'undefined') {
						this.diagnoseActionView.close();
					}
					this.diagnoseActionView = this.getNewDiagnoseLayoutView(model);

				} else if (statusId == 5) {
					if (typeof this.diagnoseActionView !== 'undefined') {
						this.diagnoseActionView.close();
					}
					var auditModel = DiagnoseEntity.API.getExistsDiagnose({
						diagnoseId: model.get('id')
					});
					this.diagnoseActionView = this.getNewAuditLayoutView(auditModel);
				}

				this.show(this.diagnoseActionView, {
					region: this.layoutView.newDiagnoseRegion,
					client: true
				});


			}, this));


			//close diagnose region
			ReqCmd.reqres.setHandler("NewDiagnoseLayoutView:closeRegion", Lodash.bind(function() {
				this.layoutView.newDiagnoseRegion.close();
			}, this));

			console.log('follow controller init end');

		},
		changeContentView: function(viewName) {
			if (typeof this.diagnoseActionView !== 'undefined') {
				this.diagnoseActionView.close();
			}
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
		getDoctorHomePageLayoutView: function() {
			return new View.DoctorHomePageLayoutView();
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
		},
		getNewDiagnoseLayoutView: function(model) {
			return new View.NewDiagnoseLayoutView({
				model: model
			});
		},
		getNewAuditLayoutView: function(model) {
			return new View.NewAuditLayoutView({
				model: model
			});
		}

	});

	return ShowController;

});