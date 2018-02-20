
    var moduleAPIUrl = window.location.host + '/ajax-status/state.json';
    // var vlc_proc = false;

    console.log(moduleAPIUrl);

    $(function updateSystemState() {

        $.ajax({
            url: '/ajax-status/state.json',

            success:
                function (data, status, jqXHR)
                {
                    console.log(data);
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
                    
                    var sPlayer = $('.status-player');
                    if (vlc_proc) {
                        sPlayer.removeClass('disabled');
                        if (!vlc_server) {
                            sPlayer.addClass('unknown');
                        }
                    } else {
                        sPlayer.not('.disabled').addClass('disabled');
                    }

                    // if(vlc_proc){
                    //     icon_status.className = "icon-status-on"
                    //     if(vlc_server) {status_player.className = "status-player"}
                    //     else{status_player.className = "status-player unknown"}
                    // }
                    // else{
                    //     icon_status.className = "icon-status-off";
                    //     status_player.className = "status-player disabled"
                    // }

                    if(dpro_proc){
                        dpro_state.className = "icon-status-on";
                        status_calib.className = "status-calib"
                    }
                    else{
                        dpro_state.className = "icon-status-off";
                        status_calib.className = "status-calib disabled"
                    }

                    if(mosaic){
                        mosaic_state.className = "icon-status-on";
                        status_mosaic.className = "status-mosaic"
                    }
                    else{
                        mosaic_state.className = "icon-status-off";
                        status_mosaic.className = "status-mosaic disabled"
                    }

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