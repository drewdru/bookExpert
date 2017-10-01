// module admin for process events

function selectModeReasonChange() {
    try {
        var mode = $('#mode_reason option:selected').attr('value');
        mode = mode.split('|')[0];
        $(document.getElementById('comment_reason').options).each(function(index, option) {
            if( option.value.split('|')[0] != mode ) {
                option.hidden = true; // not fully compatible. option.style.display = 'none'; would be an alternative or $(option).hide();
            } else {
                option.hidden = false;
            }
        });
        $('#comment_reason').val(mode + '|1');
    } catch (err) {

    }
}

$(document).ready(function (){
    selectModeReasonChange();
    $('#mode_reason').on('change', function() {
        selectModeReasonChange();
    });

    $('.table-hover tbody tr th').on('click', function() {
        if($(this).attr('name') != undefined)
            window.location = $(this).attr('name');
    });
    $('#filter_type').on('change',function() {
        url = $( '#filter_type option:selected' ).attr('value');
        window.location = url;
    });
    $('#fixlayers').on('change',function() {
        url = $( '#fixlayers option:selected' ).attr('value');
        window.location = url;
    });
    $('#input-search').on('click', function() {
        url = $( '#input-search' ).attr('name') + $('#search').val();
        window.location = url;
    })
    $("input[name=is_actual]").change(function () {
        $("#form-is_actual-change").submit();
    });
});
