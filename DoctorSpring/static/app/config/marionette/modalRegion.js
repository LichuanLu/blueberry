define(['utils/reqcmd', 'lodash', 'marionette','backbone',"bootstrap"], function(ReqCmd, Lodash, Marionette,Backbone) {
	"use strict";
	var ModalRegion = Marionette.Region.extend({
		 constructor: function(){
	      Lodash.bindAll(this);
	      Marionette.Region.prototype.constructor.apply(this, arguments);
	      this.on("show", this.showModal, this);
	    },
	    getEl: function(selector){
	      var $el = $(selector);
	      $el.on("hidden", this.close);
	      return $el;
	    },
	 
	    showModal: function(view){
	      view.on("close", this.hideModal, this);
	      this.$el.modal('show');
	    },
	    hideModal: function(){
	      this.$el.modal('hide');
	    },
	    el:"#modalRegion"
	    
	});
	return {
		ModalRegion:ModalRegion
	}

});