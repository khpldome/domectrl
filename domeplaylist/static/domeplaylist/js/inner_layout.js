// $(document).ready(function () {

// jQuery(document).ready(function($) {
    var moduleAPIUrl = window.location.host + '/ajax-status/state.json';

    console.log(moduleAPIUrl);

    $(function updateSystemState() {

        // console.log('ajax');
        $.ajax({
            // url: moduleAPIUrl,
            url: '/ajax-status/state.json',

            headers: {
                // 'Access-Control-Allow-Origin': '*'
                // 'Authorization': 'Basic OjYzOTMz'
            },

            // dataType: 'json',

            success: function (data, status, jqXHR) {
                $('.dynamic').empty();
                console.log(data);
                $('#currentTime').append(data['action']);
                console.log($('action', data).text());
                setTimeout(updateSystemState, 1000);
            },
            error: function (jqXHR, status, error) {
                console.log('error' + JSON.stringify(jqXHR));
                setTimeout(updateSystemState, 2000);
            }
        });
        // }

    });
// });




