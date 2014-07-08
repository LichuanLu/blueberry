(function() {
	"use strict";
	$(document).ready(function() {
		$('#about-tab a').click(function(e) {
			e.preventDefault();
			$(this).tab('show');
		});		
	});


})();