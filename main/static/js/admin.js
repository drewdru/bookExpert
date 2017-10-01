// module admin for autocomplete forms and process events

// autocomplete name_np, rnc, id_street
function show_id_np(str, th_name) {
    if (str.length==0) {
        $('#tip_' + th_name).removeClass('tip-open');
        $('#tip_' + th_name).addClass('tip-close');
        if (th_name == 'id_np_rnc') {
            $('#rnc').val('');
        }        
        return;
    }
    $.ajax({
        url: '/settlements?get_id_np='+str,
        type: "GET",
        dataType: "json",
        success: function(data) {
            $('#tip_' + th_name).text(data.name_np);
            $('#tip_' + th_name).removeClass('tip-close');
            $('#tip_' + th_name).addClass('tip-open');            
            if (th_name == 'id_np_rnc' && !(data.name_np.indexOf('Ошибка') + 1) ) {
                $('#rnc').val('г.' + data.name_np);
            }
            else {
                $('#rnc').val('');
            }
            if ($('#id_street').attr('readonly')){
                $('#id_street').val(data.next_id_street);
            }
            
        }
    });
}

// autocomplete name_street, id_build
function show_id_street(str, th_name) {
    if (str.length==0) {
        $('#tip_' + th_name).removeClass('tip-open');
        $('#tip_' + th_name).addClass('tip-close');
        return;
    }
    $.ajax({
        url: '/street?get_id_np='+$("#id_np").val() + '&get_id_street=' + str,
        type: "GET",
        dataType: "json",
        success: function(data) {      
            $('#tip_' + th_name).text(data.name_street);
            $('#tip_' + th_name).removeClass('tip-close');
            $('#tip_' + th_name).addClass('tip-open');
            $('#id_build').val(data.next_id_build);
        }
    });
}

// autocomplete id_selsov, id_ato, name_ato
function show_id_selsov(str, th_name) {
    if (str.length==0) {
        $('#tip_' + th_name).removeClass('tip-open');
        $('#tip_' + th_name).addClass('tip-close');
        return;
    }
    $.ajax({
        url: '/selsovet/?get_id_selsov='+ str,
        type: "GET",
        dataType: "text",
        success: function(response) {
            response_list = response.split('||');
            name = response_list[0];
            if (response_list.length > 2) {
                id_selsov = response_list[1];
                $('#id_selsov').val(id_selsov);    
                id_ato = response_list[2];
                $('#id_atu').val(id_ato);                
                name_ato = response_list[3];
                $('#tip_id_atu').text(name_ato);
                $('#tip_id_atu').removeClass('tip-close');
                $('#tip_id_atu').addClass('tip-open');
            }            
            $('#tip_' + th_name).text(name);
            $('#tip_' + th_name).removeClass('tip-close');
            $('#tip_' + th_name).addClass('tip-open');
        }
    });
}

// autocomplete id_ato, name_ato
function show_id_ato(str, th_name) {
    if (str.length==0) {
        $('#tip_' + th_name).removeClass('tip-open');
        $('#tip_' + th_name).addClass('tip-close');
        return;
    }
    $.ajax({
        url: '/ATO/?get_id_rayon='+ str,
        type: "GET",
        dataType: "text",
        success: function(response) {  
            response_list = response.split('||');
            name = response_list[0];    
            if (response_list.length > 2) {
                id_ato = response_list[1];
                $('#id_atu').val(id_ato);                
                name_ato = response_list[2];
                $('#tip_id_atu').text(name_ato);
                $('#tip_id_atu').removeClass('tip-close');
                $('#tip_id_atu').addClass('tip-open');
            }            
            $('#tip_' + th_name).text(name);
            $('#tip_' + th_name).removeClass('tip-close');
            $('#tip_' + th_name).addClass('tip-open');
        }
    });
}

// autocomplete code_detail
function show_code_detail(code_reason) {
    $.ajax({
        url: '/info_ref_modify_reason?get_code_detail='+code_reason,
        type: "GET",
        dataType: "json",
        success: function(data) {
            if ($('#code_detail').attr('readonly')){
                $('#code_detail').val(data.next_code_detail);
            }
            
        }
    });
}

// clear autocompleted control where val == -1 or ''
function fix_filter_init() {
    if ($('#id_selsov').val() == -1) {
        $('#id_selsov').val('')
    }
    if ($('#id_atu').val() == -1) {
        $('#id_atu').val('')
    }
}

$(document).ready(function () {
    if(window.location.toString().includes('/street/insert/') || window.location.toString().includes('/doma/insert/')) {
        show_id_np($('#id_np').val(), 'id_np');
    }
    if(window.location.toString().includes('/selsovet/insert/') || window.location.toString().includes('/settlements/insert/')) {
        show_id_ato($('#id_atu').val(), 'id_atu')
    }
    if(window.location.toString().includes('/settlements/insert/')) {
        show_id_selsov($('#id_selsov').val(), 'id_selsov')
    }    
    // fix_filter_init();    
    $('tbody tr').on('click', function() {
        window.location = '/admin/class/' + $(this).find("td:first").html();
    });
    $('#code_reason').on('propertychange input', function (e) {
        var valueChanged = false;
        if (e.type=='propertychange') {
            valueChanged = e.originalEvent.propertyName=='value';
        } else {
            valueChanged = true;
        }
        if (valueChanged) {
            show_code_detail($('#code_reason').val());
        }
    });
    $('input[type="number"]').on('keypress', function (e) {
        e = e || event;
        if (e.ctrlKey || e.altKey || e.metaKey) return;
        var chr = e.key;
        if (chr == 'Backspace' || chr == 'Delete') return;
        if (chr == null) return;
        if (chr < '0' || chr > '9') {
            return false;
        }
    });
});
