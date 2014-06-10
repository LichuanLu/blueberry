define(['admin/fenzhen/fz_controller'], function(FzController) {
	// body...
	"use strict";
	return {
		API: {
			fenzhen: function() {

				return new FzController();
			}
		}
	}

});