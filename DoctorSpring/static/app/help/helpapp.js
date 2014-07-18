(function() {
	"use strict";
	$(document).ready(function() {
		$('#help-tab a').click(function(e) {
			e.preventDefault();
			$(this).tab('show');
		});
		$('#login-link').click(function(e) {
			e.preventDefault();
			window.location.replace('/loginPage');
		});
	});


})();