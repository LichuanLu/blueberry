//require js root
require.config({
  paths : {
    underscore : 'lib/underscore/underscore-min',
    backbone   : 'lib/backbone/backbone',
    marionette : 'lib/backbone.marionette/lib/core/amd/backbone.marionette',
    jquery     : 'lib/jquery/jquery.min',
    dust       : 'lib/dust-full-linkedin.min',
    dustMarionette : 'lib/backbone.marionette.dust',
    dustHelper : 'lib/dust-helpers',
    'backbone.wreqr' : 'lib/backbone.wreqr/lib/amd/backbone.wreqr.min',
    'backbone.eventbinder' : 'lib/backbone.eventBinder/lib/amd/backbone.eventBinder.min',
    'backbone.babysitter' : 'lib/backbone.babysitter/lib/amd/backbone.babysitter.min',
    //"underscore.string": 'lib/underscore.string/lib/underscore.string',
    //need to find non-amd version , or the global varaible maybe duplicate with jquery2 ($ and jQuery)
    //jquery110  : 'lib/jquery-110/jquery.min',
     bootstrap  : 'lib/bootstrap/dist/js/bootstrap.min',
    'bootstrap.multiselect' : 'lib/bootstrap-multiselect',
    //bootstrap form validation plugin, cannot work for bootstrap3
    //bootstrapValidation : 'lib/jqBootstrapValidation',
    //jquery valicate
    'jquery.validate' : 'lib/jquery.validate',
    //for jquery file uploader
    'jquery.uploader.main': 'lib/jquery-uploader/_main',
    'load-image': 'lib/blueimp-load-image/js/load-image',
    'tmpl': 'lib/blueimp-tmpl/js/tmpl',
    'canvas-to-blob':'lib/blueimp-canvas-to-blob/js/canvas-to-blob',
    'load-image-meta':'lib/blueimp-load-image/js/load-image-meta',
    'jquery.fileupload-image':'lib/jquery-uploader/jquery.fileupload-image',
    'jquery.fileupload-validate':'lib/jquery-uploader/jquery.fileupload-validate',
    'jquery.fileupload-process':'lib/jquery-uploader/jquery.fileupload-process',
    'jquery.fileupload':'lib/jquery-uploader/jquery.fileupload',
    // 'jquery.iframe-transport':'lib/jquery-uploader/jquery.iframe-transport',
    'jquery.ui.widget':'lib/jquery-uploader/jquery.ui.widget',
    'load-image-exif':'lib/blueimp-load-image/js/load-image-exif',
    'load-image-ios':'lib/blueimp-load-image/js/load-image-ios',
    'jquery.iframe-transport':'lib/jquery-uploader/jquery.iframe-transport',
    'jquery.fileupload-ui':'lib/jquery-uploader/jquery.fileupload-ui',
    'jquery.xdr-transport':'lib/jquery-uploader/jquery.xdr-transport',

    //basic utils
    'string.util':'config/base/string',
    'ajax.setup':'config/jquery/ajax_setup',
    'templates':'templates',
    'flat_ui_custom':'config/jquery/flat_ui_custom',
    'dust_cus_helpers':'config/dust/cus_helpers',
    // 'file.uploader.util':'config/jquery/file_uploader',

    //messager box
    'messenger':'lib/messenger/build/js/messenger',
    'messenger-theme-future':'lib/messenger/build/js/messenger-theme-future',

    //flat ui
    'bootstrap.select':'lib/flatui/bootstrap-select',
    'bootstrap.switch':'lib/flatui/bootstrap-switch',
    'flatui.checkbox':'lib/flatui/flatui-checkbox',
    'flatui.radio':'lib/flatui/flatui-radio',
    'flatui.fileinput':'lib/flatui/flatui-fileinput',
    'image.placeholder':'lib/flatui/holder',
    'jquery-ui':'lib/flatui/jquery-ui-1.10.3.custom.min',
    //ie support html5
    'html5shiv':'lib/flatui/html5shiv',
    'icon-font-ie7':'lib/flatui/icon-font-ie7',
    'jquery.ui.touch-punch':'lib/flatui/jquery.ui.touch-punch.min',
    'jquery.tagsinput':'lib/flatui/jquery.tagsinput',
    //ie support css3
    'respond':'lib/flatui/respond.min',
    'typeahead':'lib/flatui/typeahead',
    'jquery.placeholder':'lib/flatui/jquery.placeholder',

    //elastislide
    'jquery.elastislide':'lib/elastislide/jquery.elastislide',
    'jquerypp.custom':'lib/elastislide/jquerypp.custom',
    'modernizr.custom.17475':'lib/elastislide/modernizr.custom.17475',
    'jquery.elastislide.main':'lib/elastislide/_main',

    'bootstrap-treeview':'lib/bootstrap-treeview/src/js/bootstrap-treeview',

    //ladda button
    'ladda-bootstrap':'lib/ladda-bootstrap/dist/ladda.min',
    'spin':'lib/ladda-bootstrap/dist/spin.min'

    // 'jquery.xdr-transport':'lib/jquery-uploader/jquery.xdr-transport'
  },
  packages: [
    { name: 'lodash',
      location: 'lib/lodash-amd/compat',
      main: 'main'
    },
    // {
    //   name: 'underscore',
    //   location: 'lib/lodash-amd/underscore',
    //   main: 'main'
    // },
    {
      name: 'jquery.uploader',
      location: 'lib/jquery-uploader',
      main: 'main'
    }
  ],
  shim : {
  //  'lib/backbone-localStorage' : ['backbone'],
    underscore : {
      exports : '_'
    },
    backbone : {
      exports : 'Backbone',
      deps : ['jquery','underscore']
    },
    dust : {
       exports : 'dust'
    },
    dustHelper : {
      deps: ['dust']
    },
    bootstrap: {
      deps: ['jquery']
    },
    dustMarionette: {
      deps: ['backbone','marionette','dust','dustHelper']
    },
    "bootstrap.multiselect": {
      deps: ['bootstrap']
    },
    "jquery.uploader":{
      deps:['jquery']
    },
    'ajax.setup':{
       deps:['jquery']
    },
    'templates':{
       deps:['dust']
    },
    'messenger':{
      deps:['jquery']
    },
    'messenger-theme-future':{
      deps:['messenger']
    },
    'jquery-ui':{
      deps:['jquery']
    },
    'bootstrap.switch':{
      deps:['bootstrap']
    },
    'bootstrap.select':{
      deps:['bootstrap']
    },
    'jquery.placeholder':{
      deps:['jquery']
    },
    'jquery.tagsinput':{
      deps:['jquery']
    },
    'app':{
      deps:['ajax.setup','config/_base']
    },
    'jquerypp.custom': {
      deps: ['jquery']
    },
    'jquery.elastislide': {
      deps:['jquery', 'modernizr.custom.17475', 'jquerypp.custom']
    },
    'flat_ui_custom':{
      deps:['jquery','jquery-ui']
    },
    'dust_cus_helpers':{
      deps:['dust','dustHelper']
    },
    'bootstrap-treeview':{
      deps:['bootstrap']
    },
    'ladda-bootstrap':{
      deps:['bootstrap','spin']
    }
        

  },
  deps : ['jquery','underscore']
});

require(['app','ajax.setup','config/_base'],function(App){
  "use strict";
  App.start();

});
