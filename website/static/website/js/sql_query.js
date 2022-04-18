$(function(){
    let url_string = window.location+'';
    var url = new URL(url_string);
    if(!$('[name="query"]').val()){
        var query = url.searchParams.get("query");
        $('[name="query"]').val(query);
    }

    $('#run_query').click(function(){
        let query = $('[name="query"]').val();
        if(query)
        {
            window.location = window.location.origin + window.location.pathname + '?query=' + query;
        }
    });

    class MyAjaxForm extends AJAxForm{
        success(response){
            response = super.success(response);
            if(typeof response == 'object'){
                window.location = window.location.origin + window.location.pathname + '?query=' + response.data.query;
            }
        }
    }
    let af = new MyAjaxForm();
    af.bind_form('form');


    $('#db_tables').select2();
    let selected_tables = $('#db_tables').val() || [];

    $('#db_tables').on('select2:unselecting', function (e) {
        let table_name = e.params.args.data.id;
        $(".table_columns ."+table_name).select2('destroy');
        $(".table_columns ."+table_name).remove();
    });

    $('body').on('select2:unselecting', '.table_columns select.db_columns', function(e){
        let column_name = e.params.args.data.id;
    });

    $('body').on('select2:selecting', '.table_columns select.db_columns', function(e){
        let column_name = e.params.args.data.id;
    });

    let selected_columns = [];
    $('.selected_table_columns .column.selected').each((i, el)=>{
        selected_columns.push(el.html);
    });

    $('#db_tables').on('select2:selecting', function (e) {
        let table_name = e.params.args.data.id;
        let api_url = window.location.origin + '/utils/get_columns?table='+table_name;
        console.log(api_url);
        $.get(api_url).done(function(response){
            let options = '';
            for(let column of response.data){
                options += '<option>'+column+'</option>';
                $('.selected_table_columns').append('<a class="column">'+table_name+'.'+column+'</a>');
            }
            let select_str = '<label style="margin:5px">'+table_name+'</label><select class="db_columns '+table_name+'" multiple="multiple">'+options+'</select>';
            $('.table_columns').append(select_str);
            $('.table_columns .db_columns.'+table_name).select2();
            $('.table_columns .db_columns.'+table_name+' > option').prop("selected", "selected");
            $('.table_columns .db_columns.'+table_name).trigger("change");
        })
    });

    $('body').on('click', '.selected_table_columns .column', function(e){
        $(e.target).toggleClass('selected');
        selected_columns = [];
        $('.selected_table_columns .column.selected').each(function(i, el){
            selected_columns.push(el.innerHTML);
            console.log(selected_columns);
            let columns_str = selected_columns.join(',');
            console.log(columns_str);
            $('input[name="columns"]').val(columns_str);
        });
    });
});