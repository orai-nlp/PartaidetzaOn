/////////////////// IMAGE SWITCHER ///////////////////////
function change_images()
{
	if(timerid)
	{
		timerid = 0;
	}
	var tDate = new Date();
	
	if(countimages == images.length)
	{
		countimages = 0;
	}
	if(tDate.getSeconds() % 5 == 0)
	{
		document.getElementById("id_image").src = images[countimages];
	}
	countimages++;
	timerid = setTimeout("change_images()", 1000);
}

//////////////////// IMAGE PREVIEW /////////////////////////

function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var format = input.files[0].name.split('.')[input.files[0].name.split('.').length-1];
            if ($.inArray(format.toLowerCase(),accepted_image_formats) >= 0 || $.inArray(format,accepted_image_formats) >= 0){
                reader.onload = function (e) {
                    $('#imgPreview').attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
}

/////////////////////////////////////////////////////////////

function load_errorlist_changes(){
    $(document).ready(function(){
        $('.errorlist').each( function( index, element ){
          $(this).prev().addClass("errorInput")
        });
    });
}


function get_coordinates(){
    var coordinates = $("#id_coordinates");
    $(layer_array).each(function( index, element ){
        coordinates.val(coordinates.val()+"["+$(this)[0]+","+$(this)[1]+"]|");
    });

}



function load_register_scripts(){
    /* Loads register template's javascripts */
       
    $(document).ready(function(){
        $('#id_institution_name_div').fadeOut();
        $('#id_institution').change(function(){
            if(this.checked)
                $('#id_institution_name_div').fadeIn('slow');
            else
                $('#id_institution_name_div').fadeOut('slow');

        });
    });
    
}

function load_profile_scripts(){
    /* Loads register template's javascripts */
       
    $(document).ready(function(){
        $('#id_institution').change(function(){
            if(this.checked)
                $('#id_institution_name_div').fadeIn('slow');
            else
                $('#id_institution_name_div').fadeOut('slow');

        });
    });
    
}

function manage_proposal_scripts(){
    $(document).ready(function() {
        $('#proposals_table').DataTable();
    } );
    
    $('#proposals_table tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        if ($(this).hasClass("selected")){
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+","+$(this).attr("id"));
            $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href")+","+$(this).attr("id"));
        }
        else{
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace(","+$(this).attr("id"),""));
            $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href").replace(","+$(this).attr("id"),""));
        }
    } );
}

function manage_accepted_proposal_scripts(){
    $(document).ready(function() {
        $('#projects_table').DataTable();
    } );
    
    $('#projects_table tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        if ($(this).hasClass("selected")){            
            $("#id_delete_projects").attr("href", $("#id_delete_projects").attr("href")+","+$(this).attr("id"));
        }
        else{            
            $("#id_delete_projects").attr("href", $("#id_delete_projects").attr("href").replace(","+$(this).attr("id"),""));
        }
    } );
}

function manage_my_proposal_scripts(){
    $(document).ready(function() {
        $('#proposals_table').DataTable();
    } );
    
}

function manage_criterion_scripts(){
    $(document).ready(function() {
        $('#criterions_table').DataTable();
        $('#criterions_table').change(function() {
            $(".criterion_checkbox_criterion").click(function() {
                var change_element;
                change_element = $(this).next();
                change_element.val("changed");
            } );
        } );
        
        $(".criterion_checkbox_criterion").click(function() {
            var change_element;
            change_element = $(this).next();
            change_element.val("changed");
        } );
    } );
    
    
}



function load_proposal_scripts(){

    $('#area_modal').on('shown.bs.modal', function () {
      $("#id_modal_area").chosen();
    });
 
    $('#criterions_table').DataTable({ bPaginate : false});
        $('#criterions_table').change(function() {
            $(".criterion_checkbox_criterion").click(function() {
                var change_element;
                change_element = $(this).next();
                change_element.val("changed");
            } );
        } );
        
    $(".criterion_checkbox_criterion").click(function() {
        var change_element;
        change_element = $(this).next();
        change_element.val("changed");
    } );
    
    $(function() {
        $('.upload_p').formset({
        });
    });
}

