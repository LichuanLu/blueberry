define(["backbone","marionette","config/base/constant","utils/reqcmd"],function (Backbone,Marionette,Constant,ReqCmd) {
	// body...
	"use strict";
	var FavoriteModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var FavoriteCollection = Backbone.Collection.extend({
		model:FavoriteModel,
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
		getFavoriteList: function (params,userId) {
			if(!params){
				params = {};
			}
			var favoriteCollection = new FavoriteCollection();
			favoriteCollection.url = "/userFavorties/"+userId+"/list";
			favoriteCollection.fetch({
				success:function () {
					// ReqCmd.reqres.request("localelistfetch:success");
					console.log("favoriteCollection fetch success");
				},
				data:params
			});

			return favoriteCollection
		}
	};
	
	return {
		API:API
	}

});
		