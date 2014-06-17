define([], function() {
	// body...
	"use strict";
	var loginAction = function() {
		var $form = $('#loginForm');
		var $loginBtn = $form.find('.login-btn');
		$loginBtn.click(function(e) {
			e.preventDefault();
			// if ($('#register-form').valid()) {
			var data = validate($form);
			console.dir(data);
			if (data) {
				var that = this;
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
		return data;
	};
	return {
		loginAction: loginAction
	}
});