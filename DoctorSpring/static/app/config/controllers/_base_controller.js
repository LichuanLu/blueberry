//Base controller , inherit from Marionette Controller 
define(['backbone','marionette','lodash','utils/reqcmd'],function(Backbone,Marionette,lodash,ReqCmd) {
	// body...
	//add require as circulation calling app
	"use strict";
	var BaseController = Marionette.Controller.extend(
		{
			constructor:function(options) {
				// body...
				options = typeof options !== 'undefined' ? options : {} ;
				this.region = options.region || ReqCmd.reqres.request("default:region");
				this.instance_id = lodash.uniqueId("controller");
				ReqCmd.commands.execute("register:instance",this,this.instance_id);
				BaseController.__super__.constructor.apply(this,arguments);


			},
			close:function() {
				// body...
				ReqCmd.commands.execute("unregister:instance",this,this.instance_id);
				BaseController.__super__.close.apply(this,arguments);

			},
			show:function(view, options) {
				// body...
				options = typeof options !== 'undefined' ? options : {} ;
				lodash.defaults(options,{loading:false,region:this.region,client:false});
				this.setMainView(view);
				this.manageView(view,options);

			},
			setMainView:function(view) {
				// body...
				if(this.mainView){
					
					return;
				
				}
				this.mainView = view;
				this.listenTo(view,"close",this.close());
			},
			manageView:function(view, options) {
				// body...
				if(options.loading){
					ReqCmd.commands.execute("show:loading", view, options);
				}
				else if(options.client){
					options.region.show(view);
				}
				else{
					options.region.attachView(view);
					if(options.name !== null && options.instance !== null){
					   var req = options.name+":attached";
					   ReqCmd.commands.execute(req,options.instance);
					}
				}
			}

		

		}
		// another way to call father constructor if don't have __super__
		// ,
		// {
		// 	parent_klass:Marionette.Controller.prototype

		// }
	);
	return BaseController
	
});