function load_accepted_proposal_scripts(){
    
    $('#area_modal').on('shown.bs.modal', function () {
      $("#id_modal_area").chosen();
    });
    
    $(function() {
        $('.upload_p').formset({
        });
    });
}

/* MODAL FORM FUNCTIONS */

function remove_error_messages(modal_id){
    $(modal_id).find("#response").each( function( index, element ){
          $(this).remove();
        });
}

function save_proposal_area(proposal_id){

    var area = $("#id_modal_area").val();
    $.ajax({
          url: '/ajax_edit_proposal_area',
          async: false,
          data: {proposal_id: proposal_id, area:area},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response");
            if (response != ""){
                remove_error_messages("#area_modal");
                $("#area_modal").modal('hide');
                $("#id_area").html(response);
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_area").after(data);
            }
            
         }   
          
    });
}

function save_proposal_cost(proposal_id){

    var cost = $("#id_modal_cost").val();
    $.ajax({
          url: '/ajax_edit_proposal_cost',
          async: false,
          data: {proposal_id: proposal_id, cost:cost},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#cost_modal");
                $("#cost_modal").modal('hide');
                $("#id_cost").html(cost);
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_cost").after(data);
            }
            
         }   
          
    });
}

function save_proposal_recipient_number(proposal_id){

    var recipient_number = $("#id_modal_recipient_number").val();
    $.ajax({
          url: '/ajax_edit_proposal_recipient_number',
          async: false,
          data: {proposal_id: proposal_id, recipient_number:recipient_number},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_number_modal");
                $("#recipient_number_modal").modal('hide');
                $("#id_recipient_number").html(recipient_number);
                }
            else{
                remove_error_messages("#recipient_number_modal");
                $("#id_modal_recipient_number").after(data);
            }
            
         }
   
    });
}

function save_proposal_title(proposal_id, selected_language){
    title_inputs = $("#title_div input");
    $(title_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var title = $(this).val();
        $.ajax({
          url: '/ajax_edit_proposal_title',
          async: false,
          data: {proposal_id: proposal_id, language:language, title:title},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#title_modal");
                $("#title_modal").modal('hide');
                if (selected_language == language){
                    $("#id_title").html(title);
                }
            }
            else{
                remove_error_messages("#title_modal");
                $("#id_modal_title").after(data);
            }                       
         }
        });
   });
}

function save_proposal_summary(proposal_id, selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        $.ajax({
          url: '/ajax_edit_proposal_summary',
          async: false,
          data: {proposal_id: proposal_id, language:language, summary:summary},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#summary_modal");
                $("#summary_modal").modal('hide');
                if (selected_language == language){
                    $("#id_summary").html(summary);
                }
            }
            else{
                remove_error_messages("#summary_modal");
                $("#id_modal_summary").after(data);
            }                       
         }
        });
   });
}

function save_proposal_recipient(proposal_id, selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        $.ajax({
          url: '/ajax_edit_proposal_recipient',
          async: false,
          data: {proposal_id: proposal_id, language:language, recipient:recipient},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_modal");
                $("#recipient_modal").modal('hide');
                if (selected_language == language){
                    $("#id_recipient").html(recipient);
                }
            }
            else{
                remove_error_messages("#recipient_modal");
                $("#id_modal_recipient").after(data);
            }                       
         }
        });
   });
}


function save_proposal_necessity(proposal_id, selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        $.ajax({
          url: '/ajax_edit_proposal_necessity',
          async: false,
          data: {proposal_id: proposal_id, language:language, necessity:necessity},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#necessity_modal");
                $("#necessity_modal").modal('hide');
                if (selected_language == language){
                    $("#id_necessity").html(necessity);
                }
            }
            else{
                remove_error_messages("#necessity_modal");
                $("#id_modal_necessity").after(data);
            }                       
         }
        });
   });
}


function save_proposal_where(proposal_id, selected_language){
    where_inputs = $("#where_div textarea");
    $(where_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        $.ajax({
          url: '/ajax_edit_proposal_where',
          async: false,
          data: {proposal_id: proposal_id, language:language, where:where},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#where_modal");
                $("#where_modal").modal('hide');
                if (selected_language == language){
                    $("#id_where").html(where);
                }
            }
            else{
                remove_error_messages("#where_modal");
                $("#id_modal_where").after(data);
            }                       
         }
        });
   });
}


