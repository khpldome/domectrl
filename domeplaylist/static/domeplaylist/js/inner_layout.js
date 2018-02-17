function updateSystemState() {

    $.ajax({
        url: 'ajax-status',
        // url: VLC_api_url,
        // crossDomain: true,
        headers: {
                    // 'Access-Control-Allow-Origin': '*'
                    // 'Authorization': 'Basic OjYzOTMz'
                },
        //     dataType: 'jsonp text xmls',
        success: function (data, status, jqXHR) {
            $('#data1').append(format_time($('action', data).text()));
            setTimeout(updateSystemState, 1000);
        },
        error: function (jqXHR, status, error) {
            setTimeout(updateSystemState, 500);
        }
    });
}

