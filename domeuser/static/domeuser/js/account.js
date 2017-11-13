'use strict';

$(document).ready(function () {
    var $userNameElem = $('#user-name');
    var userNameOriginalValue = $userNameElem.val();
    // var userEmail = $('#current-email').val();
    var saveNameBtn = $('#save-name');
    var saveEmailBtn = $('#save-email');
    var savePassBtn = $('#save-passwd');
    var alertDiv = $('#alert-area .alert');
    var userAPIUrl = '/account/edit/api/';

    saveNameBtn.on('click', function () {
        if (userNameOriginalValue != $userNameElem.val() && $userNameElem.val()) {
            pendingBtn(saveNameBtn);
            $.ajax({
                method: 'post',
                url: userAPIUrl,
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                data: {
                    action: 'change_first_name',
                    new_name: $userNameElem.val()
                },
                dataType: 'json'
            }).done(function (resp) {
                $userNameElem.val(resp.name);
                unpendingBtn(saveNameBtn);
                showSuccessAlert('Name changed');
            }).fail(function () {
                unpendingBtn(saveNameBtn);
            });
        } else {
            showErrorAlert('Name have not been changed');
            $userNameElem.popover('show');
        }
    });

    saveEmailBtn.on('click', function () {
        if ($('#new-email').val() && $('#current-passwd1').val()) {
            pendingBtn(saveEmailBtn);
            $.ajax({
                method: 'post',
                url: userAPIUrl,
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                dataType: 'json',
                data: {
                    action: 'change_email',
                    new_email: $('#new-email').val(),
                    pass: $('#current-passwd1').val()
                }
            }).done(function (resp) {
                $('#current-email').val(resp.email);
                $('#current-passwd1').val('');
                $('#new-email').val('');
                unpendingBtn(saveEmailBtn);
                showSuccessAlert('Email changed');
            }).fail(function (resp) {
                if (resp.status == 400) {
                    showErrorAlert(resp.responseText);
                }
                unpendingBtn(saveEmailBtn);
            });
        } else {
            showErrorAlert('Enter password and new email');
        }
    });

    savePassBtn.on('click', function () {
        if ($('#new-passwd').val() && $('#re-passwd').val() &&
            $('#current-passwd2').val()
        ) {
            if ($('#new-passwd').val() == $('#re-passwd').val()) {
                $.ajax({
                    method: 'post',
                    url: userAPIUrl,
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    dataType: 'json',
                    data: {
                        action: 'change_pass',
                        pass: $('#current-passwd2').val(),
                        pass1: $('#new-passwd').val(),
                        pass2: $('#re-passwd').val()
                    }
                }).done(function (resp) {
                    showSuccessAlert('Password saved');
                    window.location.reload();
                }).fail(function (resp) {
                    if (resp.status == 400) {
                        showErrorAlert(resp.responseText);
                    }
                });
            } else {
                showErrorAlert('The passwords do not match');
            }
        } else {
            showErrorAlert('Fill the form');
        }
    });

    function pendingBtn(btn) {
        btn.prop('disabled', true);
    }

    function unpendingBtn(btn) {
        btn.prop('disabled', false);
    }

    function showErrorAlert(msg) {
        msg = msg || 'An error happened';
        alertDiv.removeClass('alert-success').addClass('alert-danger')
            .show().find('.alert-content').text(msg);
        setTimeout(function () {
            alertDiv.fadeOut();
        }, 3000);
    }

    function showSuccessAlert(msg) {
        alertDiv.removeClass('alert-danger').addClass('alert-success')
            .show().find('.alert-content').text(msg);
        setTimeout(function () {
            alertDiv.fadeOut();
        }, 3000);
    }

    $('.alert').on('click', function () {
        $(this).fadeOut();
    });
});