function close_proposal_title(selected_language){
    title_inputs = $("#title_div input");
    $(title_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var title = $(this).val();
        remove_error_messages("#title_modal");
        $("#title_modal").modal('hide');
        if (selected_language == language){
            $("#id_title").html(title);
        }
   });
}


function close_proposal_summary(selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        remove_error_messages("#summary_modal");
        $("#summary_modal").modal('hide');
        if (selected_language == language){
            $("#id_summary").html(summary);
        }
   });
}


function close_proposal_recipient(selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        remove_error_messages("#recipient_modal");
        $("#recipient_modal").modal('hide');
        if (selected_language == language){
            $("#id_recipient").html(recipient);
        }
   });
}

function close_proposal_necessity(selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        remove_error_messages("#necessity_modal");
        $("#necessity_modal").modal('hide');
        if (selected_language == language){
            $("#id_necessity").html(necessity);
        }
   });
}

function close_proposal_where(selected_language){
    where_inputs = $("#where_div textarea");
    $(where_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        remove_error_messages("#where_modal");
        $("#where_modal").modal('hide');
        if (selected_language == language){
            $("#id_where").html(where);
        }
   });
}

function close_proposal_source(selected_language){
    source_inputs = $("#source_div textarea");
    $(source_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var source = $(this).val();
        remove_error_messages("#source_modal");
        $("#source_modal").modal('hide');
        if (selected_language == language){
            $("#id_source").html(source);
        }
   });
}


function close_proposal_explanation(selected_language){
    explanation_inputs = $("#explanation_div textarea");
    $(explanation_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var explanation = $(this).val();
        remove_error_messages("#explanation_modal");
        $("#explanation_modal").modal('hide');
        if (selected_language == language){
            $("#id_explanation").html(explanation);
        }
   });
}

function close_proposal_area(){

    var area = $("#id_area").val();
    remove_error_messages("#area_modal");
    $.ajax({
          url: '/ajax_get_proposal_area',
          async: false,
          data: {area:area},
          dataType:'html',
          success : function(data, status, xhr){           
           remove_error_messages("#area_modal");
           $("#area_modal").modal('hide');
           $("#id_area_p").html(data);

         }   
          
    });   
    
}

function close_proposal_cost(){

    var cost = $("#id_cost").val();
    remove_error_messages("#cost_modal");
    $("#cost_modal").modal('hide');
    $("#id_cost_p").html(cost);
}

function close_proposal_recipient_number(){

    var recipient_number = $("#id_recipient_number").val();
    remove_error_messages("#recipient_number_modal");
    $("#recipient_number_modal").modal('hide');
    $("#id_recipient_number_p").html(recipient_number);
}

function close_proposal_attached_documents(){
    
    $("#attached_documents_modal").modal('hide');
}

function close_proposal_proposal(){

    var proposal = $("#id_proposal").val();
    remove_error_messages("#proposal_modal");
    $("#proposal_modal").modal('hide');
    $("#id_proposal_p").html(proposal);
}

function close_proposal_state(){

    var state = $("#id_state").val();
    remove_error_messages("#state_modal");
    $.ajax({
          url: '/ajax_get_proposal_state',
          async: false,
          data: {state:state},
          dataType:'html',
          success : function(data, status, xhr){           
           remove_error_messages("#state_modal");
           $("#state_modal").modal('hide');
           $("#id_state_p").html(data);

         }   
          
    }); 
}


////////////////////////////////////

function save_project_area(project_id){

    var area = $("#id_modal_area").val();
    $.ajax({
          url: '/ajax_edit_project_area',
          async: false,
          data: {project_id: project_id, area:area},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response");
            if (response != ""){
                remove_error_messages("#area_modal");
                $("#area_modal").modal('hide');
                $("#id_area").html(response);
                }
            else{
                remove_error_messages("#area_modal");
                $("#id_modal_area").after(data);
            }
            
         }   
          
    });
}

function save_project_cost(project_id){

    var cost = $("#id_modal_cost").val();
    $.ajax({
          url: '/ajax_edit_project_cost',
          async: false,
          data: {project_id: project_id, cost:cost},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#cost_modal");
                $("#cost_modal").modal('hide');
                $("#id_cost").html(cost);
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_cost").after(data);
            }
            
         }   
          
    });
}

