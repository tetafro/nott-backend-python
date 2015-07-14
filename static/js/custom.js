$(document).ready(function() {
    $('#summernote').summernote({
        height: '100%',
        toolbar: [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['color', ['color']],
            ['codeview', ['codeview']]
        ]
    });
});


function saveNote(object) {
    var text = $('.note-editable').first().html();
    // alert(text);
    $.post('/note/1/', {text: text});
};
// Действие по клику на кнопку
$(document).on('click', '#btn-save', saveNote);
