define(['lodash', 'config/base/constant', 'config/controllers/_base_controller', 'patienthome/show/show_view', 'utils/reqcmd', 'entities/diagnoseEntity', 'entities/messageEntity', 'message/show/show_view', 'entities/favoriteEntity'], function(Lodash, CONSTANT, BaseController, View, ReqCmd, DiagnoseEntity, MessageEntity, MessageView, FavoriteEntity) {
	// body...
	"use strict";
	var ShowController = BaseController.extend({
		initialize: function() {

			this.layoutView = this.getPatientHomePageLayoutView();
			this.appInstance = require('app');

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
				if (this.diagnoseCollection) {
					DiagnoseEntity.API.getDiagnoseList(params, this.diagnoseCollection);

				} else {
					this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList(params);
				}
			}, this));

			//show message list after layout show
			ReqCmd.reqres.setHandler("showMessageList:MessageLayoutView", Lodash.bind(function() {

				this.unreadMessageCollection = MessageEntity.API.getMessageList({
					status: 0
				});
				this.unreadMessageCollectionView = this.getMessageListView(this.unreadMessageCollection);
				this.show(this.unreadMessageCollectionView, {
					region: this.contentView.unReadMessageRegion,
					client: true
				});

				this.readMessageCollection = MessageEntity.API.getMessageList({
					status: 1
				});
				this.readMessageCollectionView = this.getMessageListView(this.readMessageCollection);
				this.show(this.readMessageCollectionView, {
					region: this.contentView.readMessageRegion,
					client: true
				});


			}, this));


			//提交sharing
			ReqCmd.commands.setHandler("submitSharing:SharingModalView", Lodash.bind(function(data) {
				var that = this;
				$.ajax({
					url: '/addDiagnoseComment.json',
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							that.appInstance.modalRegion.close();
							Messenger().post({
								message: 'SUCCESS.Submit sharing.',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						//var error = jQuery.parseJSON(data);
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.msg,
								type: 'error',
								showCloseButton: true
							});
						}

					}
				});

			}, this));

			//after favorite layout show, init favorite list
			ReqCmd.reqres.setHandler("onShow:FavoriteLayoutView", Lodash.bind(function() {
				var userId = $('#patienthome-content').data('userid');
				if (userId) {
					this.favoriteDoctorCollection = FavoriteEntity.API.getFavoriteList({
						type: 0
					}, userId);

					this.favoriteDoctorCollectionView = this.getFavoriteListView(this.favoriteDoctorCollection);
					this.show(this.favoriteDoctorCollectionView, {
						region: this.contentView.doctorListRegion,
						client: true
					});

				}

			}, this));


			//confirm remove favorite
			ReqCmd.commands.setHandler("removeFavorite:CancelFavoriteModalView", Lodash.bind(function(model) {
				var that = this;
				var favoriteId = model.get('id');
				if (favoriteId) {
					$.ajax({
						url: '/userFavorties/' + favoriteId + '/cancel',
						dataType: 'json',
						type: 'POST',
						success: function(data) {
							if (data.status != 0) {
								this.onError(data);

							} else {
								that.appInstance.modalRegion.close();
								//delete the view from collection
								that.favoriteDoctorCollection.remove(model);
								Messenger().post({
									message: 'SUCCESS.remove favorite.',
									type: 'success',
									showCloseButton: true
								});
							}
						},
						onError: function(res) {
							//var error = jQuery.parseJSON(data);
							if (typeof res.msg !== 'undefined') {
								Messenger().post({
									message: "%ERROR_MESSAGE:" + res.msg,
									type: 'error',
									showCloseButton: true
								});
							}

						}
					});

				}


			}, this));

			//click detail at diagnose list item
			ReqCmd.commands.setHandler("detailLinksHandler:DiagnoseTableItemView", Lodash.bind(function(model) {
				this.contentView.hideView();
				// $('#diagnose-detail-track-wrapper').show();
				var params = "diagnoseId="+model.get('id');
				var diagnosePatientDetailModel = DiagnoseEntity.API.getDiagnosePatientDetail(params);

				this.diagnoseDetailTrackLayoutView = this.getDetailTrackLayoutView(diagnosePatientDetailModel);
				this.show(this.diagnoseDetailTrackLayoutView, {
					region: this.layoutView.diagnoseDetailTrackRegion,
					client: true
				});


			}, this));

			//click back link ,back to diagnose list from detail page
			ReqCmd.reqres.setHandler("backLinkHandler:DetailTrackLayoutView", Lodash.bind(function() {
				this.layoutView.diagnoseDetailTrackRegion.close();
				this.contentView.showAndRefreshView();

			}, this));




			console.log('show controller init end');

		},
		changeContentView: function(viewName) {
			this.layoutView.diagnoseDetailTrackRegion.close();

			if (viewName === 'diagnoseLink') {
				this.diagnoseCollection = DiagnoseEntity.API.getDiagnoseList();
				this.contentView = this.getDiagnoseListView(this.diagnoseCollection);

			} else if (viewName === 'accountLink') {
				this.contentView = this.getAccountManageLayoutView();
			} else if (viewName === 'messageLink') {
				this.contentView = this.getMessageLayoutView();
			} else if (viewName === 'favoritesLink') {
				this.contentView = this.getFavoriteLayoutView();
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
		getFavoriteLayoutView: function() {
			return new View.FavoriteLayoutView();
		},
		getFavoriteListView: function(collection) {
			var view = new View.FavoriteCollectionView({
				collection: collection,
				itemView: View.FavoriteItemView
			});
			return view;
		},
		getDetailTrackLayoutView: function(model) {
			return new View.DetailTrackLayoutView({
				model: model
			});

		}

	});

	return ShowController;

});