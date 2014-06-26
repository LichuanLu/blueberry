define(['backbone.wreqr'], function( Wreqr ){
	"use strict";
	var req = new Wreqr.RequestResponse();
	var comd = new Wreqr.Commands();
    return {
		reqres: req,
		commands: comd

    }
});
