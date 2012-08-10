function init_scoring(url_scoring, csrf_token){
    $('.scoring-board td.current').each(function(index){
	// ----------
	// ADD Score
	// ----------
	var add_button = $(this).children('a.score-add');
	add_button.click(function(){
	    var parent = $(this).parent();
	    var content = parent.children('.content');
	    var value = parseInt(content.text());
	    if(value < 8){
		// Add 1 of current scoring
		content.text(parseInt(content.text())+1);
		// RAZ score other team
		var parent_id_split = parent.attr('id').split('team-');
		var other_team_id = parent_id_split[0] + 'team-';
		if(parent_id_split[1] == '1'){
		    other_team_id += '2';
		}else{
		    other_team_id += '1';
		}
		var other_team_content = $('#'+other_team_id+' .content');
		other_team_content.text('0');
	    }
	});
	// ----------
	// SUB Score
	// ----------
	var sub_button = $(this).children('a.score-sub');
	sub_button.click(function(){
	    var parent = $(this).parent();
	    var content = parent.children('.content');
	    var value = parseInt(content.text());
	    if(value > 0){
		content.text(parseInt(content.text())-1);
	    }
	});
    });


    $('.next-end-action').each(function(){
	$(this).click(function(){
	    // Get currents end value of match
	    var ends = $(this).parents('.scoring-board-ctn').find('.scoring-board .current');

	    var id_current = null;
	    var score_current = null;

	    var score_current_0 = parseInt($(ends[0]).children('.content').text());
	    var score_current_1 = parseInt($(ends[1]).children('.content').text());
	    if(score_current_0 >= score_current_1){
		id_current = $(ends[0]).attr('id');
		score_current = score_current_0;
	    }else{
		id_current = $(ends[1]).attr('id');
		score_current = score_current_1;
	    }

	    $.post(url_scoring,
		   {'infos_scoring': id_current,
		    'scoring': score_current},
		   function(data, textStatus, jqXHR){
		       console.log("RESPONSE : ", data);
		       if(data.status == 200){
			   // Temporary - Refresh
			   window.location.reload();
			   // TODO:
			   // Affichage message
			   // Update display and button score to the next end
		       }
		   });
	});
    });

}
