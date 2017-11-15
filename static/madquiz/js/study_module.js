$(document).ready(function () {

    var nextBtn = $('#next-btn'),
        answerDiv = $('#answer'),
        goNext = answerDiv.length ? false : true,
        answerType = answerDiv.find('input').attr('type'),
        answerResponse = $('#answer-response'),
        userAnswer = [];

    nextBtn.on('click', function () {
        if (nextBtn.prop('disabled') == false && goNext) {
            window.location.href = nextBtn.data('href');
        } else {
            if (answerType == 'radio') {
                userAnswer = answerDiv.find('input:checked').val();
            } else if (answerType == 'checkbox') {
                answerDiv.find('input:checked').each(function (i, item) {
                    userAnswer.push($(item).val());
                });
            } else if (answerType == 'text') {
                userAnswer = answerDiv.find('input[type=text]').val().trim();
            }
            nextBtn.prop('disabled', true);
            $.ajax({
                method: 'post',
                url: acceptAnswerUrl,
                data: {
                    user_answer: JSON.stringify(userAnswer),
                    action: 'check_answer'
                },
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                dataType: 'json'
            }).done(function (resp) {
                nextBtn.prop('disabled', false).text('Next');
                showAnswerResponse(resp);
            }).fail(function (resp) {
                nextBtn.prop('disabled', false);
                /** @namespace resp.responseJSON */
                if (resp.responseJSON && resp.responseJSON.error) {
                    $('#quiz-content').append(
                        '<div class="alert alert-danger" role="alert">'
                        + resp.responseJSON.error + '</div>'
                    );
                }
            });
            goNext = true;
        }
    });

    answerDiv.find('input[name="answer"]').on('change input', function () {
        nextBtn.prop('disabled', false);
    });

    function showAnswerResponse(resp) {
        /** @namespace resp.correct */
        /** @namespace resp.correct_answer */
        /** @namespace resp.interrupt */
        if (resp.correct) {
            answerResponse.find('.panel-heading').text('Correct Answer');
            answerResponse.find('.panel-body').text('Nicely done.');
            answerResponse.addClass('panel-success').removeClass('hidden');
        } else {
            answerResponse.find('.panel-heading').text('Incorrect Answer');
            if (resp.correct_answer) {
                answerResponse.find('.panel-body').prepend(
                    '<p>The correct answer was:<p>'
                );
                if (answerType == 'text') {
                    answerResponse.find('.panel-body ul')
                        .append('<li>' + resp.correct_answer + '</li>');
                } else if (answerType == 'radio') {
                    var answerInput = answerDiv.find('input[value=' + resp.correct_answer + ']');
                    answerDiv.find('.incorrect').removeClass('hidden');
                    answerInput.parent().siblings('span').addClass('hidden');
                    var answer = answerInput.parent().text().trim();
                    answerResponse.find('.panel-body ul').append('<li>' + answer + '</li>');
                } else if (answerType == 'checkbox') {
                    answerDiv.find('.incorrect').removeClass('hidden');
                    resp.correct_answer.forEach(function (item) {
                        var answerInput = answerDiv.find('input[value=' + item + ']');
                        var answer = answerInput.parent().text().trim();
                        answerInput.parent().siblings('span').addClass('hidden');
                        answerResponse.find('.panel-body ul').append('<li>' + answer + '</li>');
                    });
                }
            } else {
                answerResponse.find('.panel-body').text('Not good');
            }
            answerResponse.addClass('panel-danger').removeClass('hidden');
            if (resp.interrupt) {
                nextBtn.attr('data-href', resp.interrupt);
            }
        }
    }

    $(document).keypress(function (e) {
        if (e.which == 13) {
            nextBtn.click();
        }
    });
});