function save_project_recipient_number(project_id){

    var recipient_number = $("#id_modal_recipient_number").val();
    $.ajax({
          url: '/ajax_edit_project_recipient_number',
          async: false,
          data: {project_id: project_id, recipient_number:recipient_number},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_number_modal");
                $("#recipient_number_modal").modal('hide');
                $("#id_recipient_number").html(recipient_number);
                }
            else{
                remove_error_messages("#recipient_number_modal");
                $("#id_modal_recipient_number").after(data);
            }
            
         }
   
    });
}

function save_project_title(project_id, selected_language){
    title_inputs = $("#title_div input");
    $(title_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var title = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_title',
          async: false,
          data: {project_id: project_id, language:language, title:title},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#title_modal");
                $("#title_modal").modal('hide');
                if (selected_language == language){
                    $("#id_title").html(title);
                }
            }
            else{
                remove_error_messages("#title_modal");
                $("#id_modal_title").after(data);
            }                       
         }
        });
   });
}

function save_project_summary(project_id, selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_summary',
          async: false,
          data: {project_id: project_id, language:language, summary:summary},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#summary_modal");
                $("#summary_modal").modal('hide');
                if (selected_language == language){
                    $("#id_summary").html(summary);
                }
            }
            else{
                remove_error_messages("#summary_modal");
                $("#id_modal_summary").after(data);
            }                       
         }
        });
   });
}

function save_project_recipient(project_id, selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_recipient',
          async: false,
          data: {project_id: project_id, language:language, recipient:recipient},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_modal");
                $("#recipient_modal").modal('hide');
                if (selected_language == language){
                    $("#id_recipient").html(recipient);
                }
            }
            else{
                remove_error_messages("#recipient_modal");
                $("#id_modal_recipient").after(data);
            }                       
         }
        });
   });
}


function save_project_necessity(project_id, selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_necessity',
          async: false,
          data: {project_id: project_id, language:language, necessity:necessity},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#necessity_modal");
                $("#necessity_modal").modal('hide');
                if (selected_language == language){
                    $("#id_necessity").html(necessity);
                }
            }
            else{
                remove_error_messages("#necessity_modal");
                $("#id_modal_necessity").after(data);
            }                       
         }
        });
   });
}

function save_project_where(project_id, selected_language){
    where_inputs = $("#where_div textarea");
    $(where_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_where',
          async: false,
          data: {project_id: project_id, language:language, where:where},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#where_modal");
                $("#where_modal").modal('hide');
                if (selected_language == language){
                    $("#id_where").html(where);
                }
            }
            else{
                remove_error_messages("#where_modal");
                $("#id_modal_where").after(data);
            }                       
         }
        });
   });
}


function save_project_source(project_id, selected_language){
    source_inputs = $("#source_div textarea");
    $(source_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var source = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_source',
          async: false,
          data: {project_id: project_id, language:language, source:source},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#source_modal");
                $("#source_modal").modal('hide');
                if (selected_language == language){
                    $("#id_source").html(source);
                }
            }
            else{
                remove_error_messages("#source_modal");
                $("#id_modal_source").after(data);
            }                       
         }
        });
   });
}


function save_project_explanation(project_id, selected_language){
    explanation_inputs = $("#explanation_div textarea");
    $(explanation_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var explanation = $(this).val();
        $.ajax({
          url: '/ajax_edit_project_explanation',
          async: false,
          data: {project_id: project_id, language:language, explanation:explanation},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#explanation_modal");
                $("#explanation_modal").modal('hide');
                if (selected_language == language){
                    $("#id_explanation").html(explanation);
                }
            }
            else{
                remove_error_messages("#explanation_modal");
                $("#id_modal_explanation").after(data);
            }                       
         }
        });
   });
}
/* -------------------- */

function load_main_scripts(){
    var date = new Date();
    $('#id_agenda').datepicker({
       beforeShowDay: function(date) {
            var m = date.getMonth(), d = date.getDate(), y = date.getFullYear();
            for (i = 0; i < dates.length; i++) {
                if($.inArray(y + '-' + (m+1) + '-' + d,dates) != -1) {
                    //return [false];
                    return [true, 'to-highlight', ''];
                }
            }
            return [true];

        }
    });
}

