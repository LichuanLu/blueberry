define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap", 'bootstrap.select'], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var PatientHomePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init PatientHomePageLayoutView");
			this.bindUIElements();
		},
		regions: {
			"contentRegion": "#contentRegion"
		},
		el: "#patienthome-content",
		ui: {
			"patientActionLinks": "#patient-actions ul a",
			"headerTitle":"#patient-action-header h6"

		},
		events: {
			"click @ui.patientActionLinks": "patientActionLinksHandler"
		},
		attachEndHandler: function() {

			this.ui.patientActionLinks.filter("[name*='diagnoseLink']").click();
		},
		patientActionLinksHandler: function(e) {
			e.preventDefault();
			//e.stopPropagation();
			//console.dir($(e.target));
			var $target = $(e.target);
			if ($target.is('span')) {
				$target = $target.closest('a');
			}
			console.log($target.attr("name"));
			this.ui.patientActionLinks.removeClass('active');
			$target.addClass('active');
			ReqCmd.commands.execute("patientHomePageLayoutView:changeContentView", $target.attr("name"));

			//change title
			var iconClass = $target.attr('class');
			var titleText = $target.find('.nav-text').html();
			//console.log(iconClass+','+text);
			//console.dir(this.ui);
			this.ui.headerTitle.html("<i class='"+iconClass+"'></i><span>"+titleText+"</span>");



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

		},
		ui: {
			"submitBtn": "#patient-action-content .submit-btn",
			"typeSelect": "#patient-action-content select"
		},
		events: {
			"click @ui.submitBtn": "searchDiagnose"
		},
		template: "diagnoseLayout",
		itemViewContainer: "#diagnose-tbody",
		searchDiagnose: function(e) {
			e.preventDefault();
			ReqCmd.commands.execute("DiagnoseListView:searchDiagnose", this.ui.typeSelect.val());
		}

	});

	var DiagnoseTableItemView = Marionette.ItemView.extend({
		initialize: function() {},
		template: "diagnoseItem",

		onRender: function() {
			//console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);
		}


	});


	var AccountManageLayoutView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("AccountManageLayoutView init");

		},
		template: "patientAccountManageLayout",
		ui: {
			"editBtns": ".edit-btn",
			"editBlocks": "#patient-user-account-form .edit-block"
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

	return {
		PatientHomePageLayoutView: PatientHomePageLayoutView,
		DiagnoseListView: DiagnoseListView,
		DiagnoseTableItemView: DiagnoseTableItemView,
		AccountManageLayoutView: AccountManageLayoutView
	}
});