
    var moduleAPIUrl = window.location.host + '/ajax-status/state.json';
    // var vlc_proc = false;

    console.log(moduleAPIUrl);

    $(function updateSystemState() {

        $.ajax({
            url: '/ajax-status/state.json',

            success:
                function (data, status, jqXHR)
                {
                    // console.log(data);
                    $('.dynamic_state').empty();
                    $('#request_ts').append(data['request_ts']);
                    $('#vlc_ts').append(data['vlc_ts']);
                    $('#vlc_proc').append(data['vlc_proc']);
                    $('#vlc_server').append(data['vlc_server']);
                    // $('#dpro_ts').append(data['dpro_ts']);
                    $('#dpro_proc').append(data['dpro_proc']);
                    // $('#dpro_desktop').append(data['dpro_desktop'].toString());
                    // $('#dpro_window').append(data['dpro_window'].toString());
                    $('#mosaic_ts').append(data['mosaic_ts']);
                    $('#mosaic').append(data['mosaic']);
                    // $('#pojectors_ts').append(data['pojectors_ts']);
                    // $('#pojectors').append(String(data['pojectors']));

                    var vlc_proc = data['vlc_proc'];
                    var vlc_server = data['vlc_server'];
                    var dpro_proc = data['dpro_proc'];
                    var mosaic = data['mosaic'];
                    // var icon_status = document.getElementById("icon-status");
                    // var status_player = document.getElementById("status-player");

                    var dpro_state = document.getElementById("dpro-state");
                    var status_calib = document.getElementById("status-calib");
                    // $('.status-calib').addClass('disabled')
                    var mosaic_state = document.getElementById("mosaic-state");
                    var status_mosaic = document.getElementById("status-mosaic");
                    
                    var status_player = $('.status-player');
                    if (vlc_proc) {
                        status_player.removeClass('disabled');
                        if (!vlc_server) {
                            status_player.addClass('unknown');
                        }
                    } else {
                        status_player.not('.disabled').addClass('disabled');
                        status_player.removeClass('unknown');
                    }

                    var status_calib = $('.status-calib');
                    if(dpro_proc){
                        status_calib.removeClass('disabled');
                    }
                    else{
                        status_calib.not('disabled').addClass('disabled')
                    }

                    var status_mosaic = $('.status-mosaic');
                    switch (mosaic) {
                        case 0:
                            status_mosaic.removeClass('disabled');
                            break;
                        case -1:
                            status_mosaic.not('.disabled').addClass('disabled');
                            status_mosaic.removeClass('unknown');
                            break;
                        case -2:
                            status_mosaic.not('.unknown').addClass('unknown');
                            status_mosaic.removeClass('disabled');
                            break;
                        default:
                            break;
                    }

                    // var status_mosaic = $('.mosaic');
                    // if(mosaic ){
                    //     status_mosaic.removeClass('disabled');
                    // }
                    // else{
                    //     status_mosaic.not('disabled').addClass('disabled')
                    // }

                    setTimeout(updateSystemState, 1000);
                },
            error:
                function (jqXHR, status, error)
                {
                    // console.log('error' + JSON.stringify(jqXHR));
                    setTimeout(updateSystemState, 1000);
                }
        });
    });


jQuery(document).ready(function($) {

    $('.account_tab-link a').click(function(e) {
        e.preventDefault();
        var divId = $(this).attr('href');
        console.log('divId: ' + divId);
        $('.account_tab-link').removeClass('active');
        $(this).parent().addClass('active');
        $('.account-tab').removeClass('active');
        $(divId).addClass('active');

    });

});