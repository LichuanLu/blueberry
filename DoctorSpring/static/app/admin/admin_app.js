define(['admin/fenzhen/fz_controller','admin/kefu/kf_controller'], function(FzController,KfController) {
	// body...
	"use strict";
	return {
		API: {
			fenzhen: function() {

				return new FzController();
			},
			kefu: function() {

				return new KfController();
			}
		}
	}

});