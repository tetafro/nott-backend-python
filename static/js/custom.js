baseUrl = 'http://127.0.0.1:8000';
// var $blockSuccess = $('#flash-block-success');
// var $blockFail = $('#flash-block-fail');
// $blockSuccess.hide().fadeIn(300).delay(500).fadeOut(300);
// $blockFail.hide().fadeIn(300).delay(500).fadeOut(300);


// Создать блокнот
$(document).on('click', '.link-add', function(object) {
    var notepadTitle = $(this).prev().val();

    $.ajax({
        url: baseUrl + '/ajax/notepad/',
        type: 'POST',
        data: {title: notepadTitle},
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
});


// Получить список заметок блокнота
$(document).on('click', '.link-get', function(object) {
    var elementId = $(this).data('id');
    var elementType = $(this).data('type');

    if(elementType == 'notepad')
        var url = baseUrl + '/ajax/notepad/' + elementId;
    else if(elementType == 'note')
        var url = baseUrl + '/ajax/note/' + elementId;
    
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
});










// При появлении модального окна подставить туда информацию о заметке/блокноте
$(document).on('show.bs.modal', '#modal-del', function(object) {
    var elementId = $(object.relatedTarget).data('id');
    var elementType = $(object.relatedTarget).data('type');

    $(object.currentTarget).find('input[name="id"]').val(elementId);
    $(object.currentTarget).find('input[name="type"]').val(elementType);
});


// Удалить блокнот/заметку
$(document).on('click', '#modal-del-submit', function(object) {
    var $blockSuccess = $('#flash-block-success');
    var $blockFail = $('#flash-block-fail');

    if(elementType == 'notepad')
        var url = baseUrl + '/ajax/notepad/' + elementId;
    else if(elementType == 'note')
        var url = baseUrl + '/ajax/note/' + elementId;

    $.ajax({
        url: url,
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
});







// При загрузке страницы показать flash-сообщение, вывести Summernote
$(document).ready(function(object) {
    $('#summernote').summernote({
        height: '100%',
        toolbar: [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['color', ['color']],
            ['codeview', ['codeview']]
        ]
    });
});


// Сохранить текст заметки
function saveNote(object) {
    var text = $('.note-editable').first().html();
    var $blockSuccess = $('#flash-block-success');
    var $blockFail = $('#flash-block-fail');

    $.ajax({
        url: window.location,
        type: 'POST',
        data: {text: text},
        dataType: 'json',
        success: function(response) {
            $blockSuccess.hide().fadeIn(300).delay(500).fadeOut(300);
        },
        error: function(response) {
            $blockFail.hide().fadeIn(300).delay(500).fadeOut(300);
        }
    });
};
// Действие по клику на кнопку
$(document).on('click', '#btn-save', saveNote);