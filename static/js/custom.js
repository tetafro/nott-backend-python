// var baseUrl = 'http://nott.tk';
var baseUrl = 'http://notes.lily.local:8080';

// ----------------------------------------------
// HELPERS                                      -
// ----------------------------------------------

// Get cookie value by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie) {
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

// Escape/unescape HTML special characters
function htmlEscape(html) {
    var text = $('<div/>').text(html).html();
    return text;
}
function htmlUnescape(text) {
    var html = $('<div/>').html(text).text();
    return html;
}

// Display error in fadein/fadeout box in the center of the screen
function displayFlash(status, text) {
    var $block = $('#flash-message');
    if (status == 'error') {
        $block.find('span').removeClass('label-primary').addClass('label-danger');
        text = text || 'Error';
    } else if (status == 'info') {
        $block.find('span').removeClass('label-danger').addClass('label-primary');
        text = text || 'Success';
    }
    $block.find('span').html(text);

    $block.fadeIn(300).delay(500).fadeOut(300);
}

// Template for list item in side panel
function makeListItem(id, type, title, isChild) {
    var addChild;
    var childClass;
    if (type == 'notepad') {
        if (isChild) {
            addChild = '';
            childClass = 'class="child" ';
        } else {
            addChild =
                '<span class="link-add-child">' +
                    '<i class="glyphicon glyphicon-plus text-primary"></i>' +
                '</span>';
            childClass = '';
        }
    } else {
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
        '<button type="button" class="btn btn-sm btn-primary btn-save" title="Save">' +
            '<i class="glyphicon glyphicon-ok"></i>' +
        '</button>';

    return button;
}

// Template for tab header for editor area
// (new tab is always active)
function makeTabHead(tabId) {
    var tabHead =
        '<li class="active" data-id=' + tabId + '>' +
            '<a href="#tab-' + tabId + '" role="tab" data-toggle="tab"></a>' +
        '</li>';

    return tabHead;
}

// Template for tab content for editor area
// (new tab is always active)
function makeTab(tabId) {
    var tab =
        '<div role="tabpanel" class="tab-pane active" id="tab-' + tabId + '">' +
            '<div id="editor-' + tabId + '" class="editor"></div>' +
        '</div>';

    return tab;
}

// Initialize WYSIWYG editor on specified tab
function newEditor(tabId) {
    // Load WYSIWYG editor
    $('#editor-'+tabId).trumbowyg({
        btns: [
            'viewHTML',
            ['bold', 'italic']
        ],
        btnsAdd: ['foreColor'],
        removeformatPasted: true,
        fullscreenable: false
    });

    var saveButton = makeSaveButton();
    $('.trumbowyg-button-pane').append(saveButton);
};


// ----------------------------------------------
// CRUD                                         -
// ----------------------------------------------

// Create notepad/note
function createItem($form, elementType) {
    var sideBar;
    if (elementType == 'notepad') {
        sideBar = '.sidebar-first';
    } else if (elementType == 'note') {
        sideBar = '.sidebar-second';
    }

    var elementTitle = $form.find('input').val();

    if (!elementTitle) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (elementTitle.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var data;
    var parentId;
    var url = baseUrl + '/ajax/' + elementType + '/';
    if (elementType == 'notepad') {
        data = {title: elementTitle};
        parentId = $form.find('.form-group').data('parent-id');

        // Creating child notepad
        if (parentId) {
            data.parent = parentId;
        }
    } else if (elementType == 'note') {
        notepadId = $('.sidebar-first li.active').data('id');
        data = {title: elementTitle, id: notepadId};
    }

    var newElement;
    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'POST',
        dataType: 'json',
        data: data,
        success: function (response) {
            console.log(response);
            if (parentId) {
                newElement = makeListItem(response.id, elementType, htmlEscape(elementTitle), true);
                $('.nav-sidebar > form').remove();
                $(newElement).insertAfter($(sideBar + ' ul li[data-id="' + parentId + '"]'));
            } else {
                newElement = makeListItem(response.id, elementType, htmlEscape(elementTitle), false);
                $(sideBar + ' ul').append(newElement);
            }
            $form.find('input').val('');
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
};
// Create item on clicking plus icon or on pressing enter key
$(document).on('click', '.sidebar-first .link-add', function (event) {
    createItem($(this).closest('form'), 'notepad');
});
$(document).on('click', '.sidebar-second .link-add', function (event) {
    createItem($(this).closest('form'), 'note');
});
$(document).on('keypress', '.sidebar-first input[name="title"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        createItem($(this).closest('form'), 'notepad');
    }
});
$(document).on('keypress', '.sidebar-second input[name="title"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        createItem($(this).closest('form'), 'note');
    }
});

