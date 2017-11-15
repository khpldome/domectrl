function pageFormSubmit() {
    var $imageClearID = $('#image-clear_id');
    if (
        $imageClearID.length > 0 &&
        $('#initial-img').length == 0 &&
        $('input#id_image').val() == ''
    ) {
        $imageClearID.prop('checked', true);
    }
    return true;
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

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// responsiveVoice.setDefaultVoice("US English Male");
