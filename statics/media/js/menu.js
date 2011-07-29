$(function(){ 
	$("#botonera li a").hover(
		function(){$(this).text($(this).attr('alt'))},
		function(){$(this).text($(this).attr('title'))}
	);
})
