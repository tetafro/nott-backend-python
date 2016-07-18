define(
    [
        'backbone',
        'app'
    ],
    function (
        Backbone,
        App
    ) {
        var Folder = Backbone.Model.extend({
            defaults: {
                id: null,
                title: null,
                parent_id: null
            },
            // To be able to determine what object type is current model
            type: 'folder',
            idAttribute: 'id',
            urlRoot: '/ajax/folders/',

            initialize: function () {
            },

            validate: function (attributes) {
                if (!attributes.title) {
                    return 'Title cannot be empty';
                }
                if (attributes.title.length > 80) {
                    return 'Title is too long';
                }
            }
        });

        return Folder;
    }
);
