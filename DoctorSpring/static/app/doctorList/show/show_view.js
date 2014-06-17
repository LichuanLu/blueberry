define(['utils/reqcmd', 'lodash', 'marionette', 'templates', 'dust', 'dustMarionette', "bootstrap"], function(ReqCmd, Lodash, Marionette, Templates) {
	// body...
	"use strict";
	var DoctorListLayoutView = Marionette.Layout.extend({
		initialize: function() {
			console.log("init DoctorListView");
			this.bindUIElements();
		},
		regions: {
			"doctorListRegion":"#doctor-list-region"
		},
		el: "#doctorlist-content",
		ui: {
			"queryLinks": ".query-table a"
		},
		events: {
			"click @ui.queryLinks": "queryHandler"
		},
		attachEndHandler: function() {

		},
		queryHandler: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			$target.closest('li').addClass("active");
			$target.closest('li').siblings().removeClass("active");

			var skillId = $('#skill-wrapper li.active a').data('skillid');
			var hospitalId = $('#hospital-wrapper li.active a').data('hospitalid');
			console.log("skillId:"+skillId+"hospitalId:"+hospitalId);
			var data = {
				pageNumber:this.doctorListView.currentPage,
				pageSize:6,
				skillId:skillId,
				hospitalId:hospitalId
			}
			ReqCmd.commands.execute("fetchDoctorList:DoctorListLayoutView", $.param(data));
		}

	});

	var DoctorDetailListView = Marionette.CompositeView.extend({
		initialize: function() {
			console.log("init DoctorDetailListView");
			// var doctor = this.model.get("doctor");
			// this.collection = new DoctorEntity.DoctorCollection(doctor);
			// this.listenTo(this.model, 'change', this.render, this);
			this.currentPage = 1;
		},
		onShow: function() {
			console.log("show DoctorDetailListView");
		},
		// tagName:"ul",
		// className:"result-list stylenone",
		ui: {
			"pageLinks": ".pagination-plain a"
			// "currentLi":"li.active"
		},
		events: {
			"click @ui.pageLinks": "changePage"
		},
		template: "doctorDetailList",
		itemViewContainer: ".result-list",
		changePage: function(e) {
			e.preventDefault();
			var $target = $(e.target);
			var $li = $target.closest('li');
			var $currentLi = $('.pagination-plain li.active');
			if ($li.is('.previous')) {
				if (this.currentPage > 1) {
					$currentLi.prev().addClass('active');
					$currentLi.removeClass('active');
					this.currentPage--;
				}

			} else if ($li.is('.next')) {
				if (this.currentPage < this.model.get('pageNumber')) {
					$currentLi.next().addClass('active');
					$currentLi.removeClass('active');
					this.currentPage++;
				}
			} else {
				$li.addClass('active');
				$currentLi.removeClass('active');
				this.currentPage = $li.find('a').text();

			}
			this.fetchNewPage();

		},
		fetchNewPage: function() {
			// console.log($('#select-doctor-modal form').serialize());
			// var data = $('#select-doctor-modal form').serialize();
			var skillId = $('#skill-wrapper li.active a').data('skillid');
			var hospitalId = $('#hospital-wrapper li.active a').data('hospitalid');
			var data = {
				pageNumber:this.currentPage,
				pageSize:6,
				skillId:skillId,
				hospitalId:hospitalId
			}
			ReqCmd.commands.execute("fetchDoctorList:DoctorListLayoutView", $.param(data));
			// if (data) {
			// 	data += '&pageNumber=' + this.currentPage + '&pageSize=6';
			// 	ReqCmd.commands.execute("SelectDoctorModalView:searchDoctorHandler", data);
			// }
		}

	});

	var DoctorDetailItemView = Marionette.ItemView.extend({
		initialize: function() {
			console.log("init DoctorDetailItemView");
			this.listenTo(this.model, 'change', this.render, this);

		},
		template: "doctorDetailItem",
		onRender: function() {
			console.log("item render");
			// get rid of that pesky wrapping-div
			// assumes 1 child element			
			this.$el = this.$el.children();
			this.setElement(this.$el);
		},
		ui: {
			"chooseBtn": ".apply-btn"
		},
		events: {
			"click @ui.chooseBtn": "chooseDoctor"
		},

		onShow: function() {
			console.log("recommand");
			console.dir(this.model);
		},
		chooseDoctor: function(e) {
			e.preventDefault();
			// ReqCmd.commands.execute("selectDoctorItemView:chooseDoctor", this.model);
			// $("#select-doctor-modal").modal('hide');

		}
	});

	return {
		DoctorListLayoutView: DoctorListLayoutView,
		DoctorDetailListView: DoctorDetailListView,
		DoctorDetailItemView: DoctorDetailItemView
	}
});