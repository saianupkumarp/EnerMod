
$(function() {
    //Page Tabs 
    var $tabs = $('.menu .item').tab();
    $('.tab.segment').each(function(i){
        var tabsLen = $('.tab.segment').length - 1;
        if (i != tabsLen) {
            next = i + 2
            $(this).append("<div class='column float-right'><button type='submit' class='ui button' id='next-tab' rel='" + next + "' sel='" + i + "'>Next <i class='chevron circle right icon'></i></button></div>");
        }
        if (i != 0) {
            prev = i;
            $(this).append("<div class='column float-left'><button type='submit' class='ui button' id='prev-tab' rel='" + prev + "' sel='" + i + "'>Previous <i class='chevron circle right icon'></i></button></div>");
        }
    })

    $('#next-tab, #prev-tab').click(function() { 
        if($(this).attr("sel") == 0){
            $.ajax({
                url: '/enermod/api/getTableData?cols='+$('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val(),
                type: 'GET',
                success: function(response) {
                    handsOnInit(response)
                },
                error: function(error) {
                    console.log(error)
                }
            })
        }
        $tabs.tab('change tab', $(this).attr("rel"));
        return false;
    });
            
    //Drop Down effect
    $('.ui.dropdown').dropdown({
        onChange: function (value, text, $selectedItem) {
        // console.log(value);
        },
        forceSelection: false,
        selectOnKeydown: false,
        showOnFocus: false,
        on: "click"
    });


    //Form Validation
    // $('.ui.form')
    //         .form({
    //             fields: {
    //             selectedModel: 'empty',
    //             selectedVersion: 'empty',
    //             selectedSubModel: 'empty',
    //             selectedFunction: 'empty',
    //             selectedColumns: 'empty',
    //             }
    //         });
            
});