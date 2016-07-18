define(
    [],
    function () {
        var FolderTemplate = `
            <div class="item expand">
                <a href="#">
                    <i class="glyphicon glyphicon-folder-close"></i><span><%= title %></span>
                </a>
                <span class="add">
                    <i class="glyphicon glyphicon-plus text-primary"></i>
                </span>
                <span class="edit">
                    <i class="glyphicon glyphicon-pencil text-primary"></i>
                </span>
                <span class="del">
                    <i class="glyphicon glyphicon-remove text-danger"></i>
                </span>
            </div>

            <ul id="folder-<%= id %>" class="nav children-block collapse">
        `;

        return FolderTemplate;
    }
);