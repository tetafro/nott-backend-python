module.exports = `
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">&times;</span>
                </button>
                <h4 class="modal-title"><%= windowTitle %></h4>
            </div>

            <div class="modal-body">
                <div class="block-delete" <% if (action != 'delete') print('style="display:none;"') %>>
                    Are you shure you want to delete <strong><%= elementTitle %></strong>?
                </div>

                <div class="block-create-edit" <% if (action != 'create' && action != 'edit') print('style="display:none;"') %>>
                    <input name="title" type="text" class="form-control" autocomplete="off" value="<%= elementTitle %>">
                    <select name="move" class="form-control">
                        <%= elementsList %>
                    </select>

                    <div class="radio-type" <% if (elementType == 'note' || action != 'create') print('style="display:none;"') %>>
                        <label class="radio-inline">
                            <input
                                type="radio"
                                name="type"
                                value="folder"
                                <% if (elementType == 'folder') print('checked') %>
                            > Folder
                        </label>
                        <label class="radio-inline">
                            <input
                                type="radio"
                                name="type"
                                value="notepad"
                                <% if (elementType == 'notepad') print('checked') %>
                            > Notepad
                        </label>
                        <label class="radio-inline" <% if (elementType != 'note') print('style="display:none;"') %>>
                            <input
                                type="radio"
                                name="type"
                                value="note"
                                <% if (elementType == 'note') print('checked') %>
                            > Note
                        </label>
                    </div>
                </div>

                <div class="error-message text-danger"></div>
            </div>

            <div class="modal-footer">
                <button
                    name="save"
                    type="button"
                    class="btn btn-primary"
                    <% if (action != 'create' && action != 'edit') print('style="display:none;"') %>
                >Save</button>
                <button
                    name="delete"
                    type="button"
                    class="btn btn-danger"
                    <% if (action != 'delete') print('style="display:none;"') %>
                >Delete</button>
                <button name="cancel" type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
            </div>
        </div>
    </div>
`;
