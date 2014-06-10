define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'admin/fenzhen/fz_view', 'utils/reqcmd', 'entities/diagnoseEntity', 'doctorhome/show/show_view'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DiagnoseEntity, DoctorHomeShowView) {
	// body...
	"use strict";
	var FzController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getFzPageLayoutView();

			this.show(this.layoutView, {
				name: "fenzhenPageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("fenzhenPageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("fenzhenPageLayoutView attached end");
				this.layoutView.attachEndHandler();
			}, this));


			ReqCmd.commands.setHandler("initAllDiagnoseView:FzPageLayoutView", Lodash.bind(function(params) {
				console.log("initAllDiagnoseView,params:" + params);
				if (this.allDiagnoseCollection) {
					DiagnoseEntity.API.getAdminAllDiagnose(params, this.allDiagnoseCollection);

				} else {
					this.allDiagnoseCollection = DiagnoseEntity.API.getAdminAllDiagnose(params);

				}
				// this.allDiagnoseCollection = DiagnoseEntity.API.getAdminAllDiagnose(params);

				if (this.allDiagnoseCollectionView) {
					this.allDiagnoseCollectionView.collection = this.allDiagnoseCollection;
				} else {
					this.allDiagnoseCollectionView = this.getAllDiagnoseCollectionView(this.allDiagnoseCollection);

				}
				// this.allDiagnoseCollectionView = this.getAllDiagnoseCollectionView(this.allDiagnoseCollection);

				this.show(this.allDiagnoseCollectionView, {
					region: this.layoutView.allDiagnoseTable,
					client: true
				});

			}, this));

			ReqCmd.commands.setHandler("initMyDiagnoseView:FzPageLayoutView", Lodash.bind(function(params) {
				console.log("initMyDiagnoseView,params:" + params);
				if (this.myDiagnoseCollection) {
					DiagnoseEntity.API.getAdminMyDiagnose(params, this.myDiagnoseCollection);

				} else {
					this.myDiagnoseCollection = DiagnoseEntity.API.getAdminMyDiagnose(params);

				}
				// this.myDiagnoseCollection = DiagnoseEntity.API.getAdminMyDiagnose(params);

				if (this.myDiagnoseCollectionView) {
					this.myDiagnoseCollectionView.collection = this.myDiagnoseCollection;
				} else {
					this.myDiagnoseCollectionView = this.getMyDiagnoseCollectionView(this.myDiagnoseCollection);
				}
				// this.myDiagnoseCollectionView = this.getMyDiagnoseCollectionView(this.myDiagnoseCollection);
				this.show(this.myDiagnoseCollectionView, {
					region: this.layoutView.myDiagnoseTable,
					client: true
				});

			}, this));

			//click get diagnose
			ReqCmd.reqres.setHandler("getDiagnoseLinkHandler:AdminAllDiagnoseItemView", Lodash.bind(function() {
				this.layoutView.initAllDiagnoseView();
				this.layoutView.initMyDiagnoseView();
			}, this));


			//doctor click the action link , e.g. add diagnose
			ReqCmd.commands.setHandler("DiagnoseTableItemView:actionHandler", Lodash.bind(function(model) {
				console.log("DiagnoseTableItemView actionHandler");
				var statusId = model.get('statusId');
				if (statusId == 4) {
					this.detailModel = DiagnoseEntity.API.getDiagnoseDetail({
						diagnoseId:model.get('id')
					});
					if (typeof this.diagnoseActionView !== 'undefined') {
						this.diagnoseActionView.close();
					}
					this.diagnoseActionView = this.getNewDiagnoseLayoutView(this.detailModel);

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



		},
		getFzPageLayoutView: function() {
			return new View.FzPageLayoutView();
		},
		getAllDiagnoseCollectionView: function(collection) {
			var view = new View.AdminAllDiagnoseCollectionView({
				collection: collection,
				itemView: View.AdminAllDiagnoseItemView
			})
			return view;
		},
		getMyDiagnoseCollectionView: function(collection) {
			var view = new View.AdminMyDiagnoseCollectionView({
				collection: collection,
				itemView: View.AdminMyDiagnoseItemView
			})
			return view;
		},
		getNewDiagnoseLayoutView: function(model) {
			return new DoctorHomeShowView.NewDiagnoseLayoutView({
				model: model,
				typeID:0

			});
		}

	});

	return FzController;

});