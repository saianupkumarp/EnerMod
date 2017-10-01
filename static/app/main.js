
$(function() {
    $('#loading').hide();
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
            $(this).append("<div class='column float-right'><button type='submit' class='ui button' id='insert-tab' rel='" + next + "' sel='" + i + "'><i class='cloud upload icon'></i> Insert</button></div>");
        }
        if (i != 0 && i != 2) {
            prev = i;
            $(this).append("<div class='column float-left'><button type='submit' class='ui button' id='prev-tab' rel='" + prev + "' sel='" + i + "'><i class='chevron circle left icon'></i> Previous</button></div>");
        }
    })

    $('#next-tab, #insert-tab').click(function() {
        var tab_proceed_status;
        if($(this).attr("sel") == 0){
            var cols = $('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]
            var model = $('#selectedModel').find(':selected').val()
            var sm = $('#selectedSubModel').find(':selected').val()
            var fnname = $('#selectedFunction').find(':selected').val()
            if(validate(cols, model, sm, fnname)){
                $('#loading').show();
                $.ajax({
                    url: '/enermod/api/getTableData?cols='+$('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val()+'&user='+$('#selectedOwner').find(':selected').val(),
                    type: 'GET',
                    success: function(response) {
                        var dataCopy = jQuery.extend(true, {}, response.result);
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
                        handsontable.addHook('afterChange', afterChange);
                        function afterChange(changes, source) {
                         if (source == 'edit' || source == 'autofill') {
                          $.each(changes, function(index, element) {
                              var rowIndex = element[0];
                              var columnIndex = element[1];        
                              var oldValue = element[2];
                              var newValue = element[3];
                              var cellChange = {
                                  'rowIndex': rowIndex,
                                  'columnIndex': columnIndex
                              }; 
                              if (oldValue != newValue) {
                                  var cellProperties = handsontable.getCellMeta(rowIndex, handsontable.propToCol(columnIndex));
                                  if (newValue != dataCopy[rowIndex][columnIndex]) {
                                      cellProperties.renderer = function(instance, td, row ,col, prop, value, cellProperties) {
                                        Handsontable.renderers.TextRenderer.apply(this, arguments);
                                        td.style.backgroundColor = '#FFA500';
                                      };
                                  }
                                  else {
                                      cellProperties.renderer = function(instance, td, row ,col, prop, value, cellProperties) {
                                        Handsontable.renderers.TextRenderer.apply(this, arguments);
                                        td.style.backgroundColor = 'white';
                                      };;
                                  }
                                  handsontable.render();
                              }
                          });
                         }
                        }
                        $('#loading').hide();
                    },
                    error: function(error) {
                        $('#loading').hide();
                        console.log(error)
                    }
                })
                tabChange(tab_proceed_status=true, parseInt($(this).attr("sel")) + 2);
            }
            else
                return;
        }
        if($(this).attr("sel") == 1) {
            var num = $(this).attr("sel")
            $('.ui.basic.modal').modal({
                closable  : true,
                onDeny: function(){
                    return;
                },
                onApprove : function() {
                    $('#loading').show();
                    $.ajax({
                        url: '/enermod/api/postToFact?editeddata='+JSON.stringify(handsontable.getData())+'&header='+JSON.stringify(tableHeader)+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val()+'&mainversion='+$('#selectedVersion').find(':selected').val(),
                        type: 'GET',
                        success: function(response) {
                                $('#clipboard').empty();
                                document.getElementById('clipboard').innerHTML += response;
                        },
                        error: function(error){
                            $('#loading').hide();
                            console.log(error);
                        }
                    })
                    setTimeout(function(){
                        $('#loading').hide();
                        tabChange(tab_proceed_status=true, parseInt(num) + 2);
                    }, 5000);
                    return;
                }
              }).modal('show');
        }
    });

    $('#prev-tab').click(function() {
        $tabs.tab('change tab', $(this).attr("rel"));
        return false;
    })

    function tabChange(status, tabnum) {
        if (status) {
            $tabs.tab('change tab', tabnum);
            return false;   
        }   
    }    

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