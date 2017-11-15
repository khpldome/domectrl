$(document).ready(function () {

    // instance, using default configuration.
    CKEDITOR.replace('id_description',
        {
            extraPlugins: 'responsivevoice',
            toolbar: [
                ['Bold', 'Italic', 'Underline', 'Strikethrough', 'Subscript', 'Superscript',
                    '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', '-', 'About', '-'],
                ['ResponsiveVoice']
            ]
        });

    var $monetize = $('#monetize');
    $(function () {
        $monetize.find('#id_price[name="price"]').on('input', function () {

            var cur_price = Number(this.value);
            var set_revenue = (cur_price / 2).toFixed(2);

            console.log('cur_price= ' + cur_price + " | " + set_revenue);
            $monetize.find('#id_revenue_share[name="revenue_share"]').val(set_revenue);
        });
    });


    var were_changes = false;

    $monetize.find('#id_price[name="price"]').on('input', function () {
        console.log('price changed= ');
        were_changes = true
    });

    $(window).bind('beforeunload', function (e) {
        if (were_changes) {
            return true;
        } else {
            e = null; // i.e; if form state change show warning box, else don't show it.
        }
    });

    var $b1 = $("[name='btn_pub_to_store']").get(0);
    if ($b1) {
        $b1.addEventListener('mousedown', function () {
            were_changes = false;
        }, true);
    }

    var $b2 = $("[name='btn_pub_changes']").get(0);
    if ($b2) {
        $b2.addEventListener('mousedown', function () {
            were_changes = false;
        }, true);
    }

    var $b3 = $("[name='btn_remove_from_store']").get(0);
    if ($b3) {
        $b3.addEventListener('mousedown', function () {
            were_changes = false;
        }, true);
    }
});
