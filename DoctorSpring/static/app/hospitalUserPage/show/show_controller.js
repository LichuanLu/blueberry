define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'hospitalUserPage/show/show_view', 'utils/reqcmd','entities/diagnoseEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd,DiagnoseEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getHospitalUserPageView();

			this.show(this.layoutView, {
				name: "hospitalUserPageView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("hospitalUserPageView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
			}, this));




			ReqCmd.commands.setHandler("initAllDiagnoseView:HospitalUserPageView", Lodash.bind(function(params) {
				console.log("initAllDiagnoseView,params:" + params);
				if (this.allDiagnoseCollection) {
					DiagnoseEntity.API.getHospitalUserAllDiagnose(params, this.allDiagnoseCollection);

				} else {
					this.allDiagnoseCollection = DiagnoseEntity.API.getHospitalUserAllDiagnose(params);

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

			ReqCmd.commands.setHandler("initUnFinishDiagnoseView:HospitalUserPageView", Lodash.bind(function() {
				// console.log("initMyDiagnoseView,params:" + params);
				if (this.unfinishDiagnoseCollection) {
					DiagnoseEntity.API.getHospitalUserUnfinishDiagnose(this.unfinishDiagnoseCollection);

				} else {
					this.unfinishDiagnoseCollection = DiagnoseEntity.API.getHospitalUserUnfinishDiagnose();

				}
				// this.myDiagnoseCollection = DiagnoseEntity.API.getAdminMyDiagnose(params);

				if (this.unfinishDiagnoseCollectionView) {
					this.unfinishDiagnoseCollectionView.collection = this.unfinishDiagnoseCollection;
				} else {
					this.unfinishDiagnoseCollectionView = this.getUnfinishDiagnoseCollectionView(this.unfinishDiagnoseCollection);
				}
				// this.myDiagnoseCollectionView = this.getMyDiagnoseCollectionView(this.myDiagnoseCollection);
				this.show(this.unfinishDiagnoseCollectionView, {
					region: this.layoutView.unfinishDiagnoseTable,
					client: true
				});

			}, this));



			console.log('follow controller init end');



		},
		getHospitalUserPageView: function(model) {
			var view = new View.HospitalUserPageView();
			return view;
		},
		getAllDiagnoseCollectionView: function(collection) {
			var view = new View.HospitalUserAllDiagnoseCollectionView({
				collection: collection,
				itemView: View.HospitalUserAllDiagnoseItemView
			})
			return view;
		},
		getUnfinishDiagnoseCollectionView: function(collection) {
			var view = new View.HospitalUserUnfinishDiagnoseCollectionView({
				collection: collection,
				itemView: View.HospitalUserUnfinishDiagnoseItemView
			})
			return view;
		}

	});

	return ShowController;

});