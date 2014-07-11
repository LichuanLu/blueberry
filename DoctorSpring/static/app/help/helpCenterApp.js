(function() {
	"use strict";
	$(document).ready(function() {
		$('#helpcenter-tab a').click(function(e) {
			e.preventDefault();
			$(this).tab('show');
		});	
		$('#helpcenter-tab a').hover(function(e) {
			e.preventDefault();
			$(this).tab('show');
		});	
		$('#login-link').click(function(e) {
			e.preventDefault();
			window.location.replace('/loginPage');
		});	
	});


})();