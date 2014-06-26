define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'login/login_app', 'dust', 'dustMarionette', "bootstrap", 'jquery.elastislide.main'], function(ReqCmd, Lodash, Marionette, Templates, LoginApp) {
	// body...
	"use strict";
	var HomePageLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init FollowUserLayoutView");
			this.bindUIElements();
		},
		regions: {},
		el: "#homepage-content",
		ui: {
			'preview': '#preview',
			'carouselEl': '#carousel',
			'previewWrapper':'.doctor-preview-des'
		},
		events: {},
		attachEndHandler: function() {
			//init gallary
			var current = 0;
			this.ui.carouselItems = this.ui.carouselEl.children();
			//console.log(this.ui.carouselEl);
			//console.log(this.ui.carouselItems);
			var that = this;
			var homeCarousel = this.ui.carouselEl.elastislide({
				current: current,
				minItems: 4,
				onReady: function() {

					that.changeImage(that.ui.carouselItems.eq(current), current);

				},
				onClick: function(el, pos, evt) {
					that.changeImage(el, pos);
					evt.preventDefault();
				},
				onHover: function(el, pos, evt) {
					that.changeImage(el, pos);
					//evt.preventDefault();
					that.changeInfo(el,pos);
				}
			});
			//console.dir(myCarousel);
			//init flatui
			$('.input-group').on('focus', '.form-control', function() {
				$(this).closest('.input-group, .form-group').addClass('focus');
			}).on('blur', '.form-control', function() {
				$(this).closest('.input-group, .form-group').removeClass('focus');
			});

			//init login modal
			LoginApp.loginAction();
			setInterval(that.autoScroll, 3000);


		},
		autoScroll: function(obj) {

			$('.action-wrap').find("ul:first").animate({
				marginTop: "-40px"
			}, 1000, function() {
				$(this).css({
					marginTop: "0px"
				}).find("li:first").appendTo(this);
			});

			// $('.feedback-wrapper').find("ul:first").animate({
			// 	marginTop: "-90px"
			// }, 1000, function() {
			// 	$(this).css({
			// 		marginTop: "0px"
			// 	}).find("li:first").appendTo(this);
			// });
		},
		changeImage: function(el, pos) {
			this.ui.preview.attr('src', el.data('preview'));
			this.ui.carouselItems.removeClass('current-img');
			el.addClass('current-img');
			//myCarousel.setCurrent(pos);

		},
		changeInfo: function(el, pos) {
			this.ui.previewWrapper.find('h6').html(el.find('h6').html());
			this.ui.previewWrapper.find('.hospital').html(el.find('.hospital').html());
			this.ui.previewWrapper.find('.skill').html(el.find('.skill').html());
			this.ui.previewWrapper.find('.doctor-link').attr('href',el.find('.doctor-link').html())
		}

	});

	return {
		HomePageLayoutView: HomePageLayoutView
	}
});