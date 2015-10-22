// var baseUrl = 'http://nott.tk';
var baseUrl = 'http://notes.lily.local';

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
    var timeout;
    if (status == 'error') {
        $block.find('span').removeClass('label-primary').addClass('label-danger');
        text = text || 'Error';
        timeout = 3000;
    } else if (status == 'info') {
        $block.find('span').removeClass('label-danger').addClass('label-primary');
        text = text || 'Success';
        timeout = 500;
    }
    $block.find('span').html(text);

    // Hide automatically
    // There also is a function below for closing on button press
    $block.fadeIn(300);
    setTimeout(function () {
        $block.fadeOut(300);
    }, timeout);
}

// Initialize WYSIWYG editor on specified tab
function newEditor(tabId) {
    // Load WYSIWYG editor
    $('#editor-' + tabId).trumbowyg({
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
}

// ----------------------------------------------
// TEMPLATES                                    -
// ----------------------------------------------

// Template for list item in side panel
function makeListItem(id, type, title, isChild) {
    var addChild;
    var childClass;
    if (type == 'notepad') {
        if (isChild) {
            addChild = '';
        } else {
            addChild =
                '<span class="link-add-child">' +
                    '<i class="glyphicon glyphicon-plus text-primary"></i>' +
                '</span>';
        }
    } else {
        addChild = '';
    }

    var html =
        '<li ' + 'data-type="' + type + '" data-id="' + id + '">' +
            '<a href="#" class="link-get">' +
                title +
            '</a>' +
            addChild +
            '<span class="link-edit">' +
                '<i class="glyphicon glyphicon-pencil text-primary"' +
                ' data-toggle="modal" data-target="#modal-edit"></i>' +
            '</span>' +
            '<span class="link-del">' +
                '<i class="glyphicon glyphicon-remove text-danger"' +
                ' data-toggle="modal" data-target="#modal-del"></i>' +
            '</span>' +
        '</li>';

    return html;
}

// Template for input form for child notepad creation
function makeForm(id) {
    var html =
        '<form>' +
            '<div class="form-group" data-type="notepad" data-parent-id="' + id + '">' +
                '<input type="text" name="title" class="form-control input-sm" placeholder="New notepad">' +
                '<span class="link-add">' +
                    '<i class="glyphicon glyphicon-plus text-primary"></i>' +
                '</span>' +
            '</div>' +
        '</form>';

    return html;
}

// Template for expand arrow
function makeExpandArrow(id) {
    var html =
        '<span class="expand" data-toggle="collapse" data-target="#children-' + id + '" aria-expanded="true">' +
            '<i class="glyphicon text-primary glyphicon-triangle-bottom"></i>' +
        '</span>';

    return html;
}

// Template for save button on editor's panel
function makeSaveButton() {
    var html =
        '<button type="button" class="btn btn-sm btn-primary btn-save" title="Save">' +
            '<i class="glyphicon glyphicon-ok"></i>' +
        '</button>';

    return html;
}

// Template for tab header for editor area
// (new tab is always active)
function makeTabHead(tabId) {
    var html =
        '<li class="active" data-id=' + tabId + '>' +
            '<a href="#tab-' + tabId + '" role="tab" data-toggle="tab"></a>' +
        '</li>';

    return html;
}

// Template for tab content for editor area
// (new tab is always active)
function makeTab(tabId) {
    var html =
        '<div role="tabpanel" class="tab-pane active" id="tab-' + tabId + '">' +
            '<div id="editor-' + tabId + '" class="editor"></div>' +
        '</div>';

    return html;
}

// Template for new note form
function makeNewNoteForm() {
    var html =
        '<form>' +
            '<div class="form-group" data-type="note">' +
                '<input type="text" name="title" class="form-control input-sm"' +
                    ' placeholder="New note" autocomplete="off">' +
                '<span class="link-add" data-type="note">' +
                    '<i class="glyphicon glyphicon-plus text-primary"></i>' +
                '</span>' +
            '</div>' +
        '</form>';

    return html;
}

// Template for search form
function makeSearchForm() {
    var html =
        '<form>' +
            '<div class="form-group">' +
                '<input type="text" name="search" class="form-control input-sm"' +
                    ' placeholder="Search" autocomplete="off">' +
                '<span class="search">' +
                    '<i class="glyphicon glyphicon-search text-primary"></i>' +
                '</span>' +
            '</div>' +
        '</form>';

    return html;
}

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
            var elementId = response.id;
            elementTitle = htmlEscape(elementTitle);

            if (parentId) {
                newElement = makeListItem(elementId, elementType, elementTitle, true);
                $('.nav-sidebar > form').remove();
                $parent = $(sideBar + ' ul li[data-id="' + parentId + '"]');
                // Children block existed before
                if ($parent.next().hasClass('children-block')) {
                    $($parent.next()).append(newElement);
                // Create expandable children block and arrow button
                } else {
                    newElement = '<ul id="children-' + parentId +
                        '" class="nav children-block collapse in" aria-expanded="true">' +
                        newElement +
                        '</ul>';
                    $(newElement).insertAfter($parent);
                    var arrow = makeExpandArrow(parentId);
                    $(arrow).insertAfter($parent.find('.link-get'));
                }
            } else {
                newElement = makeListItem(elementId, elementType, elementTitle, false);
                $(sideBar + ' ul').append(newElement);
            }
            $form.find('input').val('');

            // Open created element
            var $newElement;
            if (elementType == 'notepad') {
                $newElement = $('.sidebar-first li[data-id="' + elementId + '"]');
                $('.sidebar-first li').removeClass('active');
                $newElement.addClass('active');
                $('#sidebar-second-title').html(elementTitle);
                $('.sidebar-second ul').html('');
                $('.sidebar-second form').remove(); // maybe this is a search form
                var form = makeNewNoteForm();
                $(form).insertAfter($('.sidebar-second .nav-sidebar'));
            } else if (elementType == 'note') {
                // Unhide editor block
                $('#editor-block').css({visibility: 'visible'});
                $('.btn-save').prop('disabled', false);

                // Make new tab
                var newTabHead = makeTabHead(elementId);
                var newTab = makeTab(elementId);
                var $newElement = $('.sidebar-second li[data-id="' + elementId + '"]');
                $newElement.siblings().removeClass('active');
                $newElement.addClass('active');

                // Append new tab
                $('#editor-block > .nav-tabs > li').removeClass('active');
                $('#editor-block > .tab-content > .tab-pane').removeClass('active');
                $('#editor-block > .nav-tabs').append(newTabHead);
                $('#editor-block > .tab-content').append(newTab);
                $('#editor-block > .nav-tabs > .active > a').html(elementTitle +
                     '<div class="tab-close">&times;</div>');

                // Make editor for the tab
                newEditor(elementId);

                // Need to clear editor explicitly
                $('#editor-' + elementId).trumbowyg('empty');
            }

        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}
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

            // Interface changes: mark active,
            $('.sidebar-first li').removeClass('active');
            $listItem.addClass('active');
            $('#sidebar-second-title').html($listItem.find('a').html());
            $('.sidebar-second form').remove(); // maybe this is a search form
            var form = makeNewNoteForm();
            $(form).insertAfter($('.sidebar-second .nav-sidebar'));

            // Notes list
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
    // Unhide editor block
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
    if ($('#tab-' + elementId).length > 0) {
        // Activate tab
        $('#editor-block > .nav-tabs > li').removeClass('active');
        $('#editor-block > .tab-content > .tab-pane').removeClass('active');
        $('#editor-block > .nav-tabs > li[data-id="' + elementId + '"]').addClass('active');
        $('#tab-' + elementId).addClass('active');

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
            $('#editor-' + elementId).trumbowyg('empty');
            $('#editor-' + elementId).trumbowyg('html', response.text);
        },
        error: function (response) {
            console.log(response);
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
});

// Close note's tab
$(document).on('click', '.tab-close', function (event) {
    var $tabHead = $(this).closest('li');
    var elementId = $tabHead.data('id');
    var $tab = $('#tab-' + elementId);

    // Closing active tab
    if ($tabHead.hasClass('active')) {
        // Make first tab active
        if ($tabHead.siblings().length > 0) {
            $tabHead.siblings().first().addClass('active');
            $tab.siblings().first().addClass('active');
        }
    }
    // Destroy editor and remove tab
    $('#editor-' + elementId).trumbowyg('destroy');
    $tabHead.remove();
    $tab.remove();
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
            $('#modal-edit').modal('hide');
        },
        url: url,
        type: 'PUT',
        data: {title: elementTitle},
        success: function (response) {
            console.log(response);
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
    var noteId = $('#editor-block li.active').data('id');
    var text = $('#editor-' + noteId).trumbowyg('html');

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
            $('#modal-del').modal('hide');
        },
        url: url,
        type: 'DELETE',
        success: function (response) {
            console.log(response);

            // If there were opened form for deleted notepad
            if ($childFormButton) {
                $childFormButton.closest('form').remove();
            }

            // If it was active notepad - hide right panel and remove input
            // Notes deleted automaticaly by Django (cascade delete)
            var $listItem = $(
                'li' +
                '[data-type="' + elementType + '"]' +
                '[data-id="' + elementId + '"]'
            );
            if ($listItem.hasClass('active') && elementType == 'notepad') {
                $('.sidebar-second ul').html('');
                $('.sidebar-second form').remove();
            }

            // If was parent than remove it with it's children-block
            if (!$listItem.parent().hasClass('children-block')) {
                if ($listItem.next().hasClass('children-block')) {
                    $listItem.next().remove();
                }
                $listItem.remove();
            // If it was last child than delete children block and expand arrow
            } else if (!$listItem.siblings().length) {
                $listItem.parent().prev().find('.expand').remove();
                $listItem.parent().remove();
            } else {
                $listItem.remove();
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
// SEARCH                                       -
// ----------------------------------------------

// Show search form
$(document).on('click', '#show-search', function (event) {
    // Switch to search
    $('#sidebar-second-title').html('Search');
    $('.sidebar-second .nav-sidebar').html('');
    $('.sidebar-second form').remove();

    // Add searching form
    var form = makeSearchForm();
    $(form).insertAfter($('.sidebar-second .nav-sidebar'));
});

// Find notes by text and display list in the second sidebar
function searchNotes($form) {
    var text = $form.find('input').val();
    var url = baseUrl + '/ajax/search/';

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        data: {text: text},
        success: function (response) {
            console.log(response);
            $('.sidebar-first li').removeClass('active');
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
}
// Search on clicking icon or on pressing enter key
$(document).on('click', '.sidebar-second .search', function (event) {
    searchNotes($(this).closest('form'));
});
$(document).on('keypress', '.sidebar-second input[name="search"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        searchNotes($(this).closest('form'));
    }
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

// Change icon for expand/collapse children notepads
$(document).on('click', '.expand', function () {
    $icon = $(this).children().first();
    $icon
        .toggleClass('glyphicon-triangle-bottom')
        .toggleClass('glyphicon-triangle-right');
});

// Close button for flash messages
$(document).on('click', '.flash-close', function () {
    var $block = $('#flash-message');
    $block.fadeOut(300);
});
