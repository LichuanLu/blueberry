require(['messenger', 'messenger-theme-future'], function() {
    // body...
    "use strict";
    // Messenger.options = {
    //     extraClasses: 'messenger-fixed messenger-on-bottom',
    //     theme: 'future'
    // };

    $.ajaxSetup({
        headers: {
            //"X-CTT-CSRF-Token":pageModel.get("token")
        },
        beforeSend: function(xhr, settings) {
            // if (settings.url.indexOf("/file/dld/") == -1 && settings.url.indexOf("/file/upload") == -1 && settings.url.indexOf("/api/") ==-1 && settings.url.indexOf("/upload/") ==-1) {
            //     xhr.setRequestHeader("Accept", "application/vnd.ctt-com.adobe.globalization+json;version=1");
            //     xhr.setRequestHeader("Content-Type", "application/vnd.ctt-com.adobe.globalization+json;version=1");
            // }
            // if (settings.url.indexOf("/rest/loginService") != -1 || settings.url.indexOf("/api/") != -1 || settings.url.indexOf("/manage/setup/product") != -1) {
            //     xhr.setRequestHeader("Accept", "application/json");
            //     xhr.setRequestHeader("Content-Type", "application/json");
            // }
        },
        error: function(data) {
            var error;
            // try {
            //     if (this.url.indexOf("/file/dld/") != -1 || this.url.indexOf("/modules/") != -1) {
            //         error = data.status;
                   
            //         Messenger().post({
            //             message: "%ERROR_MESSAGE:" + data.message,
            //             type: 'error',
            //             showCloseButton: true
            //         });
            //     }
            // } catch (err) {
                if (data.status == 500 && this.url.indexOf("/file/dld/") == -1) {
                    // $.gritter.add({
                    //     title:'Adobe Translation Center',
                    //     text:localization.getString("%ERROR_19999"),
                    //     sticky:false,
                    //     class_name:'alert alert-warning no-shadow'
                    // });
                    //alert("ERROR_19999");
                    Messenger().post({
                        message: "ERROR_500: "+data.message,
                        type: 'error',
                        showCloseButton: true
                    });

                }
                if (data.status == 401) {
                    // if ($("div.loginForm").length == 0) {
                    //     dust.render("login", {}, function (err, output) {
                    //         $("body").append(output);
                    //     });
                    // }
                    // $("div.loginForm #uInput").focus();
                    // top.$.blockUI({ message:$("div.loginForm"), onBlock:function () {
                    //     pageModel.set({modal:true});
                    // }});
                    Messenger().post({
                        message: "ERROR_401",
                        type: 'error',
                        showCloseButton: true
                    });
                }
                if (data.status == 403) {
                    // $.gritter.add({
                    //     title:'Adobe Translation Center',
                    //     text:localization.getString("%ERROR_21004"),
                    //     sticky:false,
                    //     class_name:'alert alert-error no-shadow'
                    // });
                    Messenger().post({
                        message: "ERROR_403",
                        type: 'error',
                        showCloseButton: true
                    });
                }
                if (data.status == 412) {
                    Messenger().post({
                        message: "ERROR_412",
                        type: 'error',
                        showCloseButton: true
                    });
                }
                if (data.status == 404) {
                    //alert("ERROR_412");                
                    Messenger().post({
                        message: "ERROR_404",
                        type: 'error',
                        showCloseButton: true
                    });
                }
            
            //handle error than trigger onError for each ajax request
            try {
                this.onError(data);
            } catch (err) {

            }
        }
    });

    $.getUrlVar = function(key) {
        var result = new RegExp(key + "=([^&]*)", "i").exec(window.location.search);
        return result && unescape(result[1]) || "";
    };
});