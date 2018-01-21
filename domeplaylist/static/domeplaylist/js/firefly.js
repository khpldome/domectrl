jQuery(document).ready(function($) {

    $('.playlist-collapse').click(function() {
        $('.playlist-items-container').removeClass('expanded');
        $('.playlist-items-container').addClass('collapsed');
        $('.playlist-expand').removeClass('pressed');
        $(this).addClass('pressed');
        console.log('collapse');
    });

    $('.playlist-expand').click(function() {
        $('.playlist-items-container').removeClass('collapsed');
        $('.playlist-items-container').addClass('expanded');
        $('.playlist-collapse').removeClass('pressed');
        $(this).addClass('pressed');
        console.log('expand');
    });

    $('.playlist-item').click(function(){
        $('.playlist-item').removeClass('active');
        $(this).addClass('active');
        console.log('active');
    });

    $('.playlists-item').click(function(){
        $('.playlists-item').removeClass('active');
        $(this).addClass('active');
        console.log('active');
    });
    $('.icon-trash').click(function() {
        $(this).parent().parent().remove();
    });

    var playitemCount = $('.playlist-current').data("playitemCount");
    var playlistCount = $('.sidebar-playlists').data("playlistCount");
    console.log('playitemCount:'+playitemCount);
    console.log('playlistCount:'+playlistCount);
    $('.playlist-items-container').css('grid-template-rows', 'repeat('+playitemCount+', 120px)');
    $('.sidebar-playlists').css('grid-template-rows', '68px repeat('+playlistCount+', 50px)');

    // $('.icon-player-pause').click(function(){
    //     $(this).removeClass('.icon-player-pause');
    //     $(this).addClass('.icon-player-play');
    // });

    // $('.link-playlists').click(function() {
    //     $('.tab-more').css('display', 'none');
    //     $('.tab-playlists').css('display', 'block');
    //     $('.tab-link').removeClass('tab-link-active');
    //     $(this).addClass('tab-link-active');
    // });

    // $('.link-more').click(function() {
    //     $('.tab-playlists').css('display', 'none');
    //     $('.tab-more').css('display', 'block');
    //     $('.tab-link').removeClass('tab-link-active');
    //     $(this).addClass('tab-link-active');
    // });

});