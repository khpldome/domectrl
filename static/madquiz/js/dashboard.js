
$(document).ready(function () {

    $('button.study').on('click', function () {
        $('#go-study').attr('action', this.dataset.url);
    });

    $('button.mod-delete').on('click', function () {
        $('#go-delete').attr('action', this.dataset.url);
        // console.log('button_delete!!! url= ' + this.dataset.url);
    });


    $('#confirm-delete').on('show.bs.modal', function (event) {

        var button = $(event.relatedTarget);        // Button that triggered the modal
        var recipient = button.data('whatever');    // Extract info from data-* attributes

        console.log('show.bs.modal!!!' + button + " whatever= " + recipient);

        var modal = $(this);
        // modal.find('.modal-title').text('New message to ' + recipient)
        modal.find('.modal-body p').text('Are you sure you want to delete "' + recipient + '" module?')
    })

});
