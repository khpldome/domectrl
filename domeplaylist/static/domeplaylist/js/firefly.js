jQuery(document).ready(function($) {

    $('.playlist-collapse').on('click', function(e) {
        e.preventDefault();
        $('.tracks-container').addClass('collapsed');
        $('.playlist-expand').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $('.playlist-expand').on('click', function(e) {
        e.preventDefault();
        $('.tracks-container').removeClass('collapsed');
        $('.playlist-collapse').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $(document).keyup(function(e) {
        if (e.keyCode === 27) {
            $('#myModal').hide();
        };
    });

    $('.track-click-container').click(function() {
        $('.track').removeClass('active');
        $(this).parent('.track').addClass('active');
        var trackName = $(this).parent('.track').find('.track-title h3').html();
        $('footer marquee span').html('Сейчас играет ' + trackName);
        $('.played-track-name').find('span').html('Сейчас играет ' + trackName);
        $('.player').addClass('active');
        $('.playlist-current').addClass('active');
        $
        // $('.player').insertAfter($(this).find('.track-trash'));
        // $('.player').css({'grid-column': '1/6', 'grid-row': '2/3'});
    });
    // console.log($('.track.active').length);
    if ($('.track.active').length) {
        $('.player').addClass('active');
    }

    $('.track-click-container').on('mouseenter', function() {

    });

    $('.projectors-turn-off a').on('click', function(e) {
        $(this).parent().addClass("hidden")
        $('.projectors-turn-on').removeClass('hidden');
    });

    $('.projectors-turn-on a').on('click', function(e) {
        $(this).parent().addClass("hidden")
        $('.projectors-turn-off').removeClass('hidden');
    });

    $('.playlists-item').on('click', function() {
        $('.playlists-item').removeClass('active');
        $(this).addClass('active');
    });

    $('.icon-trash').on('click', function() {
        $(this).parent().parent().remove();
    });

    var playlistCount = $('.playlists-container').data("playlistCount");
    $('.playlists-container').css('grid-template-rows', '68px repeat(' + playlistCount + ', 50px)');

    if ( $('.page-playlists').length == 1 ) {
        $('.page-link-more').removeClass('page-link-active');
        $('.page-link-playlists').addClass('page-link-active');
    };

    if ( $('.page-more').length == 1 ) {
        $('.page-link-playlists').removeClass('page-link-active');
        $('.page-link-more').addClass('page-link-active');
    };

    $('.tab-link').on('click', function(e) {
        e.preventDefault();
        $('.tab-link').removeClass('active');
        $(this).addClass('active');
        // var target ='\'$(' + $(this).find('a').attr('href') + '\')';
        var tabTarget = $(this).find('a').attr('href');
        var tabTitle = $(this).find('a').attr('title');
        $('.tab').css('display','none');
        $('.tab-content .title h2').html(tabTitle);
        $(tabTarget).css('display','block');
    });

    var tabsCount = $('.tab-link').length;
    $('.more-tabs-list').css('grid-template-rows', '68px repeat(' + tabsCount + ', 50px)');


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
        forcePlaceholderSize: true,
        update: function (event, ui) {
            console.log('drop');

            var trackOrder = {};
            var $trackList = $('#track-list');
            if ($trackList.length) {
                $trackList.find('.track').each(function (i, item) {
                    trackOrder[$(item).data('trackNum')] = i + 1;
                });
            }
            console.log(trackOrder);
            saveTrackOrder(trackOrder);
        }
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
        forcePlaceholderSize: true,
        update: function (event, ui) {
            console.log('drop playlist');

            var playlistOrder = {};
            var plList = $('#play-list');
            if (plList.length) {
                plList.find('.playlist').each(function (i, item) {
                    playlistOrder[$(item).data('playlistNum')] = i + 1;
                });
            }
            console.log(playlistOrder);
            savePlaylistOrder(playlistOrder);
        }
    });

});

    function savePlaylistOrder(data) {
        $.ajax({
            method: 'post',
            url: '/ajax-order/',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: {
                order: JSON.stringify(data),
                action: 'change_playlist_order'
            }
        }).done(function (response) {
            // console.log('order saved');
        }).fail(function (response) {
            // console.log('save order failed');
        });
    }

    function saveTrackOrder(data) {
        $.ajax({
            method: 'post',
            url: '/ajax-order/',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: {
                order: JSON.stringify(data),
                action: 'change_track_order'
            }
        }).done(function (response) {
            // console.log('order saved');
        }).fail(function (response) {
            // console.log('save order failed');
        });
    }

    function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}