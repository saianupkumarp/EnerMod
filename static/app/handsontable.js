
var dataObject = [
        {id: 1, year: 't1', fuelType: 'Arab Light', season: 'Winter', value: 10.5},
        {id: 2, year: 't2', fuelType: 'HFO', season: 'Summer', value:25 },
        {id: 3, year: 't3', fuelType: 'Nuclwar', season: 'Winter', value: 222}
        ];

yellowRenderer = function(instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.backgroundColor = '#FCF3CF';
};
var handsontableElement = document.querySelector('#handsontable');
var handsontableElementContainer = handsontableElement.parentNode;
var handsontableSettings = {
            data: dataObject,
            stretchH: 'all',
            width: '100%',
            autoWrapRow: true,
            height: 321,
            // maxRows: 22,
            rowHeaders: true,
            colHeaders: [
                    'ID',
                    'Year',
                    'Fuel Type',
                    'Season',
                    'Value'
            ],
            columns: [
                    {
                        data: 'id',
                        type: 'numeric',
                        width: 40,
                        editor: false
                    },
                    {
                        data: 'year',
                        type: 'text',
                        editor: false
                    },
                    {
                        data: 'fuelType',
                        type: 'text',
                        editor: false

                    },
                    {
                        data: 'season',
                        type: 'text',
                        editor: false
                    },
                    {
                        data: 'value',
                        type: 'numeric',
                        format: '0.00',
                        renderer: yellowRenderer
                    }
            ],
    customBorders: [
    {col: 3, left: {width: 2, color: 'red'},
    right: {width: 1, color: 'green'}, top: '', bottom: ''}
    ]
};

var handsontable = new Handsontable(handsontableElement, handsontableSettings);