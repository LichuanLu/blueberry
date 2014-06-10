define(function(require) {
	"use strict";
	return {
		// _localeView: require('project_setup/templates/localeItem'),
		// localesView: require('project_setup/templates/locales'),
		// productItem: require('project_manage/templates/productItem'),
		// activedProducts: require('project_manage/templates/activedProducts'),
		// retiredProducts: require('project_manage/templates/retiredProducts'),
		// manageProductDetail: require('project_manage/templates/manageProductDetail'),
		// manageProductMain: require('project_manage/templates/manageProductMain'),
		// stringlistItem: require('translate/templates/stringListItem'),
		// stringDetail: require('translate/templates/stringDetail'),
		// suggestionList:require('translate/templates/suggestionList'),
		// suggestionListItem:require('translate/templates/suggestionListItem'),
		// userActivityItem:require('userhome/templates/userActivityItem')
		diagnoseItem:require('patientHome/templates/diagnoseItem'),
		diagnoseLayout:require('patientHome/templates/diagnoseLayout'),
		patientAccountManageLayout:require('patientHome/templates/patientAccountManageLayout'),
		patientMessageLayout:require('patientHome/templates/patientMessageLayout'),
		sharingModal:require('patientHome/templates/sharingModal'),
		favoriteLayout:require('patientHome/templates/favoriteLayout'),
		favoriteItem:require('patientHome/templates/favoriteItem'),
		cancelFavoriteModalView:require('patientHome/templates/cancelFavoriteModalView'),




		selectDoctorItem:require('diagnose/templates/selectDoctorItem'),
		selectDoctorList:require('diagnose/templates/selectDoctorList'),
		patientProfile:require('diagnose/templates/patientProfile'),
		dicomInfo:require('diagnose/templates/dicomInfo'),
		pathologyItem:require('diagnose/templates/pathologyItem'),

		//template for fenzhen
		allDiagnoseItem:require('admin/fenzhen/templates/allDiagnoseItem'),
		myDiagnoseItem:require('admin/fenzhen/templates/myDiagnoseItem'),


		doctorAccountManageLayout:require('doctorHome/templates/doctorAccountManageLayout'),
		doctorDiagnoseItem:require('doctorHome/templates/doctorDiagnoseItem'),
		doctorDiagnoseLayout:require('doctorHome/templates/doctorDiagnoseLayout'),
		newDiagnoseLayout:require('doctorHome/templates/newDiagnoseLayout'),
		newAuditLayout:require('doctorHome/templates/newAuditLayout'),
		doctorMessageLayout:require('doctorHome/templates/doctorMessageLayout'),
		doctorConsultLayout:require('doctorHome/templates/doctorConsultLayout'),

		doctorDetailItem:require('doctorList/templates/doctorDetailItem'),
		doctorDetailList:require('doctorList/templates/doctorDetailList'),




		messageItem:require('message/templates/messageItem')


		

		




	};
});
