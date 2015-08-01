baseUrl = 'http://127.0.0.1:8000';
// var $blockSuccess = $('#flash-block-success');
// var $blockFail = $('#flash-block-fail');
// $blockSuccess.hide().fadeIn(300).delay(500).fadeOut(300);
// $blockFail.hide().fadeIn(300).delay(500).fadeOut(300);

function makeListItem(id, type, title) {
    var li =
    '<li>' +
        '<a href="#" class="link-get" data-id="' + id + '" data-type="notepad">' +
            title +
        '</a>' +
        '<span class="link-edit">' +
            '<i class="glyphicon glyphicon-pencil text-primary" data-toggle="modal" data-target="#modal-edit" data-type="' + type + '" data-id="' + id + '"></i>' +
        '</span>' +
        '<span class="link-del">' +
            '<i class="glyphicon glyphicon-remove text-danger" data-toggle="modal" data-target="#modal-del" data-type="' + type + '" data-id="' + id + '"></i>' +
        '</span>' +
    '</li>';

    return li;
}

// Create notepad
$(document).on('click', '.link-add', function(object) {
    var title = $(this).prev().val();

    $.ajax({
        url: baseUrl + '/ajax/notepad/',
        type: 'POST',
        dataType: 'json',
        data: {title: title},
        success: function(response) {
            console.log(response);
            var newElement = makeListItem(response['id'], response['type'], response['title']);
            $inputItem = $('.sidebar-first').children(":first").children(":last");
            $(newElement).insertBefore($inputItem);
            $inputItem.find('input').val('');

        },
        error: function(response) {
            console.log(response);
        }
    });
});


// Get list of notes for notepad
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


// Set notepad/note info into hidden inputs on modal show
function populateModal(object) {
    var elementId = $(object.relatedTarget).data('id');
    var elementType = $(object.relatedTarget).data('type');

    $(object.currentTarget).find('input[name="id"]').val(elementId);
    $(object.currentTarget).find('input[name="type"]').val(elementType);
};
$(document).on('show.bs.modal', '#modal-edit', populateModal);
$(document).on('show.bs.modal', '#modal-del', populateModal);


// Rename notepad/note
$(document).on('click', '#modal-edit-submit', function(object) {
    var elementId = $('#modal-edit-id').val();
    var elementType = $('#modal-edit-type').val();
    var title = $('#modal-edit-title').val();

    if(elementType == 'notepad')
        var url = baseUrl + '/ajax/notepad/' + elementId;
    else if(elementType == 'note')
        var url = baseUrl + '/ajax/note/' + elementId;

    $.ajax({
        url: url,
        type: 'PUT',
        dataType: 'json',
        data: {title: title},
        success: function(response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            $('[data-type="'+elementType+'"][data-id="'+elementId+'"]').html(title);
        },
        error: function(response) {
            console.log(response);
        }
    });
});


// Delete notepad/note
$(document).on('click', '#modal-del-submit', function(object) {
    var elementId = $('#modal-del-id').val();
    var elementType = $('#modal-del-type').val();

    if(elementType == 'notepad')
        var url = baseUrl + '/ajax/notepad/' + elementId;
    else if(elementType == 'note')
        var url = baseUrl + '/ajax/note/' + elementId;

    $.ajax({
        url: url,
        type: 'DELETE',
        success: function(response) {
            console.log(response);
            $('#modal-del').modal('hide');
            $('[data-type="'+elementType+'"][data-id="'+elementId+'"]').parent().remove();
        },
        error: function(response) {
            console.log(response);
        }
    });
});







// Show Summernote on page load
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


// Save note content
$(document).on('click', '#btn-save', function(object) {
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
});
