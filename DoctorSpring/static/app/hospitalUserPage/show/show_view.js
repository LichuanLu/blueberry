define(['utils/reqcmd', 'lodash', 'marionette', 'templates','patienthome/show/show_view','dust', 'dustMarionette', "bootstrap",'bootstrap.select'], function(ReqCmd, Lodash, Marionette, Templates,PatientHomeShowView) {
	// body...
	"use strict";
	var HospitalUserPageView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init HospitalUserPageView");
			this.bindUIElements();
		},
		regions: {
			"allDiagnoseTable": "#submitted-diagnose-tbody",
			"unfinishDiagnoseTable": "#notsubmit-diagnose-tbody"
		},
		el: "#hospital-user-content",
		ui: {
			"allDiagnoseForm": "#submitted-diagnose-wrapper form",
			"allDiagnoseSearchBtn": "#submitted-diagnose-wrapper .submit-btn",
		},
		events: {
			"click @ui.allDiagnoseSearchBtn": "allDiagnoseSearch"

		},
		attachEndHandler: function() {
			$('#hospitalUserTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});

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

			this.initUnFinishDiagnoseView();
			this.initAllDiagnoseView();

		},
		initUnFinishDiagnoseView: function() {
			// var params = this.ui.allDiagnoseForm.serialize();
			ReqCmd.commands.execute("initUnFinishDiagnoseView:HospitalUserPageView");

		},
		initAllDiagnoseView: function() {
			var params = this.ui.allDiagnoseForm.serialize();
			ReqCmd.commands.execute("initAllDiagnoseView:HospitalUserPageView", params);

		},
		allDiagnoseSearch: function(e) {
			e.preventDefault();
			this.initAllDiagnoseView();

		}

	});



	var HospitalUserAllDiagnoseCollectionView = Marionette.CollectionView.extend({
		initialize: function() {},
		onRender: function() {
			console.log("HospitalUserAllDiagnoseCollectionView render");


		},
		onShow: function() {
			console.log("HospitalUserAllDiagnoseCollectionView onShow");
			//init the modal onshow
		},
		el: "#submitted-diagnose-tbody"
	});

	var HospitalUserAllDiagnoseItemView = Marionette.ItemView.extend({
		template: "hospitalUserSubmittedDiagnoseItem",
		initialize: function() {
			console.log("HospitalUserAllDiagnoseItemView init");
			this.listenTo(this.model, 'sync', this.render, this);


		},
		onRender: function() {
			console.log("HospitalUserAllDiagnoseItemView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		ui: {
		},
		events: {
		}
	});

	var HospitalUserUnfinishDiagnoseCollectionView = Marionette.CollectionView.extend({
		initialize: function() {
			this.listenTo(this.collection, 'sync', this.render, this);
			this.appInstance = require('app');
		},
		onRender: function() {
			console.log("HospitalUserUnfinishDiagnoseCollectionView render");
			// this.$el = this.$el.children();
			// this.setElement(this.$el);
		},
		onShow: function() {
			console.log("HospitalUserUnfinishDiagnoseCollectionView onShow");
			//init the modal onshow
		},
		el: "#notsubmit-diagnose-tbody",
		itemViewOptions: function() {
			return {
				parentsInstance: this
			};
		}

	});

	var HospitalUserUnfinishDiagnoseItemView = Marionette.ItemView.extend({
		
		template: "hospitalUserDiagnoseItem",
		initialize: function(options) {
			console.log("HospitalUserUnfinishDiagnoseItemView init");
			this.listenTo(this.model, 'sync', this.render, this);
			this.parentsInstance = options.parentsInstance;



		},
		onRender: function() {
			console.log("HospitalUserUnfinishDiagnoseItemView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		ui: {
			"deleteLinks":".rm-diagnose-link"
		},
		events: {
			"click @ui.deleteLinks": "deleteDiagnose"

		},
		deleteDiagnose: function(e) {
			e.preventDefault();
			var $link = $(e.target);
			if ($link.is('.rm-diagnose-link')) {
				console.log("rm-diagnose-link click");
				var model = this.model;
				var deleteDiagnoseModalView = new PatientHomeShowView.DeleteDiagnoseModalView({
					model: model
				});

				this.parentsInstance.appInstance.modalRegion.show(deleteDiagnoseModalView);

			}

		}

	});


	return {
		HospitalUserPageView: HospitalUserPageView,
		HospitalUserAllDiagnoseCollectionView:HospitalUserAllDiagnoseCollectionView,
		HospitalUserAllDiagnoseItemView:HospitalUserAllDiagnoseItemView,
		HospitalUserUnfinishDiagnoseCollectionView:HospitalUserUnfinishDiagnoseCollectionView,
		HospitalUserUnfinishDiagnoseItemView:HospitalUserUnfinishDiagnoseItemView
	}
});