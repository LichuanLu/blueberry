//rewrite Marionette Application
require(['backbone','marionette','lodash'],function(Backbone,Marionette,lodash) {
	// body...
	"use strict";
	lodash.extend(Backbone.Marionette.Application.prototype,{
		navigate:function(route,options) {
			// body...
			options = typeof options !== 'undefined' ? options : {};
			Backbone.history.navigate(route, options);
		},
		getCurrentRoute:function() {
			// body...
			var frag = Backbone.history.fragment;
			if (lodash.isEmpty(frag)){
				return null;
			}
			else{
				return frag;
			} 
		},
		startHistory:function() {
			// body...
			if(Backbone.history){
				Backbone.history.start();
			}
		},
		register:function(instance,id) {
			// body...
			this.registry = typeof this.registry !== 'undefined' ? this.registry : {};
			this.registry[id] = instance;
		},
		unregister:function(instance,id) {
			// body...
			delete  this.registry[id];
		},
		resetRegistry:function() {
			// body...
			var oldCount = this.getRegistrySize();
			for (var controller in this.registry){
				controller.region.close()
			}
			var msg = "There were" +oldCount+ "controllers in the registry, there are now "+this.getRegistrySize();
			if (this.getRegistrySize() > 0){
			    console.warn(msg, this.egistry);
			}else{
				console.log(msg);
			}
		},
		getRegistrySize:function() {
			// body...
			lodash.size(this.registry);
		}


	});


});
