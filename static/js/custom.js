// baseUrl = 'http://127.0.0.1:8000';
// baseUrl = 'http://notes.lily.local:80';
baseUrl = 'http://notes.lily.local:8080';

// ----------------------------------------------
// HELPERS                                      -
// ----------------------------------------------

// Display error in fadein/fadeout box in the center of the screen
function displayFlash(status, text) {
    var $block = $('#flash-message');
    if(status == 'error') {
        $block.find('span').removeClass('label-primary').addClass('label-danger');
        text = text || 'Error';
    }
    else if(status == 'info') {
        $block.find('span').removeClass('label-danger').addClass('label-primary');
        text = text || 'Success';
    }
    $block.find('span').html(text);

    $block.fadeIn(300).delay(500).fadeOut(300);
}


// Template for list item in side panel
function makeListItem(id, type, title) {
    var li =
    '<li>' +
        '<a href="#" class="link-get" data-id="' + id + '" data-type="' + type + '">' +
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


// ----------------------------------------------
// CRUD                                         -
// ----------------------------------------------

// Create notepad/note
function createItem(elementType) {
    if(elementType == 'notepad')
        var sideBar = '.sidebar-first';
    else if(elementType == 'note')
        var sideBar = '.sidebar-second';

    var elementTitle = $(sideBar+' input[name="title"]').val();
    if(elementTitle == '') {
        console.log('Error: title cannot be empty');
        return;
    }

    var url = baseUrl + '/ajax/' + elementType + '/';
    if(elementType == 'notepad') {
        var data = {title: elementTitle};
    }
    else if(elementType == 'note') {
        var notepadId = $('.sidebar-first li.active a').data('id');
        var data = {title: elementTitle, id: notepadId};
    }

    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: data,
        success: function(response) {
            console.log(response);
            var newElement = makeListItem(response['id'], elementType, elementTitle);
            $(sideBar+' ul').append(newElement);
            $(sideBar+' form').find('input').val('');
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
};
// Create item on clicking plus icon or on pressing enter key
$(document).on('click', '.sidebar-first .link-add', function(event) {
    createItem('notepad');
});
$(document).on('click', '.sidebar-second .link-add', function(event) {
    createItem('note');
});
$(document).on('keypress', '.sidebar-first input[name="title"]', function(event) {
    if(event.keyCode == 13)
        createItem('notepad');
});
$(document).on('keypress', '.sidebar-second input[name="title"]', function(event) {
    if(event.keyCode == 13)
        createItem('note');
});


// Read notepad's content (list of notes)
$(document).on('click', '.sidebar-first .link-get', function(event) {
    // Hide and clean textarea if no note selected
    $('#editor-block').hide();
    $('.note-editable').first().html('');

    var elementId = $(this).data('id');
    var elementType = 'notepad';
    var $listItem = $(this).parent();
    var url = baseUrl + '/ajax/notepad/' + elementId;
    
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            $listItem.siblings().removeClass('active');
            $listItem.addClass('active');
            $('.sidebar-second input[name="title"]').removeAttr('disabled');
            var itemsList = '';
            $.each(response['notes'], function(id, title) {
                itemsList += makeListItem(id, 'note', title);
            });
            $('.sidebar-second ul').html(itemsList);
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// Read note's content (load Summernote with text in it)
$(document).on('click', '.sidebar-second .link-get', function(event) {
    $('#editor-block').show();
    $('#summernote').summernote({
        height: '100%',
        toolbar: [
            ['style', ['bold', 'italic', 'underline']],
            ['color', ['color']],
            ['codeview', ['codeview']]
        ]
    });

    var elementId = $(this).data('id');
    var elementType = 'note';
    var url = baseUrl + '/ajax/note/' + elementId;
    var $listItem = $(this).parent();
    $listItem.siblings().removeClass('active');
    $listItem.addClass('active');
    
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            $('.note-editable').first().html(response['text']);
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// Put notepad/note info into hidden inputs on modal show
function populateModal(event) {
    var elementId = $(event.relatedTarget).data('id');
    var elementType = $(event.relatedTarget).data('type');

    $(event.currentTarget).find('input[name="id"]').val(elementId);
    $(event.currentTarget).find('input[name="type"]').val(elementType);

    // Only for edit
    if($(event.currentTarget).find('input[name="title"]').length) {
        var elementTitle = $('.nav-sidebar a[data-id="'+elementId+'"][data-type="'+elementType+'"]').html().trim();
        $(event.currentTarget).find('input[name="title"]').val(elementTitle);
    }
};
$(document).on('show.bs.modal', '#modal-edit', populateModal);
$(document).on('show.bs.modal', '#modal-del', populateModal);


// Rename notepad/note (via modal window)
$(document).on('click', '#modal-edit-submit', function(event) {
    var elementId = $('#modal-edit-id').val();
    var elementType = $('#modal-edit-type').val();
    var elementTitle = $('#modal-edit-title').val();

    if(elementType == 'notepad')
        var url = baseUrl + '/ajax/notepad/' + elementId;
    else if(elementType == 'note')
        var url = baseUrl + '/ajax/note/' + elementId;

    $.ajax({
        url: url,
        type: 'PUT',
        dataType: 'json',
        data: {title: elementTitle},
        success: function(response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            $('a[data-type="'+elementType+'"][data-id="'+elementId+'"]').html(elementTitle);
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// Save note's content
$(document).on('click', '#btn-save', function(event) {
    var noteId = $('.sidebar-second li.active a').data('id');
    var text = $('.note-editable').first().html();

    $.ajax({
        url: baseUrl + '/ajax/note/' + noteId,
        type: 'PUT',
        data: {text: text},
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// Delete notepad/note (via modal window)
$(document).on('click', '#modal-del-submit', function(event) {
    var elementId = $('#modal-del-id').val();
    var elementType = $('#modal-del-type').val();

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
            $('#modal-del').modal('hide');
            // If it was active notepad - hide right panel
            // Notes deleted automaticaly by Django (cascade delete)
            $listItem = $('a[data-type="'+elementType+'"][data-id="'+elementId+'"]').parent();
            if($listItem.hasClass('active'))
                $('.sidebar-second ul').html('');
            $listItem.remove();
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});