function load_search_scripts(){
    $("#id_main_search_box").val($("#id_search_query").val());
}

function submit_search(){
    $("#id_search_query").val($("#id_main_search_box").val());
    $('#search_form_id').submit();
}
    

function more_like_this_in(input_element, type, where){
    var input_element_id = $(input_element).attr('id');
    var language = input_element_id.split('-')[0].split('_')[2];
    var query = $(input_element).val();
    $.ajax({
          url: '/ajax_more_like_this_in_'+where,
          async: false,
          data: {query:query, language:language, type:type},
          dataType:'html',
          success : function(data, status, xhr){
            if (data.indexOf("<li>") >= 0){
                $("#related_objects_"+where).hide();
                $("#related_objects_"+where+" ul").remove();
                var old_html = $("#related_objects_"+where).html();
                $("#related_objects_"+where).html(old_html+data);
                $("#related_objects_"+where).show(1000);
            }
            else{
                $("#related_objects_"+where).hide(1000);
            }
          } 
    });
}

function correct_language(input_element, where){
    var input_element_id = $(input_element).attr('id');
    var language = input_element_id.split('-')[0].split('_')[2]; 
    var text = $(input_element).val();
    if (text!=""){
        $.ajax({
              url: '/ajax_correct_language',
              async: false,
              data: {language:language, text:text},
              dataType:'html',
              success : function(data, status, xhr){            
               var response;
               response = $(data+" #response").text(); 
               if (response=="True"){
                $("#language_error_"+where).hide(1000);
               }
               else{
                $("#language_error_"+where).show(1000);
               }
              } 
        });
    }

}


function validate_input_languages(){
    var no_errors = true;
    var json = create_proposal_json();
    
    

}

function create_language_json(element, type, json){
    $('#'+element+'_div '+type).each(function() {        
        var input_element_id = $(this).attr('id');
        var language = input_element_id.split('-')[0].split('_')[2]; 
        var text = $(this).val();
        json[element+'_'+language]=text;
    });
    
    return json;
}


function language_validation_dialog(message) {
    $("#dialog-confirm").html(message);

    // Define the Dialog and its properties.
    try{
    $("#dialog-confirm").dialog({
        resizable: false,
        modal: true,
        title: "Modal",
        height: 250,
        width: 400,
        buttons: {
            "Yes": function () {
                $(this).dialog('close');
                
                try{
                    $("#id_new_proposal_button").attr("onclick","");
                    $("#id_new_proposal_button").click();
                }
                catch(error){}
                try{
                    $("#id_new_accepted_proposal_button").attr("onclick","");
                    $("#id_new_accepted_proposal_button").click();
                }
                catch(error){}
            },
                "No": function () {
                $(this).dialog('close');
                return false;
            }
        }
    });
    }
    catch(ex){
        alert(ex);
    }
}

function validate_language(message){
    var json = {};
    json = create_language_json("title", "input", json);
    json = create_language_json("summary", "textarea", json);
    json = create_language_json("recipient", "textarea", json);
    json = create_language_json("necessity", "textarea", json);
    json = create_language_json("where", "textarea", json);

    var ajax_response;
    $.when($.ajax({
          url: '/ajax_validate_language',
          async: false,
          data: json,
          dataType:'json',
          complete: function(jqXHR,status)
            {
                if (jqXHR.responseText.indexOf("False") >= 0){
                    ajax_response = false;
                }
                else{
                    ajax_response = true;
                }
            }
            
        })
        );
    

    if (!ajax_response){
        language_validation_dialog(message);
    }
    return ajax_response;
}


function load_add_event_scripts(){
    
    $('#id_date').datepicker();

    $('#event_div textarea').focusout(function() {
        //more_like_this_in($(this),"Event", "event");
        correct_language($(this),"event");
    });
}

function load_agenda_scripts(){
    
    var date = new Date();
    $('#id_agenda').datepicker({
       beforeShowDay: function(date) {
            var m = date.getMonth(), d = date.getDate(), y = date.getFullYear();
            for (i = 0; i < dates.length; i++) {
                if($.inArray(y + '-' + (m+1) + '-' + d,dates) != -1) {
                    //return [false];
                    return [true, 'to-highlight', ''];
                }
            }
            return [true];

        }
    });
   
}

