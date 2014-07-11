define(['utils/reqcmd', 'lodash', 'marionette', 'templates','login/login_app','dust', 'dustMarionette', "bootstrap", 'utils/followbtn'], function(ReqCmd, Lodash, Marionette, Templates,LoginApp) {
	// body...
	"use strict";
	var DoctorSiteLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorSiteLayoutView");
			this.bindUIElements();
		},
		regions: {},
		el: "#doctorsite-content",
		ui: {
			"addThanksBtn": "#add-thanks-btn"
		},
		events: {
			"click @ui.addThanksBtn": "addThanksHandler"
		},
		addThanksHandler: function(e) {
			var doctorUserId = $('.avatar-wrapper .follow-link').data('uid');
			console.log(doctorUserId);
			var $thanksContent = $('#thanks-content');
			var content = $thanksContent.val();
			if (doctorUserId) {
				var params = {
					receiver:doctorUserId,
					title:"",
					content:content
				}
				$.ajax({
					url: '/gratitude/create',
					data: $.param(params),
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);

						} else {
							this.resetForm();
							Messenger().post({
								message: '成功发送感谢信，需要管理员审核后可见。',
								type: 'success',
								showCloseButton: true
							});

						}
					},
					onError: function(res) {
						//var error = jQuery.parseJSON(data);
						if (res.status == 2) {
							window.location.replace('/loginPage')

						} else if (res.status == 4) {
							window.location.replace('/error')

						}
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "错误信息:" + res.msg,
								type: 'error',
								showCloseButton: true
							});
						}

					},
					resetForm: function() {
						$thanksContent.val("");
					}
				});
			}
			
		},
		attachEndHandler: function() {
			$('.follow-link').followaction();

			$('#doctor-site-tab a').click(function(e) {
				e.preventDefault();
				$(this).addClass('active');
				$(this).siblings().removeClass('active');
				$(this).tab('show');
			});
			//init login modal
			LoginApp.loginAction();
		}

	});


	return {
		DoctorSiteLayoutView: DoctorSiteLayoutView
	}
});