define(["backbone", "marionette", "utils/reqcmd"], function(Backbone, Marionette, ReqCmd) {
	// body...
	"use strict";
	var TranslateStringModel = Backbone.Model.extend({
		//urlRoot: Constant+'/locale',
	});

	var TranslateStringCollection = Backbone.Collection.extend({
		model: TranslateStringModel,
		success: function(data, textStatus, jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function(data) {
			// body...
			console.dir(data);
		},
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data;
		}
	});
	var SuggestionModel = Backbone.Model.extend({

	});

	var SuggestionCollection = Backbone.Collection.extend({
		model: SuggestionModel,
		success: function(data, textStatus, jqXHR) {
			// body...
			console.dir(data);
		},
		onError: function(data) {
			// body...
			console.dir(data);
		},
		parse: function(resp) {
			// body...
			console.dir(resp.data);
			return resp.data;
		},
		replace: function(model) {

			var duplicates = this.filter(function(_model) {

				return _model.get('suggestionId') === model.get('suggestionId');

			});

			if (!_.isEmpty(duplicates)) {

				this.remove(duplicates);

			}

			Backbone.Collection.prototype.add.call(this, model);

		}


	});

	var API = {
		getTranslateStrings: function(params, collection) {
			if (!params) {
				params = {};
			}
			var translateStringCollection = collection !== '' ? collection : new TranslateStringCollection();
			translateStringCollection.url = "/localizableEntity/stringList.json";
			translateStringCollection.fetch({
				add: true,
				update: true,
				remove: false,
				success: function() {
					ReqCmd.reqres.request("getTranslateStrings:success");
					console.log("fetch success");

				},
				data: $.param(params)
			});

			return translateStringCollection;
		},

		//
		getSuggestions: function(params, view_instance) {
			if (!params) {
				params = {};
			}
			//for testing , should delete after intergration
			// if(typeof params.productId === 'undefined'){
			// 	params.productId = 4;
			// }
			// if(typeof params.localeId === 'undefined'){
			// 	params.localeId = 6;
			// }

			var suggestionCollection = new SuggestionCollection();
			//for testing , should update after intergration
			suggestionCollection.url = "/locales/6/products/4/translate";

			suggestionCollection.fetch({
				success: function() {
					console.log("fetch success");
					console.log(view_instance);
					view_instance.model.set({
						suggestionListDataFetched: true
					});
					var hasSuggestion = true;
					if(suggestionCollection.length === 0){
						hasSuggestion = false;
					}
					ReqCmd.commands.execute("getSuggestions:success:entities", view_instance,hasSuggestion);
				},
				data: $.param(params)
			});


			return suggestionCollection;
		}
	};
	ReqCmd.commands.setHandler("stringList:entities", function(instance) {
		instance.stringListData = API.getTranslateStrings(instance.stringListParams, '');
	});
	ReqCmd.commands.setHandler("suggestionList:entities", function(instance, params) {
		instance.suggestionListData = API.getSuggestions(params, instance);
	});
	// ReqCmd.commands.setHandler("loadStrings:translateView", function(currentpage) {
	// 	console.log(currentpage);

	// });
	return {
		API: API,
		SuggestionModel: SuggestionModel
	};

});