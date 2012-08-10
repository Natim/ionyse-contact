function shuffle_nav_cols_2(){
	var size = $("#nav-cols-2").width();	
	
	if (size >= 100) {
		$("#nav-cols-2 .reduce a:first-child").html(">>");
		$("#nav-cols-2 .content-col").fadeOut();
		$("#nav-cols-2").animate({
		    width: '30px'
		  }, 400, function() {
		    // Animation complete.
		  });
		  $("#nav-cols-content").animate({
		    left: '220px'
		  }, 400, function() {
		    // Animation complete.
		  });
	}else{
		
		$("#nav-cols-2 .reduce a:first-child").html("<<");

		$("#nav-cols-2").animate({
		    width: '350px'
		  }, 400, function() {
		  	$("#nav-cols-2 .content-col").fadeIn();
		  });
		$("#nav-cols-content").animate({
		    left: '530px'
		  }, 400, function() {
		    // Animation complete.
		  });
	}
	
}

$(document).ready(function () {

	if($(window).width() <= 1024){
		$("#nav-cols-2 .reduce a:first-child").html(">>");
		$("#nav-cols-2 .content-col").hide();
		$("#nav-cols-2").css('width', '30px');
		$("#nav-cols-content").css('left', '220px');
	}
	
});

