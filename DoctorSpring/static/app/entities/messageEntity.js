define(["backbone","marionette","config/base/constant","utils/reqcmd"],function (Backbone,Marionette,Constant,ReqCmd) {
	// body...
	"use strict";
	var MessageModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var MessageCollection = Backbone.Collection.extend({
		model:MessageModel,
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
		getMessageList: function (params) {
			if(!params){
				params = {};
			}
			var messageCollection = new MessageCollection();
			messageCollection.url = "/message/list";
			messageCollection.fetch({
				success:function () {
					// ReqCmd.reqres.request("localelistfetch:success");
					console.log("messageCollection fetch success");
				},
				data:params
			});

			return messageCollection
		}
	};
	
	return {
		API:API
	}

});
		