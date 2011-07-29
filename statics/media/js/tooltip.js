/*
 * Tooltip script
 * powered by jQuery (http://www.jquery.com)
 *
 * written by Alen Grakalic (http://cssglobe.com)
 *
 * for more info visit http://cssglobe.com/post/1695/easiest-tooltip-and-image-preview-using-jquery
 *
 */

this.tooltip = function(){
	/* CONFIG */
		xOffset = 8;
		yOffset = -25;
		// these 2 variable determine popup's distance from the cursor
		// you might want to adjust to get the right result
	/* END CONFIG */
	$("a.tooltip").hover(function(e){
		this.t = this.title;
		this.title = "";
		$("body").append("<p id='tooltip'><b>"+ this.t +"</b><span></span></p>");
		xTooltip = $("#tooltip").height() + xOffset;
		$("#tooltip")
			.css("top",(e.pageY - xTooltip) + "px")
			.css("left",(e.pageX + yOffset) + "px")
			.fadeIn("fast");
    },
	function(){
		this.title = this.t;
		$("#tooltip").remove();
    });
	$("a.tooltip").mousemove(function(e){
		var xTooltip = $("#tooltip").height() + xOffset;
		$("#tooltip")
			.css("top",(e.pageY - xTooltip) + "px")
			.css("left",(e.pageX + yOffset) + "px");
	});
};



// starting the script on page load
$(document).ready(function(){
	tooltip();
});