jQuery(document).ready(function($) {

    $('.playlist-collapse').click(function() {
        $('.tracks-container').addClass('collapsed');
        $('.playlist-expand').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $(document).keyup(function(e) {
        if (e.keyCode === 27) {
            $('#myModal').hide();
        };
    });

        var browse_target       =   'default';
        $(function(){
            $('#window_browse').dialog({
                autoOpen: false,
                width: 50,
                height: 650,
                modal: true,
                resizable: false,
                buttons: {
                    "Открыть":function(){
                        $('li.ui-selected','#browse_elements').each(function(){
                            $(this).dblclick();
                        });
                    },
                    "Enqueue": function() {
                        $('li.ui-selected','#browse_elements').each(function(){
                            var path    =   this.getAttribute('opendir') ? this.getAttribute('opendir') : this.getAttribute('openfile');
                            switch(browse_target){
                                default:
                                    sendCommand('command=in_enqueue&input='+encodeURI(path));
                                    setTimeout(function(){updatePlayList(true);},1000);
                                    break;
                            }
                        });
                        $(this).dialog("close");
                    },
                    "Отмена" : function(){
                        $(this).dialog("close")
                    }
                }
            });
        });

    $('.playlist-expand').click(function() {
        $('.tracks-container').removeClass('collapsed');
        $('.playlist-collapse').removeClass('pressed');
        $(this).addClass('pressed');
    });

    $('.track').click(function() {
        $('.track').removeClass('active');
        $(this).addClass('active');
        $('.player').insertAfter($(this).find('.track-trash'));
        $('.player').css({'grid-column': '1/6', 'grid-row': '2/3'});
    });
    // console.log($('.track.active').length);
    if ($(".track.active").length) {
        $(window).load(function () {
            $('.player').insertAfter( $(".track.active").find('.track-trash'));
            $('.player').css({'grid-column': '1/6', 'grid-row': '2/3'});
        });
    }

    $('.projectors-turn-off a').click(function(){
        $(this).parent().addClass("hidden")
        $('.projectors-turn-on').removeClass('hidden');
    });

    $('.projectors-turn-on a').click(function(){
        $(this).parent().addClass("hidden")
        $('.projectors-turn-off').removeClass('hidden');
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