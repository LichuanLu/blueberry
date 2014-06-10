define(['doctorList/show/show_controller'], function(ShowController) {
	// body...
	"use strict";
	return {
		API: {
			show: function() {

				return new ShowController();
			}
		}
	}

});