
    var moduleAPIUrl = window.location.host + '/ajax-status/state.json';

    console.log(moduleAPIUrl);

    $(function updateSystemState() {

        $.ajax({
            url: '/ajax-status/state.json',

            success: function (data, status, jqXHR) {
                console.log(data);
                $('.dynamic').empty();
                $('#vlc_ts').append(data['vlc_ts']);
                $('#vlc_proccess').append(data['vlc_proccess']);
                $('#vlc_server').append(data['vlc_server']);
                $('#request_ts').append(data['request_ts']);
                $('#dpro_ts').append(data['dpro_ts']);
                $('#dpro_process').append(data['dpro_process']);
                $('#dpro_desktop').append(data['dpro_desktop']);
                $('#dpro_window').append(data['dpro_window']);
                $('#mosaic_ts').append(data['mosaic_ts']);
                $('#mosaic').append(data['mosaic']);
                $('#pojectors_ts').append(data['pojectors_ts']);
                $('#pojectors').append(data['pojectors']);
                setTimeout(updateSystemState, 1000);
            },
            error: function (jqXHR, status, error) {
                // console.log('error' + JSON.stringify(jqXHR));
                setTimeout(updateSystemState, 1000);
            }
        });
    });





