function handsOnInit(dataObject){
    yellowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.backgroundColor = '#FCF3CF';
    };
    var handsontableElement = document.querySelector('#handsontable');
    var handsontableElementContainer = handsontableElement.parentNode;
    var handsontableSettings = {
                data: dataObject.result,
                stretchH: 'all',
                width: '100%',
                height: 500,
                rowHeaders: true,
                colHeaders: dataObject.colHeaders,
                columns: dataObject.handsOnColumns,
                customBorders: [
                    {col: 3, left: {width: 2, color: 'red'},
                    right: {width: 1, color: 'green'}, top: '', bottom: ''}
                ]
    };
    var handsontable = new Handsontable(handsontableElement, handsontableSettings);
}