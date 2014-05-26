define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var DoctorRegisterPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorRegisterPageLayoutView");
			this.bindUIElements();
		},
		regions: {},
		el: "#register-doctor-content",
		ui: {
			"registerDoctorForm": "#register-form",
			"submitBtn": ".submit-button"
		},
		events: {
			'click @ui.submitBtn': "submitForm"
		},
		attachEndHandler: function() {
		},
		submitForm: function(e) {
			e.preventDefault();
			// if ($('#register-form').valid()) {
			var data = this.validate();
			console.dir(data);

			if (data) {
				var that = this;
				$.ajax({
					url: '/register/doctor.json',
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.code != 0) {
							this.onError(data);

						} else {
							// this.resetForm();
							Messenger().post({
								message: 'SUCCESS. Product import started. Check back periodically.',
								type: 'success',
								showCloseButton: true
							});
							//alert('SUCCESS. Product import started. Check back periodically.');

						}
						//allowSubmit = true;
					},
					onError: function(res) {
						this.resetForm(true);
						//var error = jQuery.parseJSON(data);
						if (typeof res.message !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.message,
								type: 'error',
								showCloseButton: true
							});
						}
						//alert("%ERROR_CODE_" + data.code + ",%ERROR_MESSAGE_" + data.message);

						//allowSubmit = true;
					},
					resetForm: function(leaveInputData) {}
				});

			}
		},
		validate: function() {
			var data = this.ui.registerDoctorForm.serialize();
			return data;
		}

	});

	return {
		DoctorRegisterPageLayoutView: DoctorRegisterPageLayoutView
	}
});