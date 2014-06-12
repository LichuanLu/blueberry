define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap", 'bootstrap.select', 'bootstrap-treeview', 'flat_ui_custom'], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	//var $;
	var DoctorHomePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorHomePageLayoutView");
			this.bindUIElements();
		},
		regions: {
			"contentRegion": "#contentRegion",
			"newDiagnoseRegion": "#newDiagnoseRegion"
		},
		el: "#doctorhome-content",
		ui: {
			"doctorActionLinks": "#doctor-actions ul a",
			"headerTitle": "#doctor-action-header h6"

		},
		events: {
			"click @ui.doctorActionLinks": "doctorActionLinksHandler"
		},
		attachEndHandler: function() {

			this.ui.doctorActionLinks.filter("[name*='diagnoseLink']").click();
		},
		doctorActionLinksHandler: function(e) {
			e.preventDefault();
			//e.stopPropagation();
			//console.dir($(e.target));
			var $target = $(e.target);
			if ($target.is('span')) {
				$target = $target.closest('a');
			}
			console.log($target.attr("name"));
			this.ui.doctorActionLinks.removeClass('active');
			$target.addClass('active');
			ReqCmd.commands.execute("doctorHomePageLayoutView:changeContentView", $target.attr("name"));

			//change title
			var iconClass = $target.attr('class');
			var titleText = $target.find('.nav-text').html();
			//console.log(iconClass+','+text);
			//console.dir(this.ui);
			this.ui.headerTitle.html("<i class='" + iconClass + "'></i><span>" + titleText + "</span>");

		}

	});

	var DiagnoseListView = Marionette.CompositeView.extend({
		initialize: function() {
			console.log("init DiagnoseTableCollectionView");
		},
		onShow: function() {
			$("select").selectpicker({
				style: 'btn-sm btn-primary'
			});

			var $datepickerSelector = $("#startDateinput,#endDateinput");
			$datepickerSelector.each(function() {
				$(this).datepicker({
					showOtherMonths: true,
					selectOtherMonths: true,
				}).prev('.btn').on('click', function(e) {
					e && e.preventDefault();
					$(this).focus();
				});
				$.extend($.datepicker, {
					_checkOffset: function(inst, offset, isFixed) {
						return offset
					}
				});

				// Now let's align datepicker with the prepend button
				$(this).datepicker('widget').css({
					'margin-left': -$(this).prev('.input-group-btn').find('.btn').outerWidth()
				});

			});



		},
		ui: {
			"submitBtn": "#doctor-action-content .submit-btn",
			"typeSelect": "#doctor-action-content select"
		},
		events: {
			"click @ui.submitBtn": "searchDiagnose"
		},
		template: "doctorDiagnoseLayout",
		itemViewContainer: "#diagnose-tbody",
		searchDiagnose: function(e) {
			e.preventDefault();
			ReqCmd.commands.execute("DiagnoseListView:searchDiagnose", $('#doctor-action-content').find('.form-inline').serialize());
		}

	});

	var DiagnoseTableItemView = Marionette.ItemView.extend({
		initialize: function() {},
		template: "doctorDiagnoseItem",
		ui: {
			"actionLinks": ".action-group a"
		},
		events: {
			"click @ui.actionLinks": "actionHandler"
		},
		onRender: function() {
			//console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);
		},
		actionHandler: function(e) {
			var statusId = this.model.get('statusId');
			if (statusId != 6) {
				e.preventDefault();
				ReqCmd.commands.execute("DiagnoseTableItemView:actionHandler", this.model);
			}

		}


	});

	//manage account view
	var AccountManageLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("AccountManageLayoutView init");

		},
		template: "doctorAccountManageLayout",
		ui: {
			"editBtns": ".edit-btn",
			"editBlocks": "#doctor-user-account-form .edit-block"
		},
		events: {
			"click @ui.editBtns": "editFormHandler"
		},
		editFormHandler: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			$target.hide();
			$target.siblings('.edit-block').show();

		},
		onRender: function() {
			this.ui.editBlocks.hide();

		},

		onShow: function() {
			var $this = $(this);
			console.dir($('#accountTab a'));
			$('#accountTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});
		}
	});


	//consult  view
	var ConsultLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("ConsultLayoutView init");

		},
		template: "doctorConsultLayout",
		ui: {

		},
		events: {},
		onRender: function() {},
		onShow: function() {
			var $this = $(this);
			console.dir($('#accountTab a'));
			$('#consultTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});
		}
	});

	var NewDiagnoseLayoutView = Marionette.ItemView.extend({
		initialize: function(options) {
			console.log("init NewDiagnoseLayoutView");
			this.typeId = options.typeId;
			this.listenTo(this.model, 'sync', this.render, this);
			//tree data
			this.treedata = {};
			this.selectedTemplateNode = "";
			// this.bindUIElements();
		},
		template: "newDiagnoseLayout",
		ui: {
			"loadTemplateBtn": ".load-btn",
			"loadingBtn": ".loading-btn",
			"imageDesTextArea": "#imageDes",
			"diagnoseResultTextArea": "#diagnoseResult",
			"closeLink": ".close-link",
			"submitDiagnoseBtn": '.submit-btn',
			"techDesTextArea": "#techDes"
		},
		events: {
			"click @ui.loadTemplateBtn": "loadTemplate",
			"click @ui.closeLink": "closeRegion",
			"click @ui.submitDiagnoseBtn": "submitDiagnose"
		},
		editFormHandler: function(e) {

		},
		submitDiagnose: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var targetId = $target.attr("id");
			var $newDiagnoseForm = $('#new-diagnose-form');
			//console.log(targetId);
			var status;
			if (targetId === 'saveDiagnoseBtn') {
				status = 0;
			} else if (targetId === 'previewDiagnoseBtn') {
				status = 0;
			} else if (targetId === 'submitDiagnoseBtn') {
				status = 2;
			}
			if (status !== 'undefined') {
				var data = $newDiagnoseForm.serialize() + "&status=" + status + "&diagnoseId=" + this.model.get('id');
				var reportId = $newDiagnoseForm.data('report-id');
				var type = this.typeId;
				if (reportId) {
					data += "&reportId=" + reportId;
				}
				if (type) {
					data += "&type=" + type;
				}
				var url;
				if(window.location.href.indexOf('fenzhen') > -1){
					console.log('admin fenzhen page');
					url = '/admin/report/addOrUpate';

				}else{
					url = '/doctor/report/update';

				}
				var that = this;
				$.ajax({
					url: url,
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							if(targetId === 'previewDiagnoseBtn'){
								window.open ('/diagnose/'+that.model.get('id')+'/pdf','_blank');
							}
							Messenger().post({
								message: 'SUCCESS.Create diagnose',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						this.resetForm();
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


		},
		onRender: function() {

		},
		closeRegion: function(e) {
			e.preventDefault();
			ReqCmd.reqres.request("NewDiagnoseLayoutView:closeRegion");
		},
		loadTemplate: function(e) {
			e.preventDefault();
			if (this.selectedTemplateNode) {
				if (this.selectedTemplateNode.imageDesc && this.selectedTemplateNode.diagnoseDesc) {
					this.ui.imageDesTextArea.val(this.selectedTemplateNode.imageDesc);
					this.ui.diagnoseResultTextArea.val(this.selectedTemplateNode.diagnoseDesc);
				}

				// that.ui.techDesTextArea.val(data.techDes);

			}

			// var $templateLi = $('#tree ul').find('.node-selected');
			// var text = $templateLi.text();

			//var that = this;
			// if (href !== '#') {
			// 	this.ui.loadTemplateBtn.hide();
			// 	this.ui.loadingBtn.show();
			// 	var data = 'templateId=' + href;
			// 	$.ajax({
			// 		url: '/diagnose/template',
			// 		data: data,
			// 		dataType: 'json',
			// 		type: 'GET',
			// 		success: function(data) {
			// 			if (data.status != 0) {
			// 				this.onError(data);

			// 			} else {
			// 				Messenger().post({
			// 					message: 'SUCCESS. Product import started. Check back periodically.',
			// 					type: 'success',
			// 					showCloseButton: true
			// 				});
			// 				this.setTemplate(data.data);

			// 			}
			// 		},
			// 		onError: function(res) {
			// 			this.resetForm();
			// 			//var error = jQuery.parseJSON(data);
			// 			if (typeof res.msg !== 'undefined') {
			// 				Messenger().post({
			// 					message: "%ERROR_MESSAGE:" + res.msg,
			// 					type: 'error',
			// 					showCloseButton: true
			// 				});
			// 			}

			// 		},
			// 		setTemplate: function(data) {
			// 			if (data) {
			// 				that.ui.imageDesTextArea.val(data.imageDes);
			// 				that.ui.diagnoseResultTextArea.val(data.diagnoseResult);
			// 				that.ui.techDesTextArea.val(data.techDes);
			// 				this.resetForm();
			// 			}

			// 		},
			// 		resetForm: function() {
			// 			that.ui.loadTemplateBtn.show();
			// 			that.ui.loadingBtn.hide();
			// 		}
			// 	});

			// }

		},
		onShow: function() {
			// console.log(this.ui.templateLinks);
			// 	var data = [{
			// 		text: "CT",
			// 		nodes: [{
			// 			text: "呼吸系统",
			// 			nodes: [{
			// 				text: "心肺未见异常"
			// 			}, {
			// 				text: "右肺上叶干酪性肺炎并右肺下叶播放"

			// 			}]
			// 		}, {
			// 			text: "骨关节病变",
			// 			nodes: [{
			// 				text: "心肺未见异常"
			// 			}, {
			// 				text: "右肺上叶干酪性肺炎并右肺下叶播放"
			// 			}]
			// 		}]
			// 	}, {
			// 		text: "MR",
			// 		nodes: [{
			// 			text: "呼吸系统",
			// 			nodes: [{
			// 				text: "心肺未见异常"
			// 			}, {
			// 				text: "右肺上叶干酪性肺炎并右肺下叶播放"

			// 			}]
			// 		}, {
			// 			text: "骨关节病变",
			// 			nodes: [{
			// 				text: "心肺未见异常"
			// 			}, {
			// 				text: "右肺上叶干酪性肺炎并右肺下叶播放"
			// 			}]
			// 		}]
			// 	}];

			// 	$('#tree').treeview({
			// 		data: data,
			// 		enableLinks: true
			// 		// showBorder:false
			// 	});
		},
		onDomRefresh: function() {
			this.treedata = [{
				text: "ct"
			}, {
				text: "mri"
			}];
			this.refreshTree(this.treedata);
			var that = this;

			$('#tree').on('nodeSelected', function(event, node) {
				//console.dir(node);
				var nodeText = node.text;
				var nodeParent = node.parent;
				that.selectedTemplateNode = node;

				if (nodeText === 'ct' || nodeText === 'mri') {
					var targetObj = Lodash.find(that.treedata, {
						'text': nodeText
					});
					if (!Lodash.has(targetObj, 'nodes')) {

						$.ajax({
							url: '/diagnoseTemplate/postionList',
							data: "diagnoseMethod=" + nodeText,
							dataType: 'json',
							type: 'GET',
							success: function(data) {
								if (data.status != 0) {
									this.onError(data);

								} else {
									// var targetObj = Lodash.find(that.treedata, {'text': nodeText});
									targetObj.nodes = this.parseResult(data.data, nodeText);
									console.dir(targetObj);
									that.refreshTree();
									Messenger().post({
										message: 'SUCCESS.Get diagnose template.',
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

							},
							parseResult: function(data, parent) {
								var resArr = [];
								Lodash(data).forEach(function(res) {
									var obj = {
										text: res,
										parent: parent
									};
									resArr.push(obj);
								});
								return resArr;

							}
						});
					}


				} else if (!node.last) {
					// var targetObj = Lodash.find(that.treedata, {
					// 	'text': nodeText
					// });
					var targetObj;
					if (nodeParent == 'ct') {
						targetObj = Lodash.find(that.treedata[0].nodes, {
							'text': nodeText
						});
					} else if (nodeParent == 'mri') {
						targetObj = Lodash.find(that.treedata[1].nodes, {
							'text': nodeText
						});
					}

					if (!Lodash.has(targetObj, 'nodes')) {

						$.ajax({
							url: '/diagnoseTemplate/diagnoseAndImageDesc',
							data: "diagnoseMethod=" + node.parent + "&diagnosePostion=" + nodeText,
							dataType: 'json',
							type: 'GET',
							success: function(data) {
								if (data.status != 0) {
									this.onError(data);

								} else {
									targetObj.nodes = this.parseResult(data.data);
									console.dir(targetObj);
									that.refreshTree();
									Messenger().post({
										message: 'SUCCESS.Get diagnose template.',
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

							},
							parseResult: function(data) {
								Lodash(data).forEach(function(res) {
									res.text = res.diagnoseDesc;
									res.last = true;
								});
								return data;
							}
						});
					}

				}
				// else if(node.last){
				// 	that.selectedTemplateNode = node;
				// }



			});
		},
		refreshTree: function(data) {
			var treedata;
			if (data) {
				treedata = data;
			} else {
				treedata = this.treedata;
			}
			$('#tree').treeview({
				data: treedata,
				enableLinks: false
				// showBorder:false
			});
		}
	});

	var NewAuditLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init NewAuditLayoutView");
			this.listenTo(this.model, 'sync', this.render, this);

		},
		template: "newAuditLayout",
		ui: {

			"auditTextArea": "#auditText",
			"closeLink": ".close-link",
			"submitAuditBtn": '.submit-btn'
		},
		events: {
			"click @ui.closeLink": "closeRegion",
			"click @ui.submitAuditBtn": "submitAudit"
		},
		editFormHandler: function(e) {},
		submitAudit: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var targetId = $target.attr("id");
			//console.log(targetId);
			var type;
			if (targetId === 'saveAuditBtn') {
				type = 0;
			} else if (targetId === 'previewAuditBtn') {
				type = 1;
			} else if (targetId === 'submitAuditBtn') {
				type = 2;
			}


			if (type !== 'undefined') {
				var data = $('#new-audit-form').serialize() + "&type=" + type + "&diagnoseId=" + this.model.get('id');
				$.ajax({
					url: '/doctor/audit/create',
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						this.resetForm();
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


		},
		closeRegion: function(e) {
			e.preventDefault();
			ReqCmd.reqres.request("NewDiagnoseLayoutView:closeRegion");
		}
	});

	var MessageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("MessageLayoutView init");

		},
		template: "doctorMessageLayout",
		ui: {},
		regions: {
			"unReadMessageRegion": "#unread-message-region",
			"readMessageRegion": "#read-message-region"
		},
		events: {},
		onRender: function() {},
		onShow: function() {
			var $this = $(this);
			console.dir($('#messageTab a'));
			$('#messageTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});
			ReqCmd.reqres.request('showMessageList:MessageLayoutView');
		}
	});

	return {
		DoctorHomePageLayoutView: DoctorHomePageLayoutView,
		DiagnoseListView: DiagnoseListView,
		DiagnoseTableItemView: DiagnoseTableItemView,
		AccountManageLayoutView: AccountManageLayoutView,
		NewDiagnoseLayoutView: NewDiagnoseLayoutView,
		NewAuditLayoutView: NewAuditLayoutView,
		MessageLayoutView: MessageLayoutView,
		ConsultLayoutView: ConsultLayoutView
	}
});