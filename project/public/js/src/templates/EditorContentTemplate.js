define(
    [],
    function () {
        var EditorContentTemplate = `
            <div id="editor-<%= id %>" class="editor">
                <ul class="nav nav-pills editor-panel">
                    <li class="active">
                        <a data-toggle="pill" href="#editor-<%= id %>-view">
                            View
                        </a>
                    </li>
                    <li>
                        <a data-toggle="pill" href="#editor-<%= id %>-edit">
                            Edit
                        </a>
                    </li>
                    <button type="button" class="btn btn-sm btn-primary btn-save">
                        Save
                    </button>
                </ul>
                <div class="tab-content">
                    <div role="tabpanel" id="editor-<%= id %>-view" class="tab-pane active">
                        <div class="editor-content">RENDERED VIEW</div>
                    </div>
                    <div role="tabpanel" id="editor-<%= id %>-edit" class="tab-pane">
                        <textarea class="editor-content" spellcheck="false"><%= text %></textarea>
                    </div>
                </div>
            </div>
        `;

        return EditorContentTemplate;
    }
);