function load_add_proposal_scripts(){
    
    $('#area_modal').on('shown.bs.modal', function () {
      $("#id_area").chosen();
    });
    
    $(".upload_p input").change(function(){
    readURL(this);
    });

    $(function() {
        $('.upload_p').formset({
    });
    $('#title_div input').focusout(function() {
        more_like_this_in($(this),"Proposal", "title");
        correct_language($(this),"title");
    });
    $('#summary_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "summary");
        correct_language($(this),"summary", "summary");
    });
    $('#recipient_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "recipient"); 
        correct_language($(this),"recipient", "recipient");       
    });
    $('#necessity_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "necessity");
        correct_language($(this),"necessity", "necessity");
    });
    $('#where_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "where");
        correct_language($(this),"where", "where");
    });
  })
    
}

function load_add_accepted_proposal_scripts(){
    
    $('#area_modal').on('shown.bs.modal', function () {
      $("#id_area").chosen();
    });
    
    $(".upload_p input").change(function(){
    readURL(this);
    });
    
    
    $('#title_div input').focusout(function() {
        more_like_this_in($(this),"Proposal", "title");
        correct_language($(this),"title");
    });
    $('#summary_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "summary");
        correct_language($(this),"summary", "summary");
    });
    $('#recipient_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "recipient"); 
        correct_language($(this),"recipient", "recipient");       
    });
    $('#necessity_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "necessity");
        correct_language($(this),"necessity", "necessity");
    });
    $('#where_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "where");
        correct_language($(this),"where", "where");
    });
    $('#source_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "source");
        correct_language($(this),"source", "source");
    });
    $('#explanation_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "explanation");
        correct_language($(this),"explanation", "explanation");
    });
  }
    




function paginated_search(url){
    $('#search_form_id').attr('action',$('#search_form_id').attr('action')+url);
    $('#search_form_id').submit();
}


/* VOTE SYSTEM */

function mark_as_voted(id){
    $( "#id_vote_show_"+id ).addClass("voted");
    $( "#id_vote_show_"+id ).attr('disabled', true);
}

function vote_via_ajax(project_id){
    $.ajax({
          url: '/ajax_vote',
          async: false,
          data: {project_id:project_id},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                // mark as voted
                mark_as_voted(project_id);
                // Increment votes
                var votes = parseInt($( "#id_vote_show_"+project_id ).prev().find("span").text());
                votes ++;
                $( "#id_vote_show_"+project_id ).prev().find("span").text(votes);
            }
                       
               
          }
    });
}

/* FOND SYSTEM */

function mark_as_fonded(id){
    $( "#id_fond_show_"+id ).addClass("voted");
    $( "#id_fond_show_"+id ).attr('disabled', true);
}

function fond_via_ajax(proposal_id){
    $.ajax({
          url: '/ajax_fond',
          async: false,
          data: {proposal_id:proposal_id},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                // mark as fonded
                mark_as_fonded(proposal_id);
                // Increment fonds
                var fonds = parseInt($( "#id_fond_show_"+proposal_id ).prev().find("span").text());
                fonds ++;
                $( "#id_fond_show_"+proposal_id ).prev().find("span").text(fonds);
            }
                       
               
          }
    });
}


/* ------------------------------------ */


function add_point_to_map_proposal(latlng,proposal_id){

    $.ajax({
          url: '/ajax_add_point_to_map_proposal',
          async: false,
          data: {proposal_id:proposal_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}

function add_point_to_map_project(latlng,project_id){

    $.ajax({
          url: '/ajax_add_point_to_map_project',
          async: false,
          data: {project_id:project_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}
            
            
function delete_point_from_map_proposal(latlng,proposal_id){

    $.ajax({
          url: '/ajax_delete_point_from_map_proposal',
          async: false,
          data: {proposal_id:proposal_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}
            
function delete_point_from_map_project(latlng,project_id){

    $.ajax({
          url: '/ajax_delete_point_from_map_project',
          async: false,
          data: {project_id:project_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}

