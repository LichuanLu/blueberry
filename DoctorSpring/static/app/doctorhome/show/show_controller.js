define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'doctorhome/show/show_view', 'utils/reqcmd', 'entities/diagnoseEntity', 'entities/messageEntity', 'message/show/show_view'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DiagnoseEntity, MessageEntity, MessageView) {
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

			

			//click left menu , change view , send from view 
			ReqCmd.commands.setHandler("doctorHomePageLayoutView:changeContentView", Lodash.bind(function(viewName) {
				console.log("doctorHomePageLayoutView changeContentView");
				this.changeContentView(viewName);
			}, this));

			//diagnose list , change type , click search, send from view
			ReqCmd.commands.setHandler("DiagnoseListView:searchDiagnose", Lodash.bind(function(params) {
				console.log("DiagnoseListView searchDiagnose");
				// var params = {
				// 	type: type
				// };
				console.dir(params);
				if(this.diagnoseCollection){
					DiagnoseEntity.API.getDiagnoseList(params,this.diagnoseCollection);

				}else{
					this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList(params);
				}
			}, this));

			//doctor click the action link , e.g. add diagnose
			ReqCmd.commands.setHandler("DiagnoseTableItemView:actionHandler", Lodash.bind(function(model) {
				console.log("DiagnoseTableItemView actionHandler");
				var statusId = model.get('statusId');
				if (statusId == 5) {
					this.detailModel = DiagnoseEntity.API.getDiagnoseDetail({
						diagnoseId:model.get('id')
					});
					if (typeof this.diagnoseActionView !== 'undefined') {
						this.diagnoseActionView.close();
					}
					this.diagnoseActionView = this.getNewDiagnoseLayoutView(this.detailModel);

				} else if (statusId == '审核') {
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
				this.contentView.initDiagnoseListView();

			}, this));



			//show message list after layout show
			ReqCmd.reqres.setHandler("showMessageList:MessageLayoutView", Lodash.bind(function() {

				this.unreadMessageCollection = MessageEntity.API.getMessageList({
					status:0
				});
				this.unreadMessageCollectionView = this.getMessageListView(this.unreadMessageCollection);
				this.show(this.unreadMessageCollectionView, {
					region: this.contentView.unReadMessageRegion,
					client: true
				});

				this.readMessageCollection = MessageEntity.API.getMessageList({
					status:2
				});
				this.readMessageCollectionView = this.getMessageListView(this.readMessageCollection);
				this.show(this.readMessageCollectionView, {
					region: this.contentView.readMessageRegion,
					client: true
				});


			}, this));

			console.log('follow controller init end');

		},
		changeContentView: function(viewName) {
			if (typeof this.diagnoseActionView !== 'undefined') {
				this.diagnoseActionView.close();
			}
			if (viewName === 'diagnoseLink') {
				this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList({
					type:5
				});
				this.contentView = this.getDiagnoseListView(this.diagnoseCollection);

			} else if (viewName === 'accountLink') {
				this.contentView = this.getAccountManageLayoutView();
			} else if (viewName === 'messageLink') {
				this.contentView = this.getMessageLayoutView();
			} else if (viewName === 'consultLink') {
				this.contentView = this.getConsultLayoutView();
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
				model: model,
				typeID:1
			});
		},
		getNewAuditLayoutView: function(model) {
			return new View.NewAuditLayoutView({
				model: model
			});
		},
		getMessageLayoutView: function() {
			return new View.MessageLayoutView();
		},
		getMessageListView: function(collection) {
			return new MessageView.MessageListView({
				collection: collection,
				itemView: MessageView.MessageItemView
			});
		},
		getConsultLayoutView: function() {
			return new View.ConsultLayoutView();

		}

	});

	return ShowController;

});