define(
    [],
    function () {
        var EditorContentTemplate = `
            <div id="editor-<%= id %>" class="editor">
                <div class="editor-panel">
                    <button type="button" class="btn btn-sm btn-primary">
                        View
                    </button>
                    <button type="button" class="btn btn-sm btn-primary">
                        Edit
                    </button>
                    <button type="button" class="btn btn-sm btn-primary btn-save">
                        Save
                    </button>
                </div>
                <textarea spellcheck="false"><%= text %></textarea>
            </div>
        `;

        return EditorContentTemplate;
    }
);
