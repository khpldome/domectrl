
    var moduleAPIUrl = window.location.host + '/ajax-status/state.json';

    console.log(moduleAPIUrl);

    $(function updateSystemState() {

        $.ajax({
            url: '/ajax-status/state.json',

            success: function (data, status, jqXHR) {
                console.log(data);
                $('.dynamic_state').empty();
                $('#vlc_ts').append(data['vlc_ts']);
                $('#vlc_proccess').append(data['vlc_proccess'].toString());
                $('#vlc_server').append(data['vlc_server'].toString());
                $('#request_ts').append(data['request_ts']);
                $('#dpro_ts').append(data['dpro_ts']);
                $('#dpro_process').append(data['dpro_process'].toString());
                $('#dpro_desktop').append(data['dpro_desktop'].toString());
                $('#dpro_window').append(data['dpro_window'].toString());
                $('#mosaic_ts').append(data['mosaic_ts']);
                $('#mosaic').append(data['mosaic'].toString());
                $('#pojectors_ts').append(data['pojectors_ts']);
                $('#pojectors').append(String(data['pojectors']));
                setTimeout(updateSystemState, 1000);
            },
            error: function (jqXHR, status, error) {
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