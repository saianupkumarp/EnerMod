
$(function() {
    //Page Tabs 
    var $tabs = $('.menu .item').tab();
    var handsontable
    var tableHeader
    $('.tab.segment').each(function(i){
        var tabsLen = $('.tab.segment').length - 1;
        if (i == 0) {
            next = i + 2
            $(this).append("<div class='column float-right'><button type='submit' class='ui button' id='next-tab' rel='" + next + "' sel='" + i + "'>Next <i class='chevron circle right icon'></i></button></div>");
        }
        if (i == 1) {
            next = i + 2
            $(this).append("<div class='column float-right'><button type='submit' class='ui button' id='next-tab' rel='" + next + "' sel='" + i + "'><i class='cloud upload icon'></i> Insert</button></div>");
        }
        if (i != 0) {
            prev = i;
            $(this).append("<div class='column float-left'><button type='submit' class='ui button' id='prev-tab' rel='" + prev + "' sel='" + i + "'><i class='chevron circle left icon'></i> Previous</button></div>");
        }
    })

    $('#next-tab, #prev-tab').click(function() { 
        if($(this).attr("sel") == 0){
            var cols = $('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]
            var model = $('#selectedModel').find(':selected').val()
            var sm = $('#selectedSubModel').find(':selected').val()
            var fnname = $('#selectedFunction').find(':selected').val()
            if(validate(cols, model, sm, fnname)){
                $.ajax({
                    url: '/enermod/api/getTableData?cols='+$('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val(),
                    type: 'GET',
                    success: function(response) {
                        tableHeader = response.colHeaders
                        var handsontableElement = document.querySelector('#handsontable');
                        var handsontableElementContainer = handsontableElement.parentNode;
                        var handsontableSettings = {
                                    data: response.result,
                                    stretchH: 'all',
                                    width: '100%',
                                    height: 500,
                                    rowHeaders: true,
                                    colHeaders: response.colHeaders,
                                    columns: response.handsOnColumns,
                                    customBorders: [
                                        {col: 3, left: {width: 2, color: 'red'},
                                        right: {width: 1, color: 'green'}, top: '', bottom: ''}
                                    ]
                        };
                        handsontable = new Handsontable(handsontableElement, handsontableSettings);
                    },
                    error: function(error) {
                        console.log(error)
                    }
                })
            }
            else
                return;
        }
        if($(this).attr("sel") == 1) {
            var approved=false;
            //Popup Window
            $('.ui.basic.modal')
            .modal({
                onDeny: function(){
                    approved=false;
                },
                onApprove : function() {
                    approved=true;
                }
              })
            .modal('show');
            if (approved){
                $.ajax({
                    url: '/enermod/api/postToFact?editeddata='+JSON.stringify(handsontable.getData())+'&header='+JSON.stringify(tableHeader)+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val()+'&mainversion='+$('#selectedVersion').find(':selected').val(),
                    type: 'GET',
                    success: function(response) {
                        console.log(response)
                    }
                })
                console.log($('#selectedFunction').find(':selected').val())
                console.log(handsontable.getData())
                console.log(tableHeader)
            }
            else
                return;
            
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

    

});