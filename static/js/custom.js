// baseUrl = 'http://nott.tk';
baseUrl = 'http://notes.lily.local:8080';


// ----------------------------------------------
// MAIN                                         -
// ----------------------------------------------
$(document).ready(function() {
    // Load WYSIWYG editor
    $('#editor').trumbowyg({
        btns: [
          'viewHTML',
          '|', 'btnGrp-design'
        ],
        btnsAdd: ['foreColor'],
        removeformatPasted: true,
        fullscreenable: false
    });

    var saveButton = makeSaveButton();
    $('.trumbowyg-button-pane').append(saveButton);
});


// ----------------------------------------------
// HELPERS                                      -
// ----------------------------------------------

// Get cookie value by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Display error in fadein/fadeout box in the center of the screen
function displayFlash(status, text) {
    var $block = $('#flash-message');
    if (status == 'error') {
        $block.find('span').removeClass('label-primary').addClass('label-danger');
        text = text || 'Error';
    }
    else if (status == 'info') {
        $block.find('span').removeClass('label-danger').addClass('label-primary');
        text = text || 'Success';
    }
    $block.find('span').html(text);

    $block.fadeIn(300).delay(500).fadeOut(300);
}

// Template for list item in side panel
function makeListItem(id, type, title, isChild) {
    if (type == 'notepad' && !isChild) {
        var addChild =
            '<span class="link-add-child">' +
                '<i class="glyphicon glyphicon-plus text-primary"></i>' +
            '</span>';
        var childClass = 'class="child" ';
    }
    else {
        addChild = '';
        childClass = '';
    }

    var li =
        '<li ' + childClass + 'data-type="' + type + '" data-id="' + id + '">' +
            '<a href="#" class="link-get">' +
                title +
            '</a>' +
            addChild +
            '<span class="link-edit">' +
                '<i class="glyphicon glyphicon-pencil text-primary" data-toggle="modal" data-target="#modal-edit"></i>' +
            '</span>' +
            '<span class="link-del">' +
                '<i class="glyphicon glyphicon-remove text-danger" data-toggle="modal" data-target="#modal-del"></i>' +
            '</span>' +
        '</li>';

    return li;
}

// Template for input form for child notepad creation
function makeForm(id) {
    var form =
        '<form>' +
            '<div class="form-group" data-type="notepad" data-parent-id="' + id + '">' +
                '<input type="text" name="title" class="form-control input-sm" placeholder="New notepad">' +
                '<span class="link-add">' +
                    '<i class="glyphicon glyphicon-plus text-primary"></i>' +
                '</span>' +
            '</div>' +
        '</form>';

    return form;
}

// Template for save button on editor's panel
function makeSaveButton() {
    var button = 
        '<li>' +
            '<button type="button" class="trumbowyg-button-save" title="Save" tabindex="-1" style="background: #337ab7;">Save</button>' +
        '</li>';
}


// ----------------------------------------------
// CRUD                                         -
// ----------------------------------------------

// Create notepad/note
function createItem($form, elementType) {
    if (elementType == 'notepad') {
        var sideBar = '.sidebar-first';
    }
    else if (elementType == 'note') {
        var sideBar = '.sidebar-second';
    }

    var elementTitle = $form.find('input').val();
    if (elementTitle == '') {
        displayFlash('error', 'Title cannot be empty');
        return;
    }

    var url = baseUrl + '/ajax/' + elementType + '/';
    if (elementType == 'notepad') {
        var data = {title: elementTitle};
        var parentId = $form.find('.form-group').data('parent-id');

        // Creating child notepad
        if (parentId) {
            data['parent'] = parentId;
        }
    }
    else if (elementType == 'note') {
        var notepadId = $('.sidebar-first li.active').data('id');
        var data = {title: elementTitle, id: notepadId};
    }

    $.ajax({
        beforeSend: function(response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: url,
        type: 'POST',
        dataType: 'json',
        data: data,
        success: function(response) {
            console.log(response);
            var newElement = makeListItem(response['id'], elementType, elementTitle);
            if (parentId) {
                $('.nav-sidebar > form').remove();
                $(newElement).insertAfter($(sideBar+' ul li[data-id="'+parentId+'"]'));

            }
            else {
                $(sideBar+' ul').append(newElement);
            }
            $form.find('input').val('');
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
    createItem($(this).closest('form'), 'notepad');
});
$(document).on('click', '.sidebar-second .link-add', function(event) {
    createItem($(this).closest('form'), 'note');
});
$(document).on('keypress', '.sidebar-first input[name="title"]', function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        createItem($(this).closest('form'), 'notepad');
    }
});
$(document).on('keypress', '.sidebar-second input[name="title"]', function(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        createItem($(this).closest('form'), 'note');
    }
});


