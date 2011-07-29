$(document).ready(function(){

    $('td.image img').each(function(c){ 
        _a = $('td.image a').eq(c).text('');
        $(this).wrap(_a);
        _a.remove()
        })
    $('td.image a').lightBox({
         'imageLoading': '/media/img/lightbox-ico-loading.gif',
         'imageBtnClose': '/media/img/lightbox-btn-close.gif',
         'imageBtnPrev': '/media/img/lightbox-btn-prev.gif',
         'imageBtnNext': '/media/img/lightbox-btn-next.gif',
         'imageBlank': '/meida/img/lightbox-blank.gif'
         });
 });
