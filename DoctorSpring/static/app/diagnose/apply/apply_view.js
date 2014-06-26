define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'jquery.uploader.main', 'entities/doctorEntity', 'dust', 'dustMarionette', "bootstrap", 'typeahead', 'flatui.checkbox', 'flatui.radio', 'jquery-ui', 'bootstrap.select', 'flat_ui_custom', 'dust_cus_helpers', 'config/validator/config', 'bootstrap.multiselect'], function(ReqCmd, Lodash, Marionette, Templates, FileUploaderMain, DoctorEntity) {
	// body...
	"use strict";
	//var $;
	var ApplyDiagnosePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init ApplyDiagnosePageLayoutView");
			this.isEdit = $.getUrlVar('edit');
			this.diagnoseId = $.getUrlVar('diagnoseid');
			this.isHospitalUser = $.getUrlVar('type');
			this.appInstance = require('app');
			if (this.diagnoseId) {
				$('#diagnose-id-input').val(this.diagnoseId);
			}
			this.bindUIElements();
		},
		regions: {
			"recommandedDoctorRegion": "#recommandedDoctor",
			"patientProfileRegion": "#patient-already-profile-region",
			"dicomInfoRegion": "#dicom-already-info-region",
			"historyAlreadyExistsSelect": "#history-already-exists-select",
			"dicomAlreadyExistsSelect": "#dicom-already-exists-select"

		},
		el: "#applydignose-content",
		ui: {
			"formPanel": ".submit-patient-info-wrapper .panel",
			"submitBtns": ".btn-wrapper .submit-btn",
			"forms": ".submit-patient-info-wrapper .panel form",
			"patientAlreadyExistsSelect": "#patient-already-exists select",
			"dicomAlreadyExistsSelect": "#dicom-already-exists select",
			"reuploadBtn": '.edit-file-wrapper .btn'
		},
		events: {
			'click @ui.submitBtns': "submitHandler",
			'change @ui.patientAlreadyExistsSelect': "changePatientAlreadyExists",
			'change @ui.dicomAlreadyExistsSelect': "changeDicomAlreadyExists",
			'click @ui.reuploadBtn': "reuploadFile"
		},
		attachEndHandler: function() {
			//init flatui
			$('.input-group').on('focus', '.form-control', function() {
				$(this).closest('.input-group, .form-group').addClass('focus');
			}).on('blur', '.form-control', function() {
				$(this).closest('.input-group, .form-group').removeClass('focus');
			});

			//init typehead
			// if ($('#locationinput').length) {
			// 	$('#locationinput').typeahead({
			// 		name: 'cities',
			// 		highlight: true,
			// 		local: ["陕西 西安", "四川 成都"]
			// 	});
			// }

			// if ($('#hospitalinput').length) {
			// 	$('#hospitalinput').typeahead({
			// 		name: 'hospitals',
			// 		highlight: true,
			// 		local: ["西安 西京医院", "四川 华西医科大学附属医院"]
			// 	});
			// }


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
			var temp = $('#dicomfileupload').fileupload({
				disableImageResize: false,
				maxFileSize: 2000000,
				// acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				maxNumberOfFiles: 1,

				// Uncomment the following to send cross-domain cookies:
				//xhrFields: {withCredentials: true},
				url: '/dicomfile/upload',
				uploadTemplateId: FileUploaderMain.uploadTemplateStr,
				downloadTemplateId: FileUploaderMain.downloadTemplateStr

			}).bind('fileuploadsubmit', function(e, data) {
				// The example input, doesn't have to be part of the upload form:
				var input = $('#diagnose-id-input');
				data.formData = {
					diagnoseId: input.val()
				};
				// if (!data.formData.diagnoseId) {
				//   data.context.find('button').prop('disabled', false);
				//   input.focus();
				//   return false;
				// }
			});
			$('#patient-medical-report-fileupload').fileupload({
				disableImageResize: false,
				maxFileSize: 2000000,
				// acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				maxNumberOfFiles: 5,

				// Uncomment the following to send cross-domain cookies:
				//xhrFields: {withCredentials: true},
				url: '/patientreport/upload',
				uploadTemplateId: FileUploaderMain.uploadTemplateStr,
				downloadTemplateId: FileUploaderMain.downloadTemplateStr

			}).bind('fileuploadsubmit', function(e, data) {
				// The example input, doesn't have to be part of the upload form:
				var input = $('#diagnose-id-input');
				data.formData = {
					diagnoseId: input.val()
				};
				// if (!data.formData.diagnoseId) {
				//   data.context.find('button').prop('disabled', false);
				//   input.focus();
				//   return false;
				// }
			});

			//init affix
			$('#affix-wrapper').affix({
				offset: {
					top: 60
				}
			});
			//init select
			$("select").not('.multiselect').selectpicker({
				style: 'btn-sm btn-primary',
				title: "没有纪录"
			});

			//radio
			$(':radio').radio();

			//multi select

			$("#patientLocationSelect").multiselect({
				numberDisplayed: 2,
				enableFiltering: true,
				filterPlaceholder: "搜索",
				nonSelectedText: "没有选中"
				// buttonWidth: '300px'
			});

			$("#hospitalinput").multiselect({
				enableFiltering: true,
				filterPlaceholder: "搜索",
				nonSelectedText: "没有选中"
				// buttonWidth: '300px'
			});

			$("#locationinput").multiselect({
				enableFiltering: true,
				filterPlaceholder: "搜索",
				nonSelectedText: "没有选中"
				// buttonWidth: '300px'
			});


			$('#patient-profile-radio :radio').on('toggle', function() {
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
			$('#patient-dicom-radio :radio').on('toggle', function() {
				var $this = $(this);
				var value = $this.val();
				if (value == 1) {
					$('#dicom-already-exists').show();
					$('#new-dicom-form').hide();

				} else if (value == 2) {
					$('#dicom-already-exists').hide();
					$('#new-dicom-form').show();
				}
			});
			$('#patient-history-radio :radio').on('toggle', function() {
				var $this = $(this);
				var value = $this.val();
				if (value == 1) {
					$('#history-already-exists').show();
					$('#new-history-form').hide();

				} else if (value == 2) {
					$('#history-already-exists').hide();
					$('#new-history-form').show();
				}
			});

			//init form
			this.showForm(1);
			if (this.isEdit === 'true') {
				this.showForm(2);
				this.showForm(3);
				this.showForm(4);
			}

			//modal show function
			// $('#select-doctor-modal').on('shown.bs.modal', function (e) {
			// 	console.log("modal shown");
			// });
			//init validator
			//console.log(this.ui.forms);
			$(this.ui.forms).each(function(index, element) {
				$(element).validate({
					rules: {
						patientname: {
							required: true
						},
						patientsex: {
							required: true
						},
						birthdate: {
							required: true
						},
						phonenumber: {
							required: true,
							maxlength: 11,
							minlength: 11,
							number: true
						},
						identitynumber: {
							required: true
						},
						location: {
							required: true
						},
						skillId: {
							required: true
						},
						diagnoseHistory: {
							required: true
						},
						illnessHistory: {
							required: true
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


			this.initDiagnoseForms();

		},
		// we need this to do init work for forms
		initDiagnoseForms: function() {
			ReqCmd.reqres.request("ApplyDiagnosePageLayoutView:getRecommandedDoctor");
			this.initPatientProfile();
			this.initDicomInfo();

		},
		//in form3 , change exist dicom from select
		changeDicomAlreadyExists: function() {
			this.initDicomInfo();
		},
		initDicomInfo: function() {
			var params = $('#dicom-already-exists').serialize();
			console.log('initDicomInfo params:' + params);
			ReqCmd.commands.execute('initDicomInfo:ApplyDiagnosePageLayoutView', params);

		},

		//in form2 , change exist patient from select
		changePatientAlreadyExists: function() {
			this.initPatientProfile();
		},

		initPatientProfile: function() {
			var params = $('#patient-already-exists').serialize();
			console.log('initPatientProfile params:' + params);
			ReqCmd.commands.execute('initPatientProfile:ApplyDiagnosePageLayoutView', params);
			this.initPathologySelect(params);


		},
		//after select user ,get Pathology Select data
		//params contains patientId
		initPathologySelect: function(params) {
			ReqCmd.commands.execute('initPathologySelect:ApplyDiagnosePageLayoutView', params);
		},
		showForm: function(id) {

			//console.dir(this.ui.formPanel);
			var $form = this.ui.formPanel.filter(function() {
				//console.log($(this).data("form-id"));
				return $(this).data("form-id") == id
			});
			$form.addClass("visible");
			if (id == 1) {
				$('.first-nav').show();

			} else if (id == 2) {
				$('.second-nav').show();


			} else if (id == 3) {
				$('.third-nav').show();


			} else if (id == 4) {
				$('.fourth-nav').show();


			}
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
				//when edit , add diagnose id for the request
				if (this.isEdit === 'true' && this.diagnoseId) {
					data += "&diagnoseId=" + this.diagnoseId;
				}
				var that = this;
				$.ajax({
					url: '/save/diagnose/' + formId,
					data: data,
					dataType: 'json',
					type: 'POST',
					success: function(data) {
						if (data.status != 0) {
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
						if (typeof res.msg !== 'undefined') {
							Messenger().post({
								message: "%ERROR_MESSAGE:" + res.msg,
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
			if (formId == 1) {
				console.dir(this.ui.recommandedDoctor);
				data = "doctorId=" + $('#recommandedDoctor .doctor-preview').data('doctor-id');
			} else if (formId == 3) {
				console.dir($('#dicomfileupload #downloadFile'));
				var fileurl = "";
				var tempstr = $("#new-dicom-form .downloadFileLink").attr('href');
				if (typeof tempstr !== 'undefined' && tempstr != 'undefined') {
					fileurl = "&fileurl=" + encodeURIComponent(tempstr);
				}
				if (typeof fileurl !== 'undefined') {
					data = $form.serialize() + fileurl;
				} else {
					data = $form.serialize()
				}

			} else {
				var filelinks = $("#new-history-form").find('.downloadFileLink');
				var fileurl = "";
				filelinks.each(function(index, element) {
					var tempstr = $(element).attr('href');
					if (typeof tempstr !== 'undefined' && tempstr != 'undefined') {
						fileurl += "&fileurl=" + encodeURIComponent(tempstr);
					}
				})
				if (typeof fileurl !== 'undefined') {
					data = $form.serialize() + fileurl;
				} else {
					data = $form.serialize();
				}
			}

			return data;
		},
		refreshForm: function(data) {
			if (typeof data.data.formId !== 'undefined') {
				if (data.data.formId == 1) {
					if (this.isEdit !== 'true') {
						ReqCmd.reqres.request("ApplyDiagnosePageLayoutView:getRecommandedDoctor");
					}
				} else if (data.data.formId == 2) {
					if (this.isEdit !== 'true') {
						this.initPatientProfile();
					}
				} else if (data.data.formId == 3) {
					if (this.isEdit !== 'true') {
						this.initDicomInfo();
					}
					if (data.data.diagnoseId) {
						$('#diagnose-id-input').val(data.data.diagnoseId);
					}
				}
				this.showForm(data.data.formId);
			}
			if (data.data.isFinal) {

				var ModalModel = Backbone.Model.extend({

				});
				var model = new ModalModel();
				model.set('isHospitalUser', this.isHospitalUser);
				var successSubmitDiagnoseModalView = new SuccessSubmitDiagnoseModalView({
					model: model
				});
				this.appInstance.modalRegion.show(successSubmitDiagnoseModalView);

			}


		},
		reuploadFile: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var $editWrapper = $target.closest('.edit-file-wrapper');
			var $newWrapper = $editWrapper.siblings('.new-file-wrapper');
			$editWrapper.hide();
			$newWrapper.show();
			console.log("reupload file");
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
			this.currentPage = 1;

		},
		onShow: function() {
			console.log("show SelectDoctorListView");

		},
		ui: {
			"pageLinks": ".pagination-plain a"
			// "currentLi":"li.active"
		},
		events: {
			"click @ui.pageLinks": "changePage"
		},
		template: "selectDoctorList",
		itemViewContainer: ".row-fluid",
		changePage: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var $li = $target.closest('li');
			var $currentLi = $('.pagination-plain li.active');
			if ($li.is('.previous')) {
				if (this.currentPage > 1) {
					$currentLi.prev().addClass('active');
					$currentLi.removeClass('active');
					this.currentPage--;
				}

			} else if ($li.is('.next')) {
				if (this.currentPage < this.model.get('pageNumber')) {
					$currentLi.next().addClass('active');
					$currentLi.removeClass('active');
					this.currentPage++;
				}
			} else {
				$li.addClass('active');
				$currentLi.removeClass('active');
				this.currentPage = $li.find('a').text();

			}
			this.fetchNewPage();

		},
		fetchNewPage: function() {
			console.log($('#select-doctor-modal form').serialize());
			var data = $('#select-doctor-modal form').serialize();
			if (data) {
				data += '&pageNumber=' + this.currentPage + '&pageSize=6';
				ReqCmd.commands.execute("SelectDoctorModalView:searchDoctorHandler", data);
			}
		}

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
			ReqCmd.commands.execute("selectDoctorItemView:chooseDoctor", this.model);
			$("#select-doctor-modal").modal('hide');

		}
	});

	var PatientProfileView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init PatientProfileView");
			this.listenTo(this.model, 'change', this.render, this);
		},
		template: "patientProfile",
		onRender: function() {
			console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			// this.$el = this.$el.children();
			// this.setElement(this.$el);
		},
		ui: {},
		events: {},

		onShow: function() {
			console.log("PatientProfileView onShow");
		}
	});

	var DicomInfoView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init DicomInfoView");
			this.listenTo(this.model, 'change', this.render, this);
		},
		template: "dicomInfo",
		onRender: function() {
			console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			// this.$el = this.$el.children();
			// this.setElement(this.$el);
		},
		ui: {},
		events: {},

		onShow: function() {
			console.log("DicomInfoView onShow");
		}
	});


	var PathologyCollectionView = Marionette.CollectionView.extend({
		initialize: function() {

		},
		onRender: function() {
			console.log("PathologyCollectionView render");


		},
		onAfterItemAdded: function(itemView) {

		},
		onShow: function() {
			console.log("PathologyCollectionView onShow");
			//init the modal onshow
		},
		itemViewOptions: function() {}
	});

	var PathologyItemView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init PathologyItemView");
			this.listenTo(this.model, 'change', this.render, this);
		},
		template: "pathologyItem",
		onRender: function() {
			console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);
		},
		ui: {},
		events: {},
		onShow: function() {
			console.log("PathologyItemView onShow");
		}
	});


	var SuccessSubmitDiagnoseModalView = Marionette.ItemView.extend({
		template: "successSubmitDiagnoseModal",
		initialize: function() {
			console.log("SuccessSubmitDiagnoseModalView init");

		},
		onRender: function() {
			console.log("SuccessSubmitDiagnoseModalView render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);

		},
		onShow: function() {

		},
		ui: {},
		events: {}

	});


	return {
		ApplyDiagnosePageLayoutView: ApplyDiagnosePageLayoutView,
		SelectDoctorModalView: SelectDoctorModalView,
		SelectDoctorListView: SelectDoctorListView,
		SelectDoctorItemView: SelectDoctorItemView,
		PatientProfileView: PatientProfileView,
		DicomInfoView: DicomInfoView,
		PathologyCollectionView: PathologyCollectionView,
		PathologyItemView: PathologyItemView

	}
});