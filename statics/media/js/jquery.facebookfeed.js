/**
Plugin Creado por ikhuerta.
Más info en http://blog.ikhuerta.com/plugin-jquery-para-incluir-el-muro-de-una-pagina-de-facebook-en-tu-web
*/
// funciones para manejar facebook graph api con jquery...
var pagegraph = {
  pageid : "116374171720257",
  getFromGraph : function (connectionType,callback) { $.getJSON("https://graph.facebook.com/"+pagegraph.pageid+"/"+connectionType+"?callback=?",function (fbData){callback(fbData.data);}); },
  getFeed : function(callback) {pagegraph.getFromGraph('feed',callback);},
  // you can add: getPhotos() , getEvents() , getVideos() ...
  getOwnFeed : function(callback) { // only the page messages in a feed
  	pagegraph.getFeed(function (feed) {
	  ownFeed = [];
	  for(var i=0;i<feed.length;i++) if (!feed[i].to) ownFeed.push(feed[i]);
	  callback(ownFeed); 
  });},
  help /*for debug, prints in html the json object*/ : function(el,elementName){
  	if (!elementName) elementName = "element";
  	var html = "<ul>";
  	$.each(el, function(i, val) {
  		i = (/[0-9]+/.test(i)) ? "["+i+"]" : "."+i;
  		if (typeof val === "object") html += "<li><strong>"+elementName+i+"</strong> " + pagegraph.viewElement(val,elementName+i) + "</li>";
  		else html += "<li><strong>"+elementName+i+"</strong> = \"" + val + "\"</li>";
	});
	html += "</ul>";
	return html; 
  },
  userImg : function (userId){return '<img class="user-photo user-'+userId+'" src="https://graph.facebook.com/'+userId+'/picture" />';},
  feedToHtml : function (feed){
	html = '<ul id="facebook-'+pagegraph.pageid+'" class="facebook">';
	$.each(feed, function(i, el) {
		html += '<li id="'+el.id+'" class="'+el.type+' from-'+el.from.id+'">';
		if (el.icon) html += '<img class="icon" src="'+el.icon+'" /> ';
		html += pagegraph.userImg(el.from.id) + '<strong class="author author-'+el.from.id+'">'+el.from.name+'</strong> ';
		if (el.message) html += '<span class="message">'+el.message+'</span>';
		if (el.picture || el.link || el.name || el.description)
		{
			html +='<div class="extra">';
			if (el.link && el.name)	html +='<h4 class="title facebook-link"><a href="'+el.link+'">'+el.name+'</a></h4>';
			else if (el.link) html +='<h4 class="title"><a href="'+el.link+'">'+el.link+'</a></h4>';
			else if (el.name) html +='<h4 class="title">'+el.name+'</h4>';
			if (el.link && el.picture) html += '<a class="image facebook-link" href="'+el.link+'"><img src="'+el.picture+'"/></a>';
			else if (el.picture) html += '<img src="'+el.picture+'"/>';
			if (el.description) html += '<span class="description">'+el.description+'</span>';
			html +='</div>';
		}
		if (el.likes && el.likes > 0) if (el.likes == 1) html += '<p class="likes">A una persona le gusta esto</p>'; else html += '<p class="likes">A '+el.likes+' personas les gusta esto</p>';
		if (el.source) html += '<p class="source"><a href="'+el.source+'">Descargar '+el.type+'</a></p>';
		if (el.comments)
		{
			html += '<p class="comment-count">'+el.comments.count+' comentario/s</p>';
			html += '<ul class="comments">';
			$.each(el.comments.data, function(i, c) {
				html += '<li>'+pagegraph.userImg(c.from.id)+'<strong class="author author-'+c.from.id+'">'+c.from.name+'</strong><span class="message">'+c.message+'</span></li>';
			});
			html += '</ul>';
		}
		html += '</li>';
	});
	html += '</ul>';
	return html;
  }
};

// declaracion de los dos plugins...
(function($){ 
  // Plugin para crear el feed de la pagina...  $(xxx).facebookFeed(facebookpageid);
  $.fn.facebookFeed = function( pageid ) {
  	  var pgid = pagegraph.pageid;
  	  if (pageid) pagegraph.pageid = pageid;
  	  var dom = $(this);
      pagegraph.getFeed(function (data){
		html = pagegraph.feedToHtml(data);
		dom.html(html);
		if (pageid) pagegraph.pageid = pgid;
	});
  };
  // Plugin para crear el feed de solo nuestras publicaciones en nuestra pagina. $(xxx).facebookOwnFeed(facebookpageid);
  $.fn.facebookOwnFeed = function( pageid ) {
  	  var pgid = pagegraph.pageid;
  	  if (pageid) pagegraph.pageid = pageid;
  	  var dom = $(this);
      pagegraph.getOwnFeed(function (data){
		html = pagegraph.feedToHtml(data);
		dom.html(html);
		if (pageid) pagegraph.pageid = pgid;
	});
  };
})(jQuery);

/* 
Codigo de ejemplo para añadirlo a tu página:

// 1) lanzamos el ready de jquery
$(document).ready(function(){
	
	// 2) dentro de este div metemos el feed...
	$("#facebook-feed-container").facebookFeed('idPaginaFacebook');
	
	// 3) dentro de este div metemos el feed pero con solo las publicaciones de nuestra propia página (y no las de los usuarios)
	$("#facebook-ownfeed-container").facebookOwnFeed('idPaginaFacebook');
	
});
*/