
$(function(){
	$('.consultaForm').bind('submit',function(){
		var error = '' ;

		var nameField = $('.consultaForm [name|="name"]');
		var emailField = $('.consultaForm [name|="email"]');
		var telField = $('.consultaForm [name|="telephone"]');
		var consultaField = $('.consultaForm [name|="body"]');
		var captchaField = $('.consultaForm [name|="captcha_1"]');

		if ( nameField.val() == '' )
		{
			nameField.css('border','1px solid red');
			error +=  '<p>El nombre no puede estar vac&iacute;o</p>';
		}

		if ( telField.val() == '' )
		{
			telField.css('border','1px solid red');
			error +=  '<p>El tel&eacute;fono no puede estar vac&iacute;o</p>';
		}

		if ( emailField.val() == '' )
		{
			emailField.css('border','1px solid red');
			error += '<p>El e-mail no puede estar vac&iacute;o</p>';
		}else{
			if ( !echeck( emailField.val()) )
			{
				emailField.css('border','1px solid red');
				error += '<p>El email no es valido</p>'
			}
		}

		if ( consultaField.val() == '' )
		{
			consultaField.css('border','1px solid red');
			error += '<p>La consulta no puede estar vac&iacute;a</p>';
		}

		if ( captchaField.val() == '' ){
			captchaField.css('border','1px solid red');
			error += '<p>El campo de seguridad no puede estar vac&iacute;o</p>';
		}

		if (error == false ){
			return true;
		}else{
			$('.consultaForm').parent().parent().prepend('<div class="texts error">'+ error +'</div>');
			setTimeout('$(".error").hide("slow")',5000);
			return false;
		}
	});
})


function echeck(str) {

		var at="@"
		var dot="."
		var lat=str.indexOf(at)
		var lstr=str.length
		var ldot=str.indexOf(dot)
		if (str.indexOf(at)==-1){
		   return false
		}

		if (str.indexOf(at)==-1 || str.indexOf(at)==0 || str.indexOf(at)==lstr){
		   return false
		}

		if (str.indexOf(dot)==-1 || str.indexOf(dot)==0 || str.indexOf(dot)==lstr){
		    return false
		}

		 if (str.indexOf(at,(lat+1))!=-1){
		    return false
		 }

		 if (str.substring(lat-1,lat)==dot || str.substring(lat+1,lat+2)==dot){
		    return false
		 }

		 if (str.indexOf(dot,(lat+2))==-1){
		    return false
		 }
		
		 if (str.indexOf(" ")!=-1){
		    return false
		 }

 		 return true					
	}

