$(document).ready(function () {
    var moduleAPIUrl = window.location.pathname + 'api/';
    var $pageList = $('#page-list');

    if($pageList.length){
        Sortable.create($('#page-list')[0], {
            handle: '.handle-list',
            draggable: '.flex-row',
            animation: 300,
            ghostClass: "sortable-ghost",
            onEnd: function () {
                setPageOrder();
            }
        });
    }

    function setPageOrder() {
        var pageOrder = {};

        if($pageList.length) {
            $pageList.find('.flex-row').each(function (i, item) {
                pageOrder[$(item).data('pageId')] = i + 1;
            });
        }
        savePageOrder(pageOrder);
    }

    function savePageOrder(data) {
        $.ajax({
            method: 'post',
            url: moduleAPIUrl,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: {
                order: JSON.stringify(data),
                action: 'change_page_order'
            }
        }).done(function (response) {
            // console.log('order saved');
        }).fail(function (response) {
            // console.log('save order failed');
        });
    }

    // change action url for the form on study modal popup
    $('button.study').on('click', function () {
        $('#go-study').attr('action', this.dataset.url);
    });

    // to "restore" selected tab
    if (location.hash.substr(0, 2) == "#!") {
        $("a[href='#" + location.hash.substr(2) + "']").tab("show");
    }

    // to "remember" selected tab
    $("a[data-toggle='tab']").on("shown.bs.tab", function (e) {
        var hash = $(e.target).attr("href");
        if (hash.substr(0, 1) == "#") {
            location.replace("#!" + hash.substr(1));
        }
    });

    $('button.btn-share').on('click', function () {
        var $recipients = $('#recipients-email-address');
        var $messageModal = $('#message-modal');
        $.ajax({
            method: 'post',
            url: moduleAPIUrl,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: {
                action: 'module_share',
                email: $recipients.val(),
                module_id: $recipients.data('module_id')
            }
        }).done(function (response) {
            console.log('module shared: ', response);
            $messageModal.find('.modal-text').html('Thanks for sharing module!');
            $messageModal.modal('show');
            $recipients.val('');
        }).fail(function (response) {
            $messageModal.find('.modal-text').html('Something wrong happens, please try later!');
            $messageModal.modal('show');
            console.log('module sharing error: ', response);
        });
    });

    var content_editor = CKEDITOR.replace('id_description',
        {
            extraPlugins: 'responsivevoice',
            toolbar: [
                ['Bold', 'Italic', 'Underline', 'Strikethrough', 'Subscript', 'Superscript',
                    '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', '-', 'About', '-'],
                ['ResponsiveVoice']
            ]
        });

    // TODO identify tabs correctly
    var $buttonStudy = $('button.study');
    $buttonStudy.hide();  //or do it through css

    $('a.tab_settings').click(function () {
        $buttonStudy.hide();
    });

    $('a.tab_share').click(function () {
        $buttonStudy.hide();
    });

    $('a.tab_monetize').click(function () {
        $buttonStudy.hide();
    });

    $('a.tab_pages').click(function () {
        $buttonStudy.show();
    });

    function getIndex() {
        return $('ul.nav.nav-tabs > .active').index()
    }

    var idx = getIndex();
    console.log('idx= ' + idx);
    if (idx === 0) {
        $buttonStudy.show();
    } else {
        $buttonStudy.hide();
    }

    var were_changes = false;

    var $settings = $('#settings');
    $settings.find('#id_name[name="name"]').on('input', function () {
        // console.log('name changed= ');
        were_changes = true
    });

    $settings.find('#id_description[name="description"]').on('input', function () {
        // console.log('description changed= ');
        were_changes = true
    });

    $settings.find('#id_category[name="category"]').on('input', function () {
        // console.log('category changed= ');
        were_changes = true
    });

    $settings.find('#id_isbn[name="isbn"]').on('input', function () {
        // console.log('isbn changed= ');
        were_changes = true
    });


    // var form_original_data = $("form").serialize();

    // $(':input').each(function() {
    //     $(this).data('initialValue', $(this).val());
    // });

    content_editor.on('key', function () {
        console.log('content_editor changed= ');
        were_changes = true
    });

    $(window).bind('beforeunload', function (e) {

        // if ($("form").serialize() != form_original_data) {
        //     console.log('form changed= ');
        // }

        // $(':input').each(function () {
        //     if($(this).data('initialValue') != $(this).val()){
        //         console.log('form element changed= ' + $(this).data('initialValue') + " " + $(this).val());
        //     }
        // });

        // check form hash
        // var were_changes = true;
        var a = [
            'btn',
            'elem'
        ];
        delete a['btn'];
        // var hash = sort(a).join(',');

        if (were_changes) {
            return false;
        } else {
            e = null; // i.e; if form state change show warning box, else don't show it.
        }
    });

    $("[name='btn_create_save_changes']").get(0).addEventListener('mousedown', function () {
        were_changes = false;
    }, true);
});
