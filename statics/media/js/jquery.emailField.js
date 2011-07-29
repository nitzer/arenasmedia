var DJSUBSCRIBE_DEFAULT_VALUE = 'Escriba su E-Mail';

$(window).bind("load", function() {
	$('.djsubscribeFormEmail').val(DJSUBSCRIBE_DEFAULT_VALUE);
	$('.djsubscribeFormEmail')
		.focusin(function(){
			if( !$(this).val() | $(this).val()==DJSUBSCRIBE_DEFAULT_VALUE )
			{
				$(this).val('')
			}
		}
		).focusout(function(){
			if( !$(this).val() )
			{
				$(this).val(DJSUBSCRIBE_DEFAULT_VALUE)
			}
		});
});
