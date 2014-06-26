(function() {
	"use strict";
	$(document).ready(function() {
		$('#help-tab a').click(function(e) {
			e.preventDefault();
			$(this).tab('show');
		});		
	});


})();