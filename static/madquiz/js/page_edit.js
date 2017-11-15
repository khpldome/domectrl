$(document).ready(function () {
    // $('#answer-template input').val('');
    var answerTemplate = $('#answer-template').html();
    var $addAnswerForm = $('#new-answer-form');
    var $addAnswerBtn = $addAnswerForm.find('button');
    var $addAnswerText = $addAnswerForm.find('input');
    var answerIndex = $('#all-answers .flex-row').length;
    var $answerList = $('#all-answers');

    if ($('input.radio-correct-answer').length) {
        // sync hidden checkboxes and radio
        $('input:checked[id$=-is_correct]').closest('div.is-correct')
            .find('input.radio-correct-answer')
            .prop('checked', true);
    }

    if ($answerList.length) {
        // firefox can save hidden checked checkboxes after page refresh so uncheck them manually
        $('#answer-list .flex-row:visible input[id$=-DELETE]:checked').prop('checked', false);
        $('#id_answer-TOTAL_FORMS').val($('#all-answers .flex-row').length);

        $answerList.on('click', 'input.radio-correct-answer',
            function (e) {
                $('input:checked[id$=-is_correct]').prop('checked', false);
                $(e.target).closest('div.is-correct')
                    .find('input[id$=-is_correct]').prop('checked', true);
            }
        );

        Sortable.create($('#answer-list')[0], {
            handle: '.handle-list',
            draggable: '.flex-row',
            animation: 300,
            ghostClass: "sortable-ghost",
            onEnd: function (evt) {
                setAnswerOrder()
            }
        });

        $addAnswerBtn.on('click', function () {
            addAnswer();
        });

        $('#new-answer-text input').on('keypress', function (e) {
            if (e.which == 13) {
                e.preventDefault();
                addAnswer();
            }
        });

        $answerList.on('click', '.answer-delete', function () {
            var answerDelInput = $(this).closest('.flex-row').find('input[id$=-DELETE]');
            if (answerDelInput.length) {
                answerDelInput.prop('checked', true);
                $(this).closest('.flex-row').hide();
            } else {
                $(this).closest('.flex-row').remove();
                answerIndex = $('#all-answers .flex-row').length;
                $('#id_answer-TOTAL_FORMS').val(answerIndex);
                setAnswerOrder();
            }
        });
    }

    function addAnswer() {
        if ($addAnswerText.val()) {
            answerIndex = $('#all-answers .flex-row').length;
            var indexToReplace = answerTemplate.match(/-\d+-/)[0].replace(/\D/g, '');
            var regexp = new RegExp('answer-' + indexToReplace, 'g');
            var answer = $(answerTemplate.replace(regexp, 'answer-' + answerIndex));
            answer.find('.answer-text input').val($addAnswerText.val());
            answer.find('.handle-list').remove();
            $addAnswerText.val('');
            answer.appendTo('#answer-list-add');
            $('#id_answer-TOTAL_FORMS').val(answerIndex + 1);
            setAnswerOrder();
            $addAnswerText.focus();
        }
    }

    function setAnswerOrder() {
        $('#all-answers').find('.flex-row').each(function (index, item) {
            var order_element = $(item).find('input[id$="order"]');
            if (order_element.val() != index + 1) {
                order_element.val(index + 1);
            }
            if (order_element.attr('id') != 'id_answer-' + index + '-order') {
                order_element.attr('id', 'id_answer-' + index + '-order');
                order_element.attr('name', 'answer-' + index + '-order');
            }
            var title_element = $(item).find('input[id$="-title"]');
            if (title_element.attr('id') != 'id_answer-' + index + '-title') {
                title_element.attr('id', 'id_answer-' + index + '-title');
                title_element.attr('name', 'answer-' + index + '-title');
            }
            var is_correct_element = $(item).find('input[id$="-is_correct"]');
            if (is_correct_element.attr('id') != 'id_answer-' + index + '-is_correct') {
                is_correct_element.attr('id', 'id_answer-' + index + '-is_correct');
                is_correct_element.attr('name', 'answer-' + index + '-is_correct');
            }
            var id_element = $(item).find('input[id$="-id"]');
            if (id_element.attr('id') != 'id_answer-' + index + '-id') {
                id_element.attr('id', 'id_answer-' + index + '-id');
                id_element.attr('name', 'answer-' + index + '-id');
            }
            var delete_element = $(item).find('input[id$="-DELETE"]');
            if (delete_element.attr('id') !== undefined && delete_element.attr('id') != 'id_answer-' + index + '-DELETE') {
                delete_element.attr('id', 'id_answer-' + index + '-DELETE');
                delete_element.attr('name', 'answer-' + index + '-DELETE');
            }
        });
    }
});
