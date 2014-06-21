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
		diagnoseItem:require('patienthome/templates/diagnoseItem'),
		diagnoseLayout:require('patienthome/templates/diagnoseLayout'),
		patientAccountManageLayout:require('patienthome/templates/patientAccountManageLayout'),
		patientMessageLayout:require('patienthome/templates/patientMessageLayout'),
		sharingModal:require('patienthome/templates/sharingModal'),
		favoriteLayout:require('patienthome/templates/favoriteLayout'),
		favoriteItem:require('patienthome/templates/favoriteItem'),
		cancelFavoriteModalView:require('patienthome/templates/cancelFavoriteModalView'),
		detailTrackLayout:require('patienthome/templates/detailTrackLayout'),




		selectDoctorItem:require('diagnose/templates/selectDoctorItem'),
		selectDoctorList:require('diagnose/templates/selectDoctorList'),
		patientProfile:require('diagnose/templates/patientProfile'),
		dicomInfo:require('diagnose/templates/dicomInfo'),
		pathologyItem:require('diagnose/templates/pathologyItem'),

		//template for fenzhen
		allDiagnoseItem:require('admin/fenzhen/templates/allDiagnoseItem'),
		myDiagnoseItem:require('admin/fenzhen/templates/myDiagnoseItem'),
		rollbackDiagnoseModal:require('admin/fenzhen/templates/rollbackDiagnoseModal'),


		doctorAccountManageLayout:require('doctorhome/templates/doctorAccountManageLayout'),
		doctorDiagnoseItem:require('doctorhome/templates/doctorDiagnoseItem'),
		doctorDiagnoseLayout:require('doctorhome/templates/doctorDiagnoseLayout'),
		newDiagnoseLayout:require('doctorhome/templates/newDiagnoseLayout'),
		newAuditLayout:require('doctorhome/templates/newAuditLayout'),
		doctorMessageLayout:require('doctorhome/templates/doctorMessageLayout'),
		doctorConsultLayout:require('doctorhome/templates/doctorConsultLayout'),

		doctorDetailItem:require('doctorList/templates/doctorDetailItem'),
		doctorDetailList:require('doctorList/templates/doctorDetailList'),


		hospitalUserDignoseItem:require('hospitalUserPage/templates/hospitalUserDiagnoseItem'),
		hospitalUserSubmittedDignoseItem:require('hospitalUserPage/templates/hospitalUserSubmittedDiagnoseItem'),


		messageItem:require('message/templates/messageItem')


		

		




	};
});
