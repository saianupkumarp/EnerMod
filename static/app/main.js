
$(function() {


    //Page Tabs 
			$('.menu .item')
            .tab();
            
    //Drop Down effect
    $('.ui.dropdown').dropdown({
        onChange: function (value, text, $selectedItem) {
        console.log(value);
        },
        forceSelection: false,
        selectOnKeydown: false,
        showOnFocus: false,
        on: "click"
    });


    //Form Validation
    $('.ui.form')
			.form({
				fields: {
				selectedModel: 'empty',
				selectedVersion: 'empty',
				selectedSubModel: 'empty',
				selectedFunction: 'empty',
				selectedColumns: 'empty',
				}
			});
            
});