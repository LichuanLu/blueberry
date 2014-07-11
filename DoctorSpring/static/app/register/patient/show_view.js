define(['utils/reqcmd', 'lodash', 'marionette', 'templates','login/login_app','dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates,LoginApp) {
	// body...
	"use strict";
	var PatientRegisterPageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init PatientRegisterPageLayoutView");
			this.bindUIElements();
		},
		regions: {},
		el: "#register-patient-content",
		ui: {
			"registerPatientForm": "#register-form",
			"registerPatientSubmit": "#register-form .submit-button"
		},
		events: {
			"click @ui.registerPatientSubmit": "submitForm"
		},
		attachEndHandler: function() {
			console.log("PatientRegisterPageLayoutView attach end ");
			LoginApp.loginAction();

		},

		submitForm: function(e) {
			e.preventDefault();
			// if ($('#register-form').valid()) {
			var data = this.validate();
			console.dir(data);

			if (data) {
				var that = this;
				$.ajax({
					url: '/register/patient.json',
					data: data,
					dataType: 'json',
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
							//alert('SUCCESS. Product import started. Check back periodically.');

						}
						//allowSubmit = true;
					},
					onError: function(res) {
						this.resetForm(true);
						//var error = jQuery.parseJSON(data);
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "错误信息:" + res.msg,
								type: 'error',
								showCloseButton: true
							});
						}
						//alert("%ERROR_CODE_" + data.status + ",错误信息_" + data.message);

						//allowSubmit = true;
					},
					resetForm: function(leaveInputData) {
						// if (leaveInputData !== true) {
						// 	leaveInputData = false;
						// }

						// if (!leaveInputData) {
						// 	// $inProduct.val(0);
						// 	$('#inProductName').val('');
						// 	$('#inCodeName').val('');
						// 	$('#inProductVersion').val('');
						// 	$('#inDisName').val('');
						// 	$('#inOwer').val('');
						// 	$('#inRestrict').attr('checked', true);
						// 	$('#fileupload').find(".files").empty();
						// 	var $localelist = $('#localeList');
						// 	$('#localeList option').each(function() {
						// 		$localelist.multiselect('deselect', $(this).val());
						// 	});
						// 	$('#toggleBtn').text("Select All");
						// 	//$("#inRestrict")

						// }
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

		},

		validate: function() {
			var data = this.ui.registerPatientForm.serialize();
			return data;


		}

	});

	return {
		PatientRegisterPageLayoutView: PatientRegisterPageLayoutView
	}
});