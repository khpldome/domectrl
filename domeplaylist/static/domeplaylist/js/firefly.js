jQuery(document).ready(function($) {

    $('.playlist-collapse').click(function() {
        $('.tracks-container').removeClass('expanded');
        $('.tracks-container').addClass('collapsed');
        $('.playlist-expand').removeClass('pressed');
        $(this).addClass('pressed');
        // console.log('collapse');
    });

    $('.playlist-expand').click(function() {
        $('.tracks-container').removeClass('collapsed');
        $('.tracks-container').addClass('expanded');
        $('.playlist-collapse').removeClass('pressed');
        $(this).addClass('pressed');
        // console.log('expand');
    });

    $('.track').click(function(){
        $('.track').removeClass('active');
        $(this).addClass('active');
        // console.log('active');
    });

    $('.playlists-item').click(function(){
        $('.playlists-item').removeClass('active');
        $(this).addClass('active');
        // console.log('active');
    });
    $('.icon-trash').click(function() {
        $(this).parent().parent().remove();
    });

    var trackCount = $('.playlist-current').data("trackCount");
    var playlistCount = $('.playlists-container').data("playlistCount");
    // console.log('trackCount:' + trackCount);
    // console.log('playlistCount:' + playlistCount);
    $('.track-container').css('grid-template-rows', 'repeat('+ trackCount +', 120px)');
    $('.playlists-container').css('grid-template-rows', '68px repeat(' + playlistCount + ', 50px)');

    // var trackCurrentTime = $('.bar-marker').css('left');
    // console.log('trackCurrentTime: ', trackCurrentTime);
    // $('.bar-current').css('width', 'calc(' + trackCurrentTime + ' + 10px)');

    $('.bar-marker').draggable({
        axis: 'x',
        containment: 'parent',
        drag: function() {
            var trackCurrentTime = $('.bar-marker').css('left');
            $('.bar-current').css('width', 'calc(' + trackCurrentTime + ' + 10px)');
        }
    });



});