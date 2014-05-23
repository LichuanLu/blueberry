define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
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
		},

		submitForm: function(e) {
			// body...
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