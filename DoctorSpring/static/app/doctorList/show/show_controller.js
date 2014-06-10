define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'doctorList/show/show_view', 'utils/reqcmd','entities/doctorEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd,DoctorEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getDoctorListLayoutView();

			this.show(this.layoutView, {
				name: "doctorListLayoutView",
				//as bindAll this,so don't need that
				instance: this
			});

			//instance is this controller instance
			ReqCmd.commands.setHandler("doctorListLayoutView:attached", Lodash.bind(function(instance) {
				console.log("attached end");
				this.layoutView.attachEndHandler();
				this.doctorPageModel = DoctorEntity.API.getDoctorPageModel();
				this.doctorListView = this.getDoctorListView(this.doctorPageModel);
				//console.log(this.modalView.doctorListRegion);
				this.show(this.doctorListView, {
					region: this.layoutView.doctorListRegion,
					client: true

				});
			},this));


			//refresh select doctor table
			ReqCmd.commands.setHandler("SelectDoctorModalView:searchDoctorHandler", Lodash.bind(function(params) {
				console.log("SelectDoctorModalView searchDoctorHandler");
				this.doctorPageModel = DoctorEntity.API.getDoctorPageModel(params);
				this.doctorListView = this.getDoctorListView(this.doctorPageModel);
				//console.log(this.modalView.doctorListRegion);
				this.show(this.doctorListView, {
					region: this.layoutView.doctorListRegion,
					client: true
				});

			}, this));


			//handle when doctor collection fetched
			ReqCmd.reqres.setHandler("doctorPageModel:fetched", Lodash.bind(function() {
				console.log("doctorPageModel:fetched controller");
				var doctors = this.doctorPageModel.get('doctor');
				console.dir(this.doctorPageModel);
				this.doctorListView.collection = new DoctorEntity.DoctorCollection(doctors);
				this.doctorListView.render();
			}, this));
			
			console.log('follow controller init end');




		},
		getDoctorListLayoutView: function() {
			return new View.DoctorListLayoutView();
		},
		getDoctorListView: function(model) {
			var view = new View.DoctorDetailListView({
				model: model,
				itemView: View.DoctorDetailItemView
			});
			return view;
		}

	});

	return ShowController;

});