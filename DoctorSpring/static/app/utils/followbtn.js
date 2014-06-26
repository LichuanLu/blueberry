define([], function() {
	"use strict";
	$.fn.followaction = function(option, event) {
		//get the args of the outer function..
		// var args = arguments;
		//var value;
		var chain = this.each(function() {
			var $this = $(this),
				$atext = $(this).find('.a-text'),
				uid = $this.data('uid'),
				followid = $this.data('id'),
				type = $this.data('type'),
				options = typeof option == 'object' && option,
				url,
				data="",
				isRemove;
			// var l = ladda.create(this);


			$this.hover(function(e) {
				console.log("hover in");
				if ($this.is('.following')){
					$atext.text('取消收藏');
				}

			}, function(e) {
				console.log("hover out");
				if ($this.is('.following')){
					$atext.text('已收藏');

				}
			});


			if (uid) {

				$this.click(function(e) {


					if ($this.is('.following')) {
						url = "/userFavorties/"+followid+"/cancel";
						isRemove = true;

					} else {
						url = "/userFavorties/add";
						data = "doctorId="+uid+"&type="+type;
						isRemove = false;
					}
					$this.attr('disabled', 'disabled');
					//$atext.text('收藏中');



					$.ajax({
						url: url,
						data: data,
						dataType: "json",
						type: 'POST',
						success: function(res) {
							if (res.status != 0) {
								this.onError(res);

							} else {
								console.dir(res.data);
								console.dir(this.url);
								$this.removeAttr('disabled');

								if(isRemove){
									$this.removeClass('following');
									$atext.text('加入收藏');

								}else{
									$this.addClass('following');
									$atext.text('已收藏');

								}
								
							}
							//allowSubmit = true;
						},
						onError: function(res) {
							$this.removeAttr('disabled');
							if (typeof res.msg !== 'undefined') {
								Messenger().post({
									message: "%ERROR_MESSAGE:" + res.msg,
									type: 'error',
									showCloseButton: true
								});
							}

						}

					});
				});

			}
		});
	}

});