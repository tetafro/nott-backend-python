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
    var $block = $("#flash-block");
    var $msg = $("#flash-msg");
    // $.post('/note/1/', {text: text});
    $.ajax({
        // contentType: "application/json",
        // traditional: true,
        // dataType: "json",
        url: "/note/1/",
        type: "POST",
        data: {text: text},
        success: function(response) {
            $block.hide().fadeIn(300).delay(500).fadeOut(300);
        },
        error: function(response) {
            alert("Fail");
        }
    });
};
// Действие по клику на кнопку
$(document).on('click', '#btn-save', saveNote);
