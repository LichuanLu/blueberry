define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var KfPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init KfPageLayoutView");
			this.bindUIElements();
		},
		regions: {

		},
		el: "#admin-kefu-content",
		ui: {
			"payLink": ".pay-link",
			"confirmRegisterLink": ".confirm-register"

		},
		events: {
			'click @ui.payLink': "payLinkHandler",
			'click @ui.confirmRegisterLink': "confirmRegister"
		},
		confirmRegister: function(e) {
			e.preventDefault();
			var userid = $(e.target).closest('tr').data('userid');
			if (userid) {
				var that = this;
				$.ajax({
					url: '/doctor/register/confirm',
					data: "userid=" + userid,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							Messenger().post({
								message: 'SUCCESS.register confirm.',
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


		},
		payLinkHandler: function(e) {
			e.preventDefault();
			var diagnoseId = $(e.target).closest('tr').data('id');
			if (diagnoseId) {
				var that = this;
				$.ajax({
					url: '/diagnose/paylink',
					data: "diagnoseId=" + diagnoseId,
					dataType: 'json',
					type: 'GET',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							ReqCmd.commands.execute('payLinkHandler:KfPageLayoutView', data.data);
							Messenger().post({
								message: 'SUCCESS.Get diagnose.',
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
		},
		attachEndHandler: function() {
			var $this = $(this);
			console.dir($('#kefuTab a'));
			$('#kefuTab a').click(function(e) {
				e.preventDefault();
				$(this).tab('show');
			});


		}
	});

	var DisplayPayLinkModalView = Marionette.ItemView.extend({
		template: "displayPayLinkModal",
		initialize: function() {
			console.log("DisplayPayLinkModalView init");

		},
		onRender: function() {
			console.log("DisplayPayLinkModalView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		onShow: function() {},
		ui: {},
		events: {}
	});

	return {
		KfPageLayoutView: KfPageLayoutView,
		DisplayPayLinkModalView: DisplayPayLinkModalView



	}
});