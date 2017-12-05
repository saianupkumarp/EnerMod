
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
                var promised = $.ajax({
                    url: '/enermod/api/getTableData?cols='+$('#selectedColumns').dropdown('get value')[$('#selectedColumns').dropdown('get value').length -1]+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val()+'&user='+$('#selectedOwner').find(':selected').val()+'&version='+$('#selectedVersion').find(':selected').val()+'&country='+$('#selectedModelCountry').find(':selected').val(),
                    type: 'GET'
                });
                promised.done(function(response){
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
                        handsontable.addHook('beforeChange', beforeChange);
                        
                        var ch=true;
                        function beforeChange(changes, source) {
                            if (source == 'edit' || source == 'autofill') {
                                $.each(changes, function(index, element) {
                                console.log(changes);
                                    if (element[3]==null || element[3]<0){
                                        // alert("Please enter Value greater than or equals to Zero.");
                                        $('.mini.modal')
                                        .modal('show');
                                        ch= false;    
                                    }
                                    else
                                        ch= true; 
                                });
                                if (!ch)
                                    return false;
                            }
                        
                        }
                        if (ch)
                            {
                                handsontable.addHook('afterChange', afterChange);
                            }
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
                    }).fail(function(error) {
                        $('#loading').hide();
                        console.log(error)
                    });
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
                    var promised = $.ajax({
                        url: '/enermod/api/postToFact?editeddata='+JSON.stringify(handsontable.getData())+'&header='+JSON.stringify(tableHeader)+'&model='+$('#selectedModel').find(":selected").val()+'&sm='+$('#selectedSubModel').find(':selected').val()+'&fnname='+$('#selectedFunction').find(':selected').val()+'&mainversion='+$('#selectedVersion').find(':selected').val()+'&country='+$('#selectedModelCountry').find(':selected').val(),
                        type: 'GET'
                    });
                    promised.done(function(response){
                                $('#clipboard').empty();
                                document.getElementById('clipboard').innerHTML += response;
                                $('#loading').hide();
                                tabChange(tab_proceed_status=true, parseInt(num) + 2);
                    }).fail(function(error) {
                            $('#loading').hide();
                            console.log(error);
                    });
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

  
   //Selected Model Changed
   selectedModel.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistModelCountry?modelTypeID='+$('#selectedModel').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedModelCountry').dropdown('restore defaults');
                selectedModelCountry.length = 1; // remove all options bar first
                $('#selectedOwner').dropdown('restore defaults');
                selectedOwner.length = 1; // remove all options bar first
                $('#selectedVersion').dropdown('restore defaults');
                selectedVersion.length = 1; // remove all options bar first
                $('#selectedSubModel').dropdown('restore defaults');
                selectedSubModel.length = 1; // remove all options bar first
                $('#selectedFunction').dropdown('restore defaults');
                selectedFunction.length = 1; // remove all options bar first
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first

                var modelCountry=response['modelCountry'];
                //Load Country
                for (var i in modelCountry) {
                    selectedModelCountry.options[selectedModelCountry.options.length] = new Option(modelCountry[i]['cntryName'], modelCountry[i]['cntryid']);
                }
        });
    }
    //Selected Country Changed
    selectedModelCountry.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistUsers?modelTypeID='+$('#selectedModel').find(':selected').val()
                                            +'&modelCountry='+$('#selectedModelCountry').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedOwner').dropdown('restore defaults');
                selectedOwner.length = 1; // remove all options bar first
                $('#selectedVersion').dropdown('restore defaults');
                selectedVersion.length = 1; // remove all options bar first
                $('#selectedSubModel').dropdown('restore defaults');
                selectedSubModel.length = 1; // remove all options bar first
                $('#selectedFunction').dropdown('restore defaults');
                selectedFunction.length = 1; // remove all options bar first
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first

                var users=response['users'];
                //Load Users
                for (var i in users) {
                    var name= null;
                    if (users[i]['dname'].includes(","))
                        name=users[i]['fname'] +" "+users[i]['lname'];
                    else 
                        name=users[i]['dname'];

                    selectedOwner.options[selectedOwner.options.length] = new Option(name, users[i]['username']);
                }
                setTimeout(function () {
                    $('#selectedOwner').dropdown('set selected', $('#user').val());
                }, 1);
        });
    }
    //Selected User Changed
    selectedOwner.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistmainversion?modelTypeID='+$('#selectedModel').find(':selected').val()
                                            +'&modelCountry='+$('#selectedModelCountry').find(':selected').val()
                                            +'&owner='+$('#selectedOwner').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedVersion').dropdown('restore defaults');
                selectedVersion.length = 1; // remove all options bar first
                $('#selectedSubModel').dropdown('restore defaults');
                selectedSubModel.length = 1; // remove all options bar first
                $('#selectedFunction').dropdown('restore defaults');
                selectedFunction.length = 1; // remove all options bar first
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first

                var mainVersion=response['mainversion'];
                //Load Versions
                for (var i in mainVersion.reverse()) {
                    selectedVersion.options[selectedVersion.options.length] = new Option(mainVersion[i]['version'], mainVersion[i]['version']);
                }
        });
    }
    //Selected Version Changed
    selectedVersion.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistsubmodel?modelTypeID='+$('#selectedModel').find(':selected').val()
                                            +'&modelCountry='+$('#selectedModelCountry').find(':selected').val()
                                            +'&owner='+$('#selectedOwner').find(':selected').val()
                                            +'&version='+$('#selectedVersion').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedSubModel').dropdown('restore defaults');
                selectedSubModel.length = 1; // remove all options bar first
                $('#selectedFunction').dropdown('restore defaults');
                selectedFunction.length = 1; // remove all options bar first
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first
            
                var subModel=response['submodel'];
                //Load Sub models
                for (var i in subModel) {
                    selectedSubModel.options[selectedSubModel.options.length] = new Option(subModel[i]['submodelName'], subModel[i]['submodelid']);
                }
        });
    }
    //Selected SubModel Changed
    selectedSubModel.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistfunc?modelTypeID='+$('#selectedModel').find(':selected').val()
                                            +'&modelCountry='+$('#selectedModelCountry').find(':selected').val()
                                            +'&owner='+$('#selectedOwner').find(':selected').val()
                                            +'&version='+$('#selectedVersion').find(':selected').val()
                                            +'&subModel='+$('#selectedSubModel').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedFunction').dropdown('restore defaults');
                selectedFunction.length = 1; // remove all options bar first
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first
            
                var func=response['func'];
                //Load Functions
                for (var i in func) {
                    selectedFunction.options[selectedFunction.options.length] = new Option(func[i]['funcName'], func[i]['funcid']);
                }
        });
    }
    //Selected Function Changed
    selectedFunction.onchange = function () {
        var promised = $.ajax({
            url:  '/enermod/api/getdistcolumns?modelTypeID='+$('#selectedModel').find(':selected').val()
                                            +'&modelCountry='+$('#selectedModelCountry').find(':selected').val()
                                            +'&owner='+$('#selectedOwner').find(':selected').val()
                                            +'&version='+$('#selectedVersion').find(':selected').val()
                                            +'&subModel='+$('#selectedSubModel').find(':selected').val()
                                            +'&func='+$('#selectedFunction').find(':selected').val(),
            type:  'GET'
        });
        promised.done(function(response){
                //Clear 
                $('#selectedColumns').dropdown('restore defaults');
                selectedColumns.length = 1; // remove all options bar first
                
                var cols=JSON.parse(response['columns']);
                console.log(response['columns']);
                console.log(JSON.parse(response['columns']));
                var selected=[];
                //Load Columns
                for (var i in cols) {
                    selectedColumns.options[selectedColumns.options.length] = new Option(cols[i]['colName'], cols[i]['colID']);
                    selected[i]=cols[i]['colID'];
                }
                setTimeout(function () {
                    $('#selectedColumns').dropdown('set selected', selected);
                }, 1);
        });
    }

});