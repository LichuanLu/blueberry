define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'jquery.uploader.main', 'entities/doctorEntity', 'dust', 'dustMarionette', "bootstrap", 'typeahead', 'flatui.checkbox', 'flatui.radio', 'jquery-ui', 'bootstrap.select', 'flat_ui_custom', 'dust_cus_helpers','config/validator/config'], function(ReqCmd, Lodash, Marionette, Templates, FileUploaderMain, DoctorEntity) {
	// body...
	"use strict";
	var ApplyDiagnosePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init ApplyDiagnosePageLayoutView");
			this.bindUIElements();
		},
		regions: {
			"recommandedDoctorRegion": "#recommandedDoctor"
		},
		el: "#applydignose-content",
		ui: {
			"formPanel": ".submit-patient-info-wrapper .panel",
			"submitBtns": ".btn-wrapper .submit-btn",
			"forms":".submit-patient-info-wrapper .panel form"

		},
		events: {
			'click @ui.submitBtns': "submitHandler"
		},
		attachEndHandler: function() {
			//init flatui
			$('.input-group').on('focus', '.form-control', function() {
				$(this).closest('.input-group, .form-group').addClass('focus');
			}).on('blur', '.form-control', function() {
				$(this).closest('.input-group, .form-group').removeClass('focus');
			});

			//init typehead
			if ($('#locationinput').length) {
				$('#locationinput').typeahead({
					name: 'cities',
					highlight: true,
					local: ["陕西 西安", "四川 成都"
					]
				});
			}

			if ($('#hospitalinput').length) {
				$('#hospitalinput').typeahead({
					name: 'hospitals',
					highlight: true,
					local: ["西安 西京医院", "四川 华西医科大学附属医院"]
				});
			}

			// jQuery UI Datepicker JS init
			var datepickerSelector = '#birthdateinput';
			$(datepickerSelector).datepicker({
				showOtherMonths: true,
				selectOtherMonths: true,
			}).prev('.btn').on('click', function(e) {
				e && e.preventDefault();
				$(datepickerSelector).focus();
			});
			$.extend($.datepicker, {
				_checkOffset: function(inst, offset, isFixed) {
					return offset
				}
			});

			// Now let's align datepicker with the prepend button
			$(datepickerSelector).datepicker('widget').css({
				'margin-left': -$(datepickerSelector).prev('.input-group-btn').find('.btn').outerWidth()
			});

			//init file uploader
			$('#dicomfileupload').fileupload({
				disableImageResize: false,
				maxFileSize: 2000000,
				// acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				maxNumberOfFiles: 1,

				// Uncomment the following to send cross-domain cookies:
				//xhrFields: {withCredentials: true},
				url: '/dicomfile/upload',
				uploadTemplateId: FileUploaderMain.uploadTemplateStr,
				downloadTemplateId: FileUploaderMain.downloadTemplateStr

			});
			$('#patient-medical-report-fileupload').fileupload({
				disableImageResize: false,
				maxFileSize: 2000000,
				// acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				maxNumberOfFiles: 1,

				// Uncomment the following to send cross-domain cookies:
				//xhrFields: {withCredentials: true},
				url: '/patientreport/upload',
				uploadTemplateId: FileUploaderMain.uploadTemplateStr,
				downloadTemplateId: FileUploaderMain.downloadTemplateStr

			});

			//init affix
			$('#affix-wrapper').affix({
				offset: {
					top: 60
				}
			});
			//init select
			$("select").selectpicker({
				style: 'btn-sm btn-primary'
			});

			//radio
			$(':radio').radio();

			$('.patient-radio-wrapper :radio').on('toggle', function() {
				var $this = $(this);
				var value = $this.val();
				if (value == 1) {
					$('#patient-already-exists').show();
					$('#new-patient-form').hide();

				} else if (value == 2) {
					$('#patient-already-exists').hide();
					$('#new-patient-form').show();
				}
			});

			//init form
			this.showForm(1);

			//modal show function
			// $('#select-doctor-modal').on('shown.bs.modal', function (e) {
			// 	console.log("modal shown");
			// });
			//init validator
			//console.log(this.ui.forms);
			$(this.ui.forms).each(function(index,element){
				$(element).validate({
					rules: {
						patientname: {
							required: true
						},
						patientsex: {
							required: true
						},
						birthdate:{
							required: true
						},
						phonenumber:{
							required: true,
							maxlength:11,
							minlength:11,
							number: true
						},
						location:{
							required:true
						},
						sectionId:{
							required:true
						},
						diagnoseHistory:{
							required:true
						},
						illnessHistory:{
							required:true
						}

					},
					ignore: [],
					highlight: function(element) {
						$(element).closest('.form-group').addClass('has-error');
					},
					unhighlight: function(element) {
						$(element).closest('.form-group').removeClass('has-error');
					},
					errorElement: 'span',
					errorClass: 'help-block',
					errorPlacement: function(error, element) {
						// if (element.is(":hidden")) {
						// 	element.next().parent().append(error);
						// } else if (element.parent('.input-group').length) {
						// 	error.insertAfter(element.parent());
						// } else {
						// 	error.insertAfter(element);
						// }
						error.appendTo($(element).closest('.form-group'));
					}
				});
			});




		},
		showForm: function(id) {

			//console.dir(this.ui.formPanel);

			var $form = this.ui.formPanel.filter(function() {
				//console.log($(this).data("form-id"));
				return $(this).data("form-id") == id
			});
			$form.addClass("visible");
		},
		submitHandler: function(e) {
			e.preventDefault();
			//console.log($(e.target).closest('.panel').data('form-id'));
			var $panel = $(e.target).closest('.panel');
			var $form = $panel.find('form:visible');
			var formId = $panel.data('form-id');
			var data = this.validate($form, formId);
			console.dir(data);
			if (data) {
				var that = this;
				$.ajax({
					url: '/save/diagnose/' + formId,
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.code != 0) {
							this.onError(data);

						} else {
							that.refreshForm(data);
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
						if (typeof res.message !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.message,
								type: 'error',
								showCloseButton: true
							});
						}

					},
					resetForm: function(leaveInputData) {

					}
				});

			}

		},
		validate: function($form, formId) {
			var data;
			console.log($form.valid());
			if(formId == 3){
				console.dir(this.ui.recommandedDoctor);
				data = "doctorId="+ $('#recommandedDoctor .doctor-preview').data('doctor-id');
			}else if(formId == 2){
				console.dir($('#dicomfileupload #downloadFile'));
				var fileurl = encodeURIComponent($("#downloadFile a:first").attr('href'));
				data = $form.serialize()+"&fileurl="+fileurl;

			}
			else{
				data = $form.serialize();
			}

			return data;
		},
		refreshForm: function(data) {
			if (typeof data.data.formId !== 'undefined') {
				if (data.data.formId == 3) {
					ReqCmd.reqres.request("ApplyDiagnosePageLayoutView:getRecommandedDoctor");
				}
				this.showForm(data.data.formId);
			}


		}



	});


	//modal select doctor
	var SelectDoctorModalView = Marionette.Layout.extend({
		initialize: function(options) {
			console.log("init SelectDoctorLayoutView");
			this.bindUIElements();
			this.controllerInstance = options.controllerInstance;
			// $('#select-doctor-modal .search-btn').click(function(e) {
			// 	e.preventDefault();
			// 	console.log(this.ui.selectDoctorForm.serialize());

			// });
		},
		regions: {
			"doctorListRegion": "#doctorListRegion"
		},
		el: "#select-doctor-modal",
		ui: {
			"selectDoctorForm": "form",
			"selectDoctorSearchBtn": ".search-btn"
		},
		events: {
			'click @ui.selectDoctorSearchBtn': "searchDoctorHandler"
		},
		//for search doctor modal
		searchDoctorHandler: function(e) {
			e.preventDefault();
			console.log(this.ui.selectDoctorForm.serialize());
			var data = this.ui.selectDoctorForm.serialize();
			if (data) {
				data += '&pageNumber=1&pageSize=6';

				ReqCmd.commands.execute("SelectDoctorModalView:searchDoctorHandler", data);
			}
		}
	});


	var SelectDoctorListView = Marionette.CompositeView.extend({
		initialize: function() {
			console.log("init SelectDoctorListView");
			// var doctor = this.model.get("doctor");
			// this.collection = new DoctorEntity.DoctorCollection(doctor);
			// this.listenTo(this.model, 'change', this.render, this);

		},
		onShow: function() {
			console.log("show SelectDoctorListView");

		},
		template: "selectDoctorList",
		itemViewContainer: ".row-fluid"
	});

	var SelectDoctorItemView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init SelectDoctorItemView");
			this.listenTo(this.model, 'change', this.render, this);


		},
		template: "selectDoctorItem",
		onRender: function() {
			console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			// this.$el = this.$el.children();
			// this.setElement(this.$el);
		},
		ui: {
			"chooseBtn": ".choose-btn"
		},
		events: {
			"click @ui.chooseBtn": "chooseDoctor"
		},

		onShow: function() {
			console.log("recommand");
			console.dir(this.model);
		},
		chooseDoctor: function(e) {
			e.preventDefault();
			ReqCmd.commands.execute("selectDoctorItemView:chooseDoctor",this.model);
			$("#select-doctor-modal").modal('hide');

		}
	});


	return {
		ApplyDiagnosePageLayoutView: ApplyDiagnosePageLayoutView,
		SelectDoctorModalView: SelectDoctorModalView,
		SelectDoctorListView: SelectDoctorListView,
		SelectDoctorItemView: SelectDoctorItemView
	}
});