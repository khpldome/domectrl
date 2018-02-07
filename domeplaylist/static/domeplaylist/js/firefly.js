jQuery(document).ready(function($) {

    $('.playlist-collapse').click(function() {
        $('.tracks-container').addClass('collapsed');
        $('.playlist-expand').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $('.playlist-expand').click(function() {
        $('.tracks-container').removeClass('collapsed');
        $('.playlist-collapse').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $('.track').click(function(){
        $('.track').removeClass('active');
        $(this).addClass('active');
        $('.player').insertAfter($(this).find('.track-trash'));
        $('.player').css({'grid-column': '1/6', 'grid-row': '2/3'});
    });

    $('.playlists-item').click(function(){
        $('.playlists-item').removeClass('active');
        $(this).addClass('active');
    });

    $('.icon-trash').click(function() {
        $(this).parent().parent().remove();
    });

    var playlistCount = $('.playlists-container').data("playlistCount");
    $('.playlists-container').css('grid-template-rows', '68px repeat(' + playlistCount + ', 50px)');

    $('.bar-marker').draggable({
        axis: 'x',
        containment: 'parent',
        drag: function() {
            var trackCurrentTime = $('.bar-marker').css('left');
            $('.bar-current').css('width', 'calc(' + trackCurrentTime + ' + 10px)');
        }
    });

// Загузка плейлиста без перезагузки всей страницы
    //  $(".playlist-link").click(function(e){
    //     e.preventDefault(); //отключаем событие по умолчанию
    //     var target = $(this).attr("href"); //берем URL из ссылки на плейлист
    //     $(".tracks-container").load(target); //подгружаем содержимое в элемент с классом 'tracks-container'
    // });

        var origin = 'sortable';
        $(".tracks-container").droppable({
            drop: function (event, ui) {
                if (origin === 'draggable') {
                    console.log(ui.draggable);
                    origin = 'sortable';
                }
            }
        }).sortable({
            revert: true,
            handle: ".track-move",
            axis: "y",
            helper: "clone",
            forceHelperSize: true,
            opacity: 1,
            placeholder: "sortable-placeholder",
            forcePlaceholderSize: true
        });

        $(".playlists-container").droppable({
            drop: function (event, ui) {
                if (origin === 'draggable') {
                    console.log(ui.draggable);
                    origin = 'sortable';
                }
            }
        }).sortable({
            revert: true,
            handle: ".playlist-move",
            axis: "y",
            helper: "clone",
            forceHelperSize: true,
            opacity: 1,
            placeholder: "sortable-placeholder",
            forcePlaceholderSize: true
        });

});