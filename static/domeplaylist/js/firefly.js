jQuery(document).ready(function($) {

    $('.playlist-collapse').click(function() {
        $('.playlist-items-container').removeClass('expanded');
        $('.playlist-items-container').addClass('collapsed');
        $('.playlist-expand-button-bg').removeClass('pressed');
        $(this).next('.playlist-collapse-button-bg').addClass('pressed');
        console.log('collapse');
    });

    $('.playlist-expand').click(function() {
        $('.playlist-items-container').removeClass('collapsed');
        $('.playlist-items-container').addClass('expanded');
        $('.playlist-collapse-button-bg').removeClass('pressed');
        $(this).next('.playlist-expand-button-bg').addClass('pressed');
        console.log('expand');
    });

    $('.playlist-item').click(function(){
        $('.playlist-item').removeClass('active');
        $(this).addClass('active');
        console.log('active');
    });

    $('.icon-trash').click(function() {
        $(this).parent().parent().remove();
    });

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