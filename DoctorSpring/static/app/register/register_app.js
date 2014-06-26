define(['register/patient/show_controller', 'register/doctor/show_controller'], function(PatientShowController, DoctorShowController) {
	// body...
	"use strict";
	return {
		API: {
			registerPatient: function() {

				return new PatientShowController();
			},
			registerDoctor: function() {
				return new DoctorShowController();
			}
		}
	}

});