// Показать flash-сообщение, вывести Summernote
function onLoad(object) {
    $('#summernote').summernote({
        height: '100%',
        toolbar: [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['color', ['color']],
            ['codeview', ['codeview']]
        ]
    });
};
// Действие при загрузке страницы
$(document).ready(onLoad);


function saveNote(object) {
    var text = $('.note-editable').first().html();
    var $block_success = $("#flash-block-success");
    var $block_fail = $("#flash-block-fail");

    $.ajax({
        // contentType: "application/json",
        // traditional: true,
        // dataType: "json",
        url: window.location,
        type: "POST",
        data: {text: text},
        success: function(response) {
            $block_success.hide().fadeIn(300).delay(500).fadeOut(300);
        },
        error: function(response) {
            $block_fail.hide().fadeIn(300).delay(500).fadeOut(300);
        }
    });
};
// Действие по клику на кнопку
$(document).on('click', '#btn-save', saveNote);
