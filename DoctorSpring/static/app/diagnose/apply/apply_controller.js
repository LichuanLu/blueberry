define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'diagnose/apply/apply_view', 'utils/reqcmd', 'entities/doctorEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DoctorEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getApplyDiagnosePageLayoutView();
			this.modalView = this.getSelectDoctorModalView();


			this.show(this.layoutView, {
				name: "applyDiagnosePageLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			this.show(this.modalView, {
				name: "selectDoctorModalView",
				//as bindAll this,so don't need that
				instance: this
			});

			ReqCmd.commands.setHandler("selectDoctorModalView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.doctorPageModel = DoctorEntity.API.getDoctorPageModel();
				this.doctorListView = this.getDoctorListView(this.doctorPageModel);
				//console.log(this.modalView.doctorListRegion);
				this.show(this.doctorListView, {
					region: this.modalView.doctorListRegion,
					client: true

				});


				// var that = this;
				// $('#select-doctor-modal').on('shown.bs.modal', function(e) {
				// 	console.log("modal shown");
				// 	that.doctorPageModel = DoctorEntity.API.getDoctorPageModel();
				// 	that.doctorListView = that.getDoctorListView(that.doctorPageModel);
				// 	console.log(that.modalView.doctorListRegion);
				// 	that.show(that.doctorListView,{
				// 		region: that.modalView.doctorListRegion,
				// 		client: true

				// 	});
				// });


			}, this));

			//refresh select doctor table
			ReqCmd.commands.setHandler("SelectDoctorModalView:searchDoctorHandler", Lodash.bind(function(params) {
				console.log("SelectDoctorModalView searchDoctorHandler");
				this.doctorPageModel = DoctorEntity.API.getDoctorPageModel(params);
				this.doctorListView = this.getDoctorListView(this.doctorPageModel);
				//console.log(this.modalView.doctorListRegion);
				this.show(this.doctorListView, {
					region: this.modalView.doctorListRegion,
					client: true

				});


			}, this));



			//instance is this controller instance
			ReqCmd.commands.setHandler("applyDiagnosePageLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();

			}, this));


			//handle when doctor collection fetched
			ReqCmd.reqres.setHandler("doctorPageModel:fetched", Lodash.bind(function() {
				console.log("doctorPageModel:fetched controller");
				var doctors = this.doctorPageModel.get('doctor')
				console.dir(this.doctorPageModel);
				this.doctorListView.collection = new DoctorEntity.DoctorCollection(doctors);
				this.doctorListView.render();
			}, this));

			//handle recommaned doctor
			ReqCmd.reqres.setHandler("ApplyDiagnosePageLayoutView:getRecommandedDoctor", Lodash.bind(function() {
				this.recommandedDoctorModel = DoctorEntity.API.getRecommandedDoctorModel();
				this.recommandedDoctorView = this.getRecommandedDoctorView(this.recommandedDoctorModel);
				this.show(this.recommandedDoctorView, {
					region: this.layoutView.recommandedDoctorRegion,
					client: true

				});
			}, this));

			ReqCmd.reqres.setHandler("recommandedDoctorModel:fetched", Lodash.bind(function() {
				//this.recommandedDoctorView.render();
			}, this));


			//recommanded doctor
			ReqCmd.commands.setHandler("selectDoctorItemView:chooseDoctor",Lodash.bind(function(model) {
				console.log("SelectDoctorItemView:chooseDoctor");
				this.recommandedDoctorView.model = model;
				this.recommandedDoctorView.render();
			}, this));



			console.log('follow controller init end');

		},
		getApplyDiagnosePageLayoutView: function() {
			return new View.ApplyDiagnosePageLayoutView();
		},
		getDoctorListView: function(model) {
			var view = new View.SelectDoctorListView({
				model: model,
				itemView: View.SelectDoctorItemView
			});
			return view;
		},
		getSelectDoctorModalView: function() {
			var that = this;
			return new View.SelectDoctorModalView({
				controllerInstance: that
			});
		},
		getRecommandedDoctorView: function(model) {
			console.dir(model);
			return new View.SelectDoctorItemView({
				model:model
			});
		}

	});

	return ShowController;

});