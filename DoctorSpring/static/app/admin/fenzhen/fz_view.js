define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap", 'bootstrap.select', 'bootstrap-treeview', 'flat_ui_custom', 'bootstrap.multiselect'], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var FzPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init FzPageLayoutView");
			this.bindUIElements();
		},
		regions: {
			"allDiagnoseTable": "#all-diagnose-tbody",
			"myDiagnoseTable": "#my-diagnose-tbody",
			"newDiagnoseRegion": "#newDiagnoseRegion"

		},
		el: "#admin-fenzhen-content",
		ui: {
			"doctorHospitalSelect": "#doctor-hospital-select",
			"diagnoseStatusSelect": "#diagnose-status-select",
			"allDiagnoseForm": "#all-apply-wrapper form",
			"myDiagnoseForm": "#my-apply-wrapper form",
			"allDiagnoseSearchBtn": "#all-apply-wrapper .submit-btn",
			"myDiagnoseSearchBtn": "#my-apply-wrapper .submit-btn"

		},
		events: {
			"click @ui.allDiagnoseSearchBtn": "allDiagnoseSearch",
			"click @ui.myDiagnoseSearchBtn": "myDiagnoseSearch"

		},
		allDiagnoseSearch: function(e) {
			e.preventDefault();
			this.initAllDiagnoseView();

		},
		myDiagnoseSearch: function(e) {
			e.preventDefault();
			this.initMyDiagnoseView();

		},
		attachEndHandler: function() {
			var $this = $(this);
			console.dir($('#fenzhenTab a'));
			$('#fenzhenTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});
			this.ui.doctorHospitalSelect.multiselect({
				numberDisplayed: 2,
				enableFiltering: true,
				filterPlaceholder: "搜索",
				nonSelectedText: "不限"
				// buttonWidth: '300px'
			});

			// this.ui.diagnoseStatusSelect.multiselect({
			// 	nonSelectedText: "没有选中"
			// 	// buttonWidth: '300px'
			// });


			$("select").not('.multiselect').selectpicker({
				style: 'btn-sm btn-primary',
				title: "没有选中"
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
			this.initAllDiagnoseView();
			this.initMyDiagnoseView();



		},
		initAllDiagnoseView: function() {
			var params = this.ui.allDiagnoseForm.serialize();
			ReqCmd.commands.execute("initAllDiagnoseView:FzPageLayoutView", params);

		},
		initMyDiagnoseView: function() {
			var params = this.ui.myDiagnoseForm.serialize();
			ReqCmd.commands.execute("initMyDiagnoseView:FzPageLayoutView", params);

		}
	});

	var AdminAllDiagnoseCollectionView = Marionette.CollectionView.extend({
		initialize: function() {},
		onRender: function() {
			console.log("AdminAllDiagnoseCollectionView render");


		},
		onShow: function() {
			console.log("AdminAllDiagnoseCollectionView onShow");
			//init the modal onshow
		},
		el: "#all-diagnose-tbody"
	});

	var AdminAllDiagnoseItemView = Marionette.ItemView.extend({
		template: "allDiagnoseItem",
		initialize: function() {
			console.log("AdminAllDiagnoseItemView init");
			this.listenTo(this.model, 'sync', this.render, this);


		},
		onRender: function() {
			console.log("AdminAllDiagnoseItemView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		ui: {
			"getDiagnoseLink": "#get-diagnose-link"
		},
		events: {
			"click @ui.getDiagnoseLink": "getDiagnoseLinkHandler"
		},
		getDiagnoseLinkHandler: function(e) {
			e.preventDefault();
			var diagnoseId = this.model.get('id');
			var that = this;
			if (diagnoseId) {
				$.ajax({
					url: '/admin/diagnose/update',
					data: "diagnoseId=" + diagnoseId,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							ReqCmd.reqres.request("getDiagnoseLinkHandler:AdminAllDiagnoseItemView");
							Messenger().post({
								message: 'SUCCESS.Get diagnose.',
								type: 'success',
								showCloseButton: true
							});
						}
					},
					onError: function(res) {
						if (res.status == 2) {
							window.location.replace('/loginPage')

						} else if (res.status == 4) {
							window.location.replace('/error')

						}
						this.resetForm();
						//var error = jQuery.parseJSON(data);
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "错误信息:" + res.msg,
								type: 'error',
								showCloseButton: true
							});
						}

					}
				});

			}

		}
	});

	var AdminMyDiagnoseCollectionView = Marionette.CollectionView.extend({
		initialize: function() {
			this.listenTo(this.collection, 'sync', this.render, this);
		},
		onRender: function() {
			console.log("AdminAllDiagnoseCollectionView render");
			// this.$el = this.$el.children();
			// this.setElement(this.$el);
		},
		onShow: function() {
			console.log("AdminAllDiagnoseCollectionView onShow");
			//init the modal onshow
		},
		el: "#my-diagnose-tbody"

	});

	var AdminMyDiagnoseItemView = Marionette.ItemView.extend({
		template: "myDiagnoseItem",
		initialize: function() {
			console.log("AdminMyDiagnoseItemView init");
			this.listenTo(this.model, 'sync', this.render, this);


		},
		onRender: function() {
			console.log("AdminMyDiagnoseItemView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		ui: {
			"startDiagnoseLink": "#start-diagnose-link"
		},
		events: {
			"click @ui.startDiagnoseLink": "startDiagnoseLinkHandler"
		},
		startDiagnoseLinkHandler: function(e) {
			e.preventDefault();
			ReqCmd.commands.execute("DiagnoseTableItemView:actionHandler", this.model);

		}

	});



	return {
		FzPageLayoutView: FzPageLayoutView,
		AdminAllDiagnoseCollectionView: AdminAllDiagnoseCollectionView,
		AdminAllDiagnoseItemView: AdminAllDiagnoseItemView,
		AdminMyDiagnoseCollectionView: AdminMyDiagnoseCollectionView,
		AdminMyDiagnoseItemView: AdminMyDiagnoseItemView



	}
});