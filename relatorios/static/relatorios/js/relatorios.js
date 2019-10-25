// Filtro médicos
$(document).ready(function() {
    $('.select-medico').select2();
});

$('#data_inicio').change(function(){
    var date = $(this).val();
    if (date.length > 9){
        if (!$('#data_fim').val() || $('#data_fim').val() < date) {
            $('#data_fim').val(date)
        }
    }
});
