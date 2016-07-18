define(
    [],
    function () {
        var NotepadTemplate = `
            <div class="item">
                <a href="#">
                    <i class="glyphicon glyphicon-paperclip"></i><span><%= title %></span>
                </a>
                <span class="edit">
                    <i class="glyphicon glyphicon-pencil text-primary"></i>
                </span>
                <span class="del">
                    <i class="glyphicon glyphicon-remove text-danger"></i>
                </span>
            </div>
        `;

        return NotepadTemplate;
    }
);