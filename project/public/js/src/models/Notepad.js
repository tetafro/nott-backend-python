define(
    [
        'backbone', 'app',
        'collections/NotesCollection',
        'views/NotesCollectionView'
    ],
    function (
        Backbone, App,
        NotesCollection,
        NotesCollectionView
    ) {
        var Notepad = Backbone.Model.extend({
            defaults: {
                id: null,
                title: null,
                folder_id: null,

                active: false
            },
            // Interface fields, not stored in DB
            dontSync: [
                'active'
            ],
            // To be able to determine what object type is current model
            type: 'notepad',
            idAttribute: 'id',
            urlRoot: '/ajax/notepads/',

            events: {
                'error': 'displayError'
            },

            validate: function (attributes) {
                if (!attributes.title) {
                    return 'Title cannot be empty';
                }
                if (attributes.title.length > 80) {
                    return 'Title is too long';
                }
            },

            displayError: function (model, error) {
                App.AppView.displayError(error);
            },

            open: function () {
                this.collection.setActive(this);
                App.notesCollection.switchNotepad(this);
            },

            // Filter the data to send to the server
            save: function (attrs, options) {
                attrs || (attrs = _.clone(this.attributes));
                options || (options = {});

                attrs = _.omit(attrs, this.dontSync);
                options.data = JSON.stringify(attrs);

                // Proxy the call to the original save function
                return Backbone.Model.prototype.save.call(this, attrs, options);
            }
        });

        return Notepad;
    }
);
