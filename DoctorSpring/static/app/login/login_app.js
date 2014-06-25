define(['ladda-bootstrap','crypto-sha256'], function(ladda) {
	// body...
	"use strict";
	var loginAction = function(returnuri) {
		var $form = $('#loginForm');
		var $loginBtn = $form.find('.login-btn');
		$loginBtn.click(function(e) {
			e.preventDefault();
			// if ($('#register-form').valid()) {
			var l = ladda.create(document.querySelector('#submit'));

			var data = validate($form);
			if(returnuri){
				data+= "&returnuri="+returnuri;
			}
			console.dir(data);
			if (data) {
				var that = this;
				l.start();
				$.ajax({
					url: '/login.json',
					data: data,
					dataType: 'JSON',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
							this.onError(data);
						} else {
							// this.resetForm();
							console.log("msg:"+data.msg);
							this.reLocation(data.msg);
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});

						}
					},
					onError: function(res) {
						this.resetForm(true);
						//var error = jQuery.parseJSON(data);
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.msg,
								type: 'error',
								showCloseButton: true
							});
						}

					},
					complete: function(status,request) {

						l.stop();
					},
					resetForm: function(leaveInputData) {

					},
					reLocation: function(locationData) {

						if (locationData != null) {
							window.location.replace(locationData);
						} else {
							window.location.reload();
						}
					}
				});

			}
		});
	};
	var validate = function($from) {
		var data = $from.serialize();
		// var name = $('#inputUsername').val();
		// var data = "name="+name+"&password="+CryptoJS.SHA256($('#inputUserPassword').val());
		return data;
	};
	return {
		loginAction: loginAction
	}
});