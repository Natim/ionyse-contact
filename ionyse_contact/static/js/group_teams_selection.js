/*****************************
 * Edition Teams of Group
/****************************/

var group_infos = null;

function init_group_teams(group_infos_str){

    // Init teams infos
    group_infos = eval('(' + group_infos_str + ')');

    console.log('GROUP INFOS:', group_infos);
 
    $('.placeholder').disableSelection();
    $('.team').draggable({
	cursor: 'move',
	stack: '.team',
	start: function(event, ui){
	    $(this).draggable( 'option', 'revert', true );
	},
    });

    $('.placeholder').droppable({
	accept: function(draggable){
	    // Accept all div with 'team' class
	    if(draggable.hasClass('team')){
		return true;
	    }
	    return false;
	},
    	hoverClass: 'droppable',
    	drop: function(event, ui) {

	    console.log('draggable', ui.draggable);

	    // Graggable item
	    var draggable_id = parseInt(ui.draggable.attr('id').split('-')[1]);
	    // Placeholder source
	    var source_id = group_infos.teams_order[draggable_id];
	    var source = null;
	    if(source_id){
		source = $('#placeholder-'+source_id);
	    }
	    // Placeholder target
	    var target = $(this);
	    var target_id = parseInt(target.attr('id').split('-')[1]);
	    // Child item of droppable (target) placeholder
	    var child_id = group_infos.group_order[target_id-1];

	    console.log('draggable_id', draggable_id);
	    console.log('source_id', source_id);
	    console.log('source', source);
	    console.log('target', target);
	    console.log('target_id', target_id);
	    console.log('child_id', child_id);

	    // Update draggable item
	    ui.draggable.draggable( 'option', 'revert', false );
	    ui.draggable.position({ of: $(this), my: 'left top', at: 'left top' });
	    ui.draggable.removeClass('available');
	    ui.draggable.addClass('organized');

	    // Update group_infos for draggable item and target placeholder
	    group_infos.group_order[target_id-1] = draggable_id;
	    group_infos.teams_order[draggable_id] = target_id;

	    // Update droppable placeholder style
	    $(this).removeClass('empty');

	    // Update droppable child item and source placeholder
	    if( child_id ){
	    	// New Position for child item
	    	var child = $('#team-'+child_id);
	    	child.position({ of: source, my: 'left top', at: 'left top' });
		// Update group_infos for source placeholder and child item
		group_infos.group_order[source_id-1] = child_id;
		group_infos.teams_order[child_id] = source_id;
	    }else{
		if(source){
	    	    // Empty style for source placeholder
	    	    source.addClass('empty');
		    // Update group_infos
		    group_infos.group_order[source_id-1] = null;
		}
	    }
	    
	    console.log('New group infos :', group_infos);
    	},
    });
}

function save_button_action(){
    console.log('preparing data...');
    $("#group-infos-input").attr('value', JSON.stringify(group_infos));
    // Submit form
    $("#group-teams-form").submit();
}