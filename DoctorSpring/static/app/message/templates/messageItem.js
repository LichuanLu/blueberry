(function(){dust.register("messageItem",body_0);function body_0(chk,ctx){return chk.write("<li class=\"message-item\" data-id=\"").reference(ctx.get(["id"], false),ctx,"h").write("\"><a href=\"").reference(ctx.get(["url"], false),ctx,"h").write("\" class=\"message-link\"><div class=\"icon\"><img alt=\"\" src=\"/static/assets/Icons/PNG/clipboard.png\"></div><div class=\"top-wrapper\"><span class=\"title\">").reference(ctx.get(["title"], false),ctx,"h").write("</span><div class=\"right-content\"><span class=\"date\">").reference(ctx.get(["createTime"], false),ctx,"h").write("</span></div></div><div class=\"message-content-wrapper\"><p>").reference(ctx.get(["content"], false),ctx,"h").write("</p></div></a></li>");}return body_0;})();