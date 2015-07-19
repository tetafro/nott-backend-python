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
    // $.post('/note/1/', {text: text});
    $.ajax({
        // contentType: "application/json",
        // traditional: true,
        // dataType: "json",
        url: "/note/1/",
        type: "POST",
        data: {text: text},
        success: function(response) {
            alert("Done");
        },
        error: function(response) {
            alert("Fail");
        }
    });
};
// Действие по клику на кнопку
$(document).on('click', '#btn-save', saveNote);