// Read notepad's content (list of notes)
$(document).on('click', '.sidebar-first .link-get', function(event) {
    $('#btn-save').prop('disabled', true);

    var elementId = $(this).closest('li').data('id');
    var elementType = 'notepad';
    var $listItem = $(this).parent();
    var url = baseUrl + '/ajax/notepad/' + elementId;
    
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            var csrftoken = getCookie('csrftoken');

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


// Read note's content
$(document).on('click', '.sidebar-second .link-get', function(event) {
    $('#editor-block').css({"visibility":"visible"});
    $('#btn-save').prop('disabled', false);

    var elementId = $(this).closest('li').data('id');
    var elementType = 'note';
    var url = baseUrl + '/ajax/note/' + elementId;1
    var $listItem = $(this).parent();
    $listItem.siblings().removeClass('active');
    $listItem.addClass('active');
    
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            // Need to clear editor explicitly if response text is empty string
            $('#editor').trumbowyg('empty');
            $('#editor').trumbowyg('html', response['text']);
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
    var $listItem = $(event.relatedTarget).closest('li');
    var elementId = $listItem.data('id');
    var elementType = $listItem.data('type');

    $(event.currentTarget).find('input[name="id"]').val(elementId);
    $(event.currentTarget).find('input[name="type"]').val(elementType);

    // Only for edit
    if ($(event.currentTarget).find('input[name="title"]').length) {
        var elementTitle = $listItem.find('a').html().trim();
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

    if (elementTitle == '') {
        $('#modal-edit').modal('hide');
        displayFlash('error', 'Error: title cannot be empty');
        return;
    }

    if (elementType == 'notepad') {
        var url = baseUrl + '/ajax/notepad/' + elementId;
    }
    else if (elementType == 'note') {
        var url = baseUrl + '/ajax/note/' + elementId;
    }

    $.ajax({
        beforeSend: function(response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader("X-CSRFToken", csrftoken);

        },
        url: url,
        type: 'PUT',
        data: {title: elementTitle},
        success: function(response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            $('a[data-type="'+elementType+'"][data-id="'+elementId+'"]').html(elementTitle);
        },
        error: function(response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// Save note's content
$(document).on('click', '#btn-save', function(event) {
    var noteId = $('.sidebar-second li.active').data('id');
    var text = $('#editor').trumbowyg('html');

    $.ajax({
        beforeSend: function(response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: baseUrl + '/ajax/note/' + noteId,
        type: 'PUT',
        data: {text: text},
        success: function(response) {
            console.log(response);
            displayFlash('info', 'Saved successfully');
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

    if (elementType == 'notepad') {
        var url = baseUrl + '/ajax/notepad/' + elementId;
        // If there were opened form for deleted notepad
        var $childFormButton = $('span[data-parent-id="'+elementId+'"]');
    }
    else if (elementType == 'note') {
        var url = baseUrl + '/ajax/note/' + elementId;
    }

    $.ajax({
        beforeSend: function(response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: url,
        type: 'DELETE',
        success: function(response) {
            console.log(response);
            $('#modal-del').modal('hide');
            // If it was active notepad - hide right panel
            // Notes deleted automaticaly by Django (cascade delete)
            $listItem = $('a[data-type="'+elementType+'"][data-id="'+elementId+'"]').parent();
            if ($listItem.hasClass('active')) {
                $('.sidebar-second ul').html('');
            }
            $listItem.remove();

            // If there were opened form for deleted notepad
            if ($childFormButton) {
                $childFormButton.closest('form').remove();
            }
        },
        error: function(response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText)['error'];
            displayFlash('error', errorMessage);
        }
    });
});


// ----------------------------------------------
// INTERFACE                                    -
// ----------------------------------------------


// Show loading icon on each AJAX query
var $loaderIcon = $('#ajax-load-icon').hide();
$(document)
  .ajaxStart(function () {
    $loaderIcon.show();
  })
  .ajaxStop(function () {
    $loaderIcon.hide();
  });


// Make new input form for creating child notepad
$(document).on('click', '.link-add-child', function() {
    var $listItem = $(this).closest('li');
    var parentId = $listItem.data('id');

    // Check if there already is an additional form
    var $prevForm = $('.sidebar-first > .nav-sidebar > form');
    if ($prevForm.length) {
        var prevId = $prevForm.find('.form-group').data('parent-id');
    }
    else {
        prevId = null;
    }

    // If it is second click on same element
    // then only hide previous form
    $('.nav-sidebar > form').remove();
    if (parentId != prevId || !prevId) {
        console.log('ding!');
        var newForm = makeForm(parentId);
        $(newForm).insertAfter($listItem);
    }
});