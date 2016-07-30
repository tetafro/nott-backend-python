define(
    [],
    function () {
        var NoteTemplate = `
            <div class="item">
                <a href="#">
                    <i class="glyphicon glyphicon-file"></i><span><%= title %></span>
                </a>
                <span class="edit">
                    <i class="glyphicon glyphicon-pencil"></i>
                </span>
                <span class="del">
                    <i class="glyphicon glyphicon-remove text-danger"></i>
                </span>
            </div>
        `;

        return NoteTemplate;
    }
);