// Read notepad's content (list of notes)
$(document).on('click', '.sidebar-first .link-get', function (event) {
    $('.btn-save').prop('disabled', true);

    var elementId = $(this).closest('li').data('id');
    var elementType = 'notepad';
    var $listItem = $(this).parent();
    var url = baseUrl + '/ajax/notepad/' + elementId;

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            console.log(response);
            $listItem.siblings().removeClass('active');
            $listItem.addClass('active');
            $('.sidebar-second input[name="title"]').removeAttr('disabled');
            var itemsList = '';
            $.each(response.notes, function (index, note) {
                itemsList += makeListItem(note.id, 'note', note.title, false);
            });
            $('.sidebar-second ul').html(itemsList);
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
});

// Read note's content
$(document).on('click', '.sidebar-second .link-get', function (event) {
    $('#editor-block').css({visibility: 'visible'});
    $('.btn-save').prop('disabled', false);

    var elementId = $(this).closest('li').data('id');
    var elementType = 'note';
    var elementTitle = $(this).html();
    var url = baseUrl + '/ajax/note/' + elementId;
    var $listItem = $(this).parent();
    $listItem.siblings().removeClass('active');
    $listItem.addClass('active');

    // If tab for selected note is already exist
    if ($('#tab-'+elementId).length > 0) {
        // Activate tab
        $('#editor-block > .nav-tabs > li').removeClass('active');
        $('#editor-block > .tab-content > .tab-pane').removeClass('active');
        $('#editor-block > .nav-tabs > li[data-id="'+elementId+'"]').addClass('active');
        $('#tab-'+elementId).addClass('active');

        return;
    }

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            console.log(response);

            // Make new tab
            var newTabHead = makeTabHead(elementId);
            var newTab = makeTab(elementId);

            // Append new tab
            $('#editor-block > .nav-tabs > li').removeClass('active');
            $('#editor-block > .tab-content > .tab-pane').removeClass('active');
            $('#editor-block > .nav-tabs').append(newTabHead);
            $('#editor-block > .tab-content').append(newTab);
            $('#editor-block > .nav-tabs > .active > a').html(elementTitle +
                 '<div class="tab-close">&times;</div>');

            // Make editor for the tab
            newEditor(elementId);

            // Need to clear editor explicitly if response text is empty string
            $('#editor-'+elementId).trumbowyg('empty');
            $('#editor-'+elementId).trumbowyg('html', response.text);
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
});

// Close note's tab
$(document).on('click', '.tab-close', function () {
    var $tabHead = $(this).closest('li');
    var elementId = $tabHead.data('id');
    var $tab = $('#tab-'+elementId);

    // Closing active tab
    if ($tabHead.hasClass('active')) {
        // Make first tab active
        if ($tabHead.siblings().length > 0) {
            $tabHead.siblings().first().addClass('active');
            $tab.siblings().first().addClass('active');
        }
    }
    // Destroy editor and remove tab
    // $('#editor-'+elementId).trumbowyg('destroy');
    $tabHead.remove();
    $tab.remove();
})

// Put notepad/note info into hidden inputs on modal show
function populateModal(event) {
    var $listItem = $(event.relatedTarget).closest('li');
    var elementId = $listItem.data('id');
    var elementType = $listItem.data('type');

    $(event.currentTarget).find('input[name="id"]').val(elementId);
    $(event.currentTarget).find('input[name="type"]').val(elementType);

    // Only for edit
    if ($(event.currentTarget).find('input[name="title"]').length) {
        var elementTitle = htmlUnescape($listItem.find('a').html().trim());
        $(event.currentTarget).find('input[name="title"]').val(elementTitle);
    }
}
$(document).on('show.bs.modal', '#modal-edit', populateModal);
$(document).on('show.bs.modal', '#modal-del', populateModal);

// Rename notepad/note (via modal window)
function renameItem(event) {
    var elementId = $('#modal-edit-id').val();
    var elementType = $('#modal-edit-type').val();
    var elementTitle = $('#modal-edit-title').val();

    if (!elementTitle) {
        $('#modal-edit').modal('hide');
        displayFlash('error', 'Error: title cannot be empty');
        return;
    }
    if (elementTitle.length > 80) {
        $('#modal-edit').modal('hide');
        displayFlash('error', 'Title is too long');
        return;
    }

    var url;
    if (elementType == 'notepad') {
        url = baseUrl + '/ajax/notepad/' + elementId;
    } else if (elementType == 'note') {
        url = baseUrl + '/ajax/note/' + elementId;
    }

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'PUT',
        data: {title: elementTitle},
        success: function (response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            $('li[data-type="' + elementType + '"][data-id="' + elementId + '"] > a').html(htmlEscape(elementTitle));
        },
        error: function (response) {
            console.log(response);
            $('#modal-edit').modal('hide');
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}
$(document).on('click', '#modal-edit-submit', renameItem);
$(document).on('keypress', '#modal-edit-title', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        renameItem(event);
    }
});

// Save note's content
$(document).on('click', '.btn-save', function (event) {
    var noteId = $('.sidebar-second li.active').data('id');
    var text = $('#editor').trumbowyg('html');

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: baseUrl + '/ajax/note/' + noteId,
        type: 'PUT',
        data: {text: text},
        success: function (response) {
            console.log(response);
            displayFlash('info', 'Saved successfully');
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
});

// Delete notepad/note (via modal window)
$(document).on('click', '#modal-del-submit', function (event) {
    var elementId = $('#modal-del-id').val();
    var elementType = $('#modal-del-type').val();

    var url;
    if (elementType == 'notepad') {
        url = baseUrl + '/ajax/notepad/' + elementId;
        // If there were opened form for deleted notepad
        var $childFormButton = $('span[data-parent-id="' + elementId + '"]');
    } else if (elementType == 'note') {
        url = baseUrl + '/ajax/note/' + elementId;
    }

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'DELETE',
        success: function (response) {
            console.log(response);
            $('#modal-del').modal('hide');
            // If it was active notepad - hide right panel and disable input
            // Notes deleted automaticaly by Django (cascade delete)
            var $listItem = $('li[data-type="' + elementType + '"][data-id="' + elementId + '"]');
            if ($listItem.hasClass('active')) {
                $('.sidebar-second ul').html('');
                $('.sidebar-second input[name="title"]').prop('disabled', true);
            }
            if (!$listItem.hasClass('child')) {
                // Remove all children one by one
                var nextChild = $listItem.next().hasClass('child');
                while (nextChild) {
                    $listItem.next().remove();
                    nextChild = $listItem.next().hasClass('child');
                }
            }
            $listItem.remove();

            // If there were opened form for deleted notepad
            if ($childFormButton) {
                $childFormButton.closest('form').remove();
            }
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
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
$(document).on('click', '.link-add-child', function () {
    var $listItem = $(this).closest('li');
    var parentId = $listItem.data('id');

    // Check if there already is an additional form
    var $prevForm = $('.sidebar-first > .nav-sidebar > form');
    var prevId;
    if ($prevForm.length) {
        prevId = $prevForm.find('.form-group').data('parent-id');
    } else {
        prevId = null;
    }

    // If it is second click on same element
    // then only hide previous form
    $('.nav-sidebar > form').remove();
    if (parentId != prevId || !prevId) {
        var newForm = makeForm(parentId);
        $(newForm).insertAfter($listItem);
    }
});
