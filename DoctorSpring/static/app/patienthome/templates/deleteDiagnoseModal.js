(function(){dust.register("deleteDiagnoseModal",body_0);function body_0(chk,ctx){return chk.write("   <div class=\"modal-dialog\"><div class=\"modal-content\"><div class=\"modal-header\"><button type=\"button\" class=\"close fui-cross\" data-dismiss=\"modal\" aria-hidden=\"true\"></button><h4 class=\"modal-title\">撤销诊断请求</h4></div><div class=\"modal-body\" id=\"confirm-form\" data-id=\"").reference(ctx.get(["id"], false),ctx,"h").write("\"><p>您确定需要撤销诊断请求吗？一旦撤销后将无法恢复。</p></div><div class=\"modal-footer\"><button name=\"cancel\" data-dismiss=\"modal\" class=\"btn btn-default\">取消</button><button name=\"save\" class=\"btn btn-primary\">确定</button></div></div></div> ");}return body_0;})();