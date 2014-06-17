define(["backbone","marionette","config/base/constant","utils/reqcmd"],function (Backbone,Marionette,Constant,ReqCmd) {
	// body...
	"use strict";
	var LocaleModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var LocaleCollection = Backbone.Collection.extend({
		model:LocaleModel,
		success: function (data,textStatus,jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function (data) {
			// body...
			console.dir(data);
		},
		parse: function (resp) {
			// body...
			console.dir(resp.data);
			return resp.data
		}
	});
	
	var API = {
		getLocales: function (params) {
			if(!params){
				params = {};
			}
			var localesListData = new LocaleCollection();
			localesListData.url = "/locale/list";
			localesListData.fetch({
				success:function () {
					ReqCmd.reqres.request("localelistfetch:success");
					console.log("fetch success");
				},
				data:params
			});

			return localesListData
		}
	};
	ReqCmd.reqres.setHandler("locale:entities",function () {
		var temp = API.getLocales();
		return temp

	});

});
		