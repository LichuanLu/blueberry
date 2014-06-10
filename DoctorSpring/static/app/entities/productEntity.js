define(["backbone","marionette","utils/reqcmd"],function (Backbone,Marionette,ReqCmd) {
	// body...
	"use strict";
	var ProductModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var ProductCollection = Backbone.Collection.extend({
		model:ProductModel,
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
		getActivedProducts: function (params) {
			if(!params){
				params = {};
			}
			var productListData = new ProductCollection();
			productListData.url = "/product/list?actived=true";
			productListData.fetch({
				success:function () {
					//ReqCmd.reqres.request("localelistfetch:success");
					console.log("fetch success");
				},
				data:params
			});

			return productListData
		},
		getRetiredProducts:function (params) {
			if(!params){
				params = {};
			}
			var productListData = new ProductCollection();
			productListData.url = "/product/list?actived=false";
			productListData.fetch({
				success:function () {
					//ReqCmd.reqres.request("localelistfetch:success");
					console.log("fetch success");
				},
				data:params
			});

			return productListData
		}

	};
	ReqCmd.reqres.setHandler("activedProduct:entities",function () {
		var temp = API.getActivedProducts();
		return temp
	});

	ReqCmd.reqres.setHandler("retiredProduct:entities",function () {
		var temp = API.getRetiredProducts();
		return temp
	});

});
		