// baseUrl = 'http://nott.tk';
baseUrl = 'http://notes.lily.local';

// ----------------------------------------------
// HELPERS                                      -
// ----------------------------------------------

// Get cookie value by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie) {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
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
    var errorTimeout = 3000;
    var infoTimeout = 500;

    if (status == 'error') {
        $block.find('span').removeClass('label-primary').addClass('label-danger');
        text = text || 'Error';
        timeout = errorTimeout;
    } else if (status == 'info') {
        $block.find('span').removeClass('label-danger').addClass('label-primary');
        text = text || 'Success';
        timeout = infoTimeout;
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
    $('#editor-' + tabId).attr('spellcheck', 'false');

    var saveButton = makeSaveButton();
    $('.trumbowyg-button-pane').append(saveButton);
}

// Get level class (responsible for left padding for
// sidebars' list items)
function getLevel($element) {
    var classString = $element.attr('class');
    var levelPosition = classString.indexOf('lvl-');
    var level = classString.substring(levelPosition+4, levelPosition+5);

    return parseInt(level);
}

// Remove old and set new level class (responsible
// for left padding for sidebars' list items)
function setLevel($element, newLevel) {
    var classString = $element.attr('class');
    var levelPosition = classString.indexOf('lvl-');
    var oldLevel = classString.substring(levelPosition, levelPosition+5);

    $element
        .toggleClass(oldLevel)
        .toggleClass('lvl-'+newLevel);
}

// Sort items by their title
function sortItems($target, type) {
    if (type == 'folder') {
        $notepads = $target.children();
        $notepads.sort(function (a, b) {
            var an = a.getElementsByTagName('span')[0].innerHTML;
            var bn = b.getElementsByTagName('span')[0].innerHTML;

            if (an > bn) {
                return 1;
            } else if (an < bn) {
                return -1;
            } else {
                return 0;
            }
        });

        $notepads.detach().appendTo($target);
    }
}

// ----------------------------------------------
// TEMPLATES                                    -
// ----------------------------------------------

// Template for list item in side panel
// Notice: var level is only for children block
function makeListItem(id, type, title, level) {
    var addChild;
    var childClass;
    var link;
    var childrenBlock;
    if (typeof level == 'undefined') {
        level = 0;
    }

    switch (type) {
        case 'folder':
            link =
                '<a href="#" class="expand" ' +
                'data-toggle="collapse" data-target="#folder-' + id + '" ' +
                'aria-expanded="false">' +
                    '<i class="glyphicon glyphicon-folder-close"></i>' +
                    '<span>' + title + '</span>' +
                '</a>';
            addChild =
                '<span class="link-add">' +
                    '<i class="glyphicon glyphicon-plus text-primary"' +
                    ' data-toggle="modal" data-target="#modal-crud"></i>' +
                '</span>';
            childrenBlock =
                '<ul id="folder-' + id + '" class="nav children-block collapse lvl-' + level + '">' +
                '</ul>';
        break;

        case 'notepad':
            link =
                '<a href="#" class="link-get">' +
                    '<i class="glyphicon glyphicon-paperclip"></i>' +
                    '<span>' + title + '</span>' +
                '</a>';
            addChild = '';
            childrenBlock = '';
        break;

        case 'note':
            link =
                '<a href="#" class="link-get">' +
                    '<i class="glyphicon glyphicon-file"></i>' +
                    '<span>' + title + '</span>' +
                '</a>';
            addChild = '';
            childrenBlock = '';
        break;
    }

    var html =
        '<li ' + 'data-type="' + type + '" data-id="' + id + '">' +
            link +
            addChild +
            '<span class="link-edit">' +
                '<i class="glyphicon glyphicon-pencil text-primary"' +
                ' data-toggle="modal" data-target="#modal-crud"></i>' +
            '</span>' +
            '<span class="link-del">' +
                '<i class="glyphicon glyphicon-remove text-danger"' +
                ' data-toggle="modal" data-target="#modal-crud"></i>' +
            '</span>' +
        '</li>' +
        childrenBlock;

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

// Change icon on folder expand/collapse
$(document).on('click', '.expand', function () {
    $icon = $(this).children().first();
    $icon
        .toggleClass('glyphicon glyphicon-folder-open')
        .toggleClass('glyphicon glyphicon-folder-close');
});

// Close button for flash messages
$(document).on('click', '.flash-close', function () {
    var $block = $('#flash-message');
    $block.fadeOut(300);
});

// Put folder/notepad/note info into hidden inputs on modal show
function populateModal(event) {
    var $listItem = $(event.relatedTarget).closest('li');
    var elementId = $listItem.data('id');
    var elementType = $listItem.data('type');

    var $modalWindow = $('#modal-crud');

    // Folder is default value for radio
    $modalWindow
        .find('input[name="is-folder"][value=1]')
        .prop('checked', true);

    var action;
    var windowTitle;
    var $actionInput = $(event.currentTarget).find('input[name="action"]');
    if ($(event.relatedTarget).hasClass('glyphicon-plus')) {
        action = 'create';
        windowTitle = 'Create new item';
    } else if ($(event.relatedTarget).hasClass('glyphicon-pencil')) {
        action = 'edit';
        windowTitle = 'Edit ' + elementType;
    } else if ($(event.relatedTarget).hasClass('glyphicon-remove')) {
        action = 'delete';
        windowTitle = 'Delete ' + elementType;
    }
    $actionInput.val(action);

    // Change modal window appearance
    $(event.currentTarget).find('h4.modal-title').text(windowTitle);
    changeModalAction(action);

    var elementTitle;
    if (action == 'create') {
        elementTitle = '';
    } else if (action == 'edit' || action == 'delete') {
        elementTitle = htmlUnescape($listItem.find('a > span').html().trim());
    }

    $(event.currentTarget).find('input[name="id"]').val(elementId);
    $(event.currentTarget).find('input[name="type"]').val(elementType);

    if (action == 'create' || action == 'edit') {
        // Insert title (empty for creation)
        $(event.currentTarget).find('input[name="title"]').val(elementTitle);

        // Reload the list of folders
        var $selectParent = $(event.currentTarget).find('select[name="move"]');

        // Clear list from previous call
        $selectParent.html('');

        var selected;
        var level;
        var ident;
        var parentId;

        if (elementType == 'folder' || elementType == 'notepad') {
            // Empty option for the root folders
            $selectParent.append($('<option></option>'));

            var $allFolders = $('.sidebar-first li[data-type="folder"]');

            // If it is not one of the root folders, get ID without prefix "folder-"
            if (action == 'create') {
                parentId = $listItem.data('id');
            } else if (action != 'create' && $listItem.parent().hasClass('children-block')) {
                parentId = parseInt($listItem.parent().attr('id').substr(7));
            } else {
                parentId = null;
            }

            // List of all folders in <select>
            $allFolders.each(function(index) {
                if (parentId && $(this).data('id') == parentId) {
                    selected = true;
                } else {
                    selected = false;
                }

                level = getLevel($('ul#folder-' + $(this).data('id')));
                ident = '';
                for (var i = 0; i < level; i++) {
                    ident += '--';
                };

                $selectParent.append(
                    $('<option></option>')
                        .attr('value', $(this).data('id'))
                        .text(ident + ' ' + $(this).find('a > span').text())
                        .prop('selected', selected)
                );
            });
        } else if (elementType == 'note') {
            var $currentNotepad = $('.sidebar-first li[data-type="notepad"].active');
            var $notepads = $currentNotepad.siblings().addBack(); // siblings and itself
            parentId = $currentNotepad.data('id');

            // List of notepads from the same folders in <select>
            $notepads.each(function (index) {
                if (parentId && $(this).data('id') == parentId) {
                    selected = true;
                } else {
                    selected = false;
                }

                $selectParent.append(
                    $('<option></option>')
                        .attr('value', $(this).data('id'))
                        .text($(this).find('a > span').text())
                        .prop('selected', selected)
                );
            });
        }

    } else if (action == 'delete') {
        $(event.currentTarget).find('.block-delete > strong').html(elementTitle);
    }
}
$(document).on('show.bs.modal', '#modal-crud', populateModal);

// Change madal window appearance according to it's action
function changeModalAction(action) {
    var $modalWindow = $('#modal-crud');

    var $blockCreateEdit = $modalWindow.find('.block-create-edit');
    var $blockDelete = $modalWindow.find('.block-delete');

    var $blockRadio = $blockCreateEdit.find('.radio-type');

    var $buttonSave = $modalWindow.find('button[name="save"]');
    var $buttonDelete = $modalWindow.find('button[name="delete"]');

    switch (action) {
        case 'create':
            $blockDelete.hide();
            $blockCreateEdit.show();
            $blockRadio.show();
            $buttonSave.show();
            $buttonDelete.hide();
        break;

        case 'edit':
            $blockDelete.hide();
            $blockCreateEdit.show();
            $blockRadio.hide();
            $buttonSave.show();
            $buttonDelete.hide();
        break;

        case 'delete':
            $blockDelete.show();
            $blockCreateEdit.hide();
            $buttonSave.hide();
            $buttonDelete.show();
        break;
    }
}

// Change hidden field of the modal according to radio
// Notice: radio don't used directly, because there is no radio for
// type 'note', but we want to have one common determine to detect type
$(document).on('change', '#modal-crud input[name="is-folder"]', function () {
    if ($(this).val() == '1') {
        $('#modal-crud input[name="type"]').val('folder');
    } else {
        $('#modal-crud input[name="type"]').val('notepad');
    }
});

// Close note's tab
// This function is separate because used several times
function closeEditorTab(id) {
    var $tabHead = $('#editor-block li[data-id="' + id + '"]');
    var $tab = $('#tab-' + id);

    // Closing active tab
    if ($tabHead.hasClass('active')) {
        // Make first tab active
        if ($tabHead.siblings().length > 0) {
            $tabHead.siblings().first().addClass('active');
            $tab.siblings().first().addClass('active');
        }
    }

    // Destroy editor and remove tab
    $('#editor-' + id).trumbowyg('destroy');
    $tabHead.remove();
    $tab.remove();
}
$(document).on('click', '.tab-close', function () {
    var id = $(this).closest('li').data('id');
    closeEditorTab(id);
});

// ----------------------------------------------
// CRUD: FOLDERS                                -
// ----------------------------------------------

function folderCreate(title, parentId) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/folder/';
    var data = {title: title}
    if (parentId) {
        data.parent = parentId;
    }

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
            var id = response.id;
            var listItem;

            if (parentId) {
                var $parent = $('.sidebar-first ul li[data-id="' + parentId + '"]');
                var parentLevel = getLevel($('ul#folder-'+parentId));
                listItem = makeListItem(id, 'folder', title, parentLevel+1);
                // Append to children-block
                $parent.next().append(listItem);
            } else {
                listItem = makeListItem(id, 'folder', title);
                $('.sidebar-first > ul').append(listItem);
            }
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function folderEdit(id, parentId, title) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/folder/' + id;
    var data = {title: title};
    if (parentId) {
        data.parent = parentId;
    }

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'PUT',
        data: data,
        success: function (response) {
            // Rename
            var $listItem = $('li' +
                '[data-type="folder"]' +
                '[data-id="' + id + '"]');
            $listItem.find('a > span').html(htmlEscape(title));

            // Move
            if (parentId) {
                $listItem.appendTo('ul#folder-'+parentId);

                $childrenBlock = $('ul#folder-'+id);

                var parentLevel = getLevel($('ul#folder-'+parentId));
                setLevel($childrenBlock, parentLevel+1);

                $childrenBlock.appendTo('ul#folder-'+parentId);
            }
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function folderDelete(id) {
    var url = baseUrl + '/ajax/folder/' + id;

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'DELETE',
        success: function (response) {
            var $listItem = $('li' +
                '[data-type="folder"]' +
                '[data-id="' + id + '"]');

            // Delete children block
            if ($listItem.next().hasClass('children-block')) {
                $listItem.next().remove();
            }
            $listItem.remove();
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

// Calls function with folder depending on action variable
function folderCrud(action, id, parentId, title) {
    switch (action) {
        case 'create':
            folderCreate(title, parentId);
        break;
        case 'edit':
            folderEdit(id, parentId, title);
        break;
        case 'delete':
            folderDelete(id);
        break;
    }
}

// ----------------------------------------------
// CRUD: NOTEPADS                               -
// ----------------------------------------------

function notepadCreate(title, folderId) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/notepad/';
    var data = {title: title, folder: folderId};

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
            var id = response.id;
            title = htmlEscape(title);

            // Create notepad in sidebar
            var listItem = makeListItem(id, 'notepad', title);
            $('ul#folder-'+folderId).append(listItem);

            // Open created notepad
            var $listItem = $('.sidebar-first li[data-id="' + id + '"]');
            $('.sidebar-first li').removeClass('active');
            $listItem.addClass('active');
            $('#sidebar-second-title').html(title);
            $('.sidebar-second ul').html('');
            $('.sidebar-second form').remove(); // maybe this is a search form
            var form = makeNewNoteForm();
            $(form).insertAfter($('.sidebar-second .nav-sidebar'));
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function notepadRead(id) {
    $('.btn-save').prop('disabled', true);

    var $listItem = $('li' +
        '[data-type="notepad"]' +
        '[data-id="' + id + '"]');
    var url = baseUrl + '/ajax/notepad/' + id;

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            // Interface changes: mark active, set title on second
            // sidebar, remove search form if exists
            $('.sidebar-first li[data-type="notepad"]').removeClass('active');
            $listItem.addClass('active');
            $('#sidebar-second-title').html($listItem.find('a > span').html().trim());
            $('.sidebar-second form').remove(); // maybe this is a search form
            var form = makeNewNoteForm();
            $(form).insertAfter($('.sidebar-second .nav-sidebar'));

            // Notes list
            var itemsList = '';
            $.each(response.notes, function (index, note) {
                itemsList += makeListItem(note.id, 'note', note.title);
            });
            $('.sidebar-second ul').html(itemsList);
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function notepadEdit(id, folderId, title) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/notepad/' + id;
    var data = {title: title};
    if (folderId) {
        data.folder = folderId;
    }

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'PUT',
        data: data,
        success: function (response) {
            // Rename
            var $listItem = $('li' +
                '[data-type="notepad"]' +
                '[data-id="' + id + '"]');
            $listItem.find('a > span').html(htmlEscape(title));
            // If notepad is opened then change title of the second sidebar
            if ($listItem.hasClass('active')) {
                $('#sidebar-second-title').text(htmlEscape(title));
            }

            // Move
            if (folderId) {
                $listItem.appendTo('ul#folder-' + folderId);
                sortItems($('ul#folder-' + folderId), 'folder');
            }
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function notepadDelete(id) {
    var url = baseUrl + '/ajax/notepad/' + id;

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'DELETE',
        success: function (response) {
            var $listItem = $('li' +
                '[data-type="notepad"]' +
                '[data-id="' + id + '"]');
            $listItem.remove();
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

// Calls function with notepad depending on action variable
function notepadCrud(action, id, folderId, title) {
    switch (action) {
        case 'create':
            notepadCreate(title, folderId);
        break;
        case 'read':
            notepadRead(id);
        break;
        case 'edit':
            notepadEdit(id, folderId, title);
        break;
        case 'delete':
            notepadDelete(id);
        break;
    }
}

// ----------------------------------------------
// CRUD: NOTES                                  -
// ----------------------------------------------

function noteCreate(title, notepadId) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/note/';
    var data = {title: title, id: notepadId};

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
            var noteId = response.id;
            title = htmlEscape(title);

            var newListItemHtml = makeListItem(noteId, 'note', title);
            $('.sidebar-second ul').append(newListItemHtml);

            // Open created element

            // Unhide editor block
            $('#editor-block').css({visibility: 'visible'});
            $('.btn-save').prop('disabled', false);

            // Make new tab
            var newTabHead = makeTabHead(noteId);
            var newTab = makeTab(noteId);
            var $newListItem = $('.sidebar-second li[data-id="' + noteId + '"]');
            $newListItem.siblings().removeClass('active');
            $newListItem.addClass('active');

            // Append new tab
            $('#editor-block > .nav-tabs > li').removeClass('active');
            $('#editor-block > .tab-content > .tab-pane').removeClass('active');
            $('#editor-block > .nav-tabs').append(newTabHead);
            $('#editor-block > .tab-content').append(newTab);
            $('#editor-block > .nav-tabs > .active > a').html(title +
                 '<div class="tab-close">&times;</div>');

            // Make editor for the tab
            newEditor(noteId);

            // Need to clear editor explicitly
            $('#editor-' + noteId).trumbowyg('empty');

        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function noteRead(id) {
    // Unhide editor block
    $('#editor-block').css({visibility: 'visible'});
    $('.btn-save').prop('disabled', false);

    var $listItem = $('li' +
        '[data-type="note"]' +
        '[data-id="' + id + '"]');
    var title = $listItem.find('a > span').html().trim();
    var url = baseUrl + '/ajax/note/' + id;

    $listItem.siblings().removeClass('active');
    $listItem.addClass('active');

    // If tab for selected note is already exist
    if ($('#tab-' + id).length > 0) {
        // Activate tab
        $('#editor-block > .nav-tabs > li').removeClass('active');
        $('#editor-block > .tab-content > .tab-pane').removeClass('active');
        $('#editor-block > .nav-tabs > li[data-id="' + id + '"]').addClass('active');
        $('#tab-' + id).addClass('active');

        return;
    }

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            // Make new tab
            var newTabHead = makeTabHead(id);
            var newTab = makeTab(id);

            // Append new tab
            $('#editor-block > .nav-tabs > li').removeClass('active');
            $('#editor-block > .tab-content > .tab-pane').removeClass('active');
            $('#editor-block > .nav-tabs').append(newTabHead);
            $('#editor-block > .tab-content').append(newTab);
            $('#editor-block > .nav-tabs > .active > a')
                .html(title + '<div class="tab-close">&times;</div>');

            // Make editor for the tab
            newEditor(id);

            // Need to clear editor explicitly if response text is empty string
            $('#editor-' + id).trumbowyg('empty');
            $('#editor-' + id).trumbowyg('html', response.text);
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function noteEdit(id, notepadId, title) {
    if (!title) {
        displayFlash('error', 'Title cannot be empty');
        return;
    } else if (title.length > 80) {
        displayFlash('error', 'Title is too long');
        return;
    }

    var url = baseUrl + '/ajax/note/' + id;
    var data = {title: title};
    if (notepadId) {
        data.notepad = notepadId;
    }

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'PUT',
        data: data,
        success: function (response) {
            // Rename
            var $listItem = $('li' +
                '[data-type="note"]' +
                '[data-id="' + id + '"]');
            $listItem.find('a > span').html(htmlEscape(title));
            // If it is opened, rename it's tab
            if ($('#tab-' + id).length > 0) {
                $('.nav-tabs > li > a[href="#tab-' + id + '"]')
                    .html(htmlEscape(title) + '<div class="tab-close">&times;</div>');
            }

            // Move
            var currentNotepadId = $('.sidebar-first li[data-type="notepad"].active').data('id');
            if (notepadId != currentNotepadId) {
                $listItem.remove();
            }
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function noteSave(id) {
    var text = $('#editor-' + id).trumbowyg('html');

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: baseUrl + '/ajax/note/' + id,
        type: 'PUT',
        data: {text: text},
        success: function (response) {
            displayFlash('info', 'Saved successfully');
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

function noteDelete(id) {
    var url = baseUrl + '/ajax/note/' + id;

    $.ajax({
        beforeSend: function (response, settings) {
            csrftoken = getCookie('csrftoken');
            response.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: url,
        type: 'DELETE',
        success: function (response) {
            var $listItem = $('li' +
                '[data-type="note"]' +
                '[data-id="' + id + '"]');
            $listItem.remove();

            // If it was opened note then close it's tab
            if ($('#tab-' + id).length > 0) {
                closeEditorTab(id);
            }
        },
        error: function (response) {
            var errorMessage = $.parseJSON(response.responseText).error;
            displayFlash('error', errorMessage);
        }
    });
}

// Calls function with notepad depending on action variable
function noteCrud(action, id, notepadId, title) {
    switch (action) {
        case 'create':
            noteCreate(title, notepadId);
        break;
        case 'read':
            noteRead(id);
        break;
        case 'edit':
            noteEdit(id, notepadId, title);
        break;
        case 'save':
            noteSave(id);
        break;
        case 'delete':
            noteDelete(id);
        break;
    }
}

// ----------------------------------------------
// CRUD CALLS                                   -
// ----------------------------------------------

// Create root folder
$(document).on('click', '.sidebar-first form .link-add', function (event) {
    var $form = $(this).closest('form');
    var title = $form.find('input').val();
    folderCrud('create', null, null, title);

    // Clear input
    $('.sidebar-first form').find('input').val('');
});
$(document).on('keypress', '.sidebar-first form input[name="title"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        var $form = $(this).closest('form');
        var title = $form.find('input').val();
        folderCrud('create', null, null, title);

        // Clear input
        $('.sidebar-first form').find('input').val('');
    }
});

// Create subfolder/notepad
// Update folder/notepad/note
// Delete folder/notepad/note
function performCrud() {
    var $modalContent = $('#modal-crud .modal-body');

    var action = $modalContent.find('input[name="action"]').val();
    var elementId = $modalContent.find('input[name="id"]').val();
    var parentId = $modalContent.find('select[name="move"]').val() || null;
    var elementTitle = $modalContent.find('input[name="title"]').val();
    var elementType = $modalContent.find('input[name="type"]').val();

    if (elementType == 'folder') {
        folderCrud(action, elementId, parentId, elementTitle);
    } else if (elementType == 'notepad') {
        notepadCrud(action, elementId, parentId, elementTitle);
    } else if (elementType == 'note') {
        noteCrud(action, elementId, parentId, elementTitle);
    }

    // Hide modal window
    $('#modal-crud').modal('hide');
}
$(document).on('click', '#modal-crud [name="save"]', function (event) {
    performCrud();
});
$(document).on('keypress', '#modal-crud [name="title"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        performCrud();
    }
});
$(document).on('click', '#modal-crud [name="delete"]', function (event) {
    performCrud();
});

// Read notepad's content (list of notes)
$(document).on('click', '.sidebar-first .link-get', function (event) {
    var id = $(this).closest('li').data('id');
    notepadCrud('read', id);
});

// Create note
$(document).on('click', '.sidebar-second .link-add', function (event) {
    var $form = $(this).closest('form');
    var title = $form.find('input').val();
    var notepadId = $('.sidebar-first li[data-type="notepad"].active').data('id');

    noteCrud('create', null, notepadId, title);

    // Clear input
    $('.sidebar-second form').find('input').val('');
});
$(document).on('keypress', '.sidebar-second input[name="title"]', function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();

        var $form = $(this).closest('form');
        var title = $form.find('input').val();
        var notepadId = $('.sidebar-first li[data-type="notepad"].active').data('id');

        noteCrud('create', null, notepadId, title);

        // Clear input
        $('.sidebar-second form').find('input').val('');
    }
});

// Read note
$(document).on('click', '.sidebar-second .link-get', function (event) {
    var id = $(this).closest('li').data('id');
    noteCrud('read', id);
});

// Save note's content
$(document).on('click', '.btn-save', function (event) {
    var id = $('#editor-block li.active').data('id');
    noteCrud('save', id);
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
            $('.sidebar-first li').removeClass('active');
            var itemsList = '';
            $.each(response.notes, function (index, note) {
                itemsList += makeListItem(note.id, 'note', note.title);
            });
            $('.sidebar-second ul').html(itemsList);
        },
        error: function (response) {
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
