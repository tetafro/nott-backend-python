define(
    [
        'underscore', 'backbone', 'app',
        'views/EditorHeadView', 'views/EditorContentView'
    ],
    function (
        _, Backbone, App,
        EditorHeadView, EditorContentView
    ) {
        var Note = Backbone.Model.extend({
            defaults: {
                id: null,
                title: null,
                text: null,
                notepad_id: null,

                opened: false, // tab is opened,
                               // need for view to fire close event
                active: false // tab is active
            },
            // Interface fields, not stored in DB
            dontSync: [
                'opened',
                'active'
            ],
            // To be able to determine what object type is current model
            type: 'note',
            idAttribute: 'id',
            urlRoot: '/ajax/notes/',

            validate: function (attributes) {
                if (!attributes.title) {
                    return 'Title cannot be empty';
                }
                if (attributes.title.length > 80) {
                    return 'Title is too long';
                }
            },

            // Load from server or activate if already loaded
            open: function () {
                var that = this;

                // Model is already opened - make it's tab active
                if (that.get('opened')) {
                    App.editorsCollection.openOne(that);
                // Fetch model and open it in new tab
                } else {
                    that.fetch({
                        success: function () {
                            App.editorsCollection.openOne(that);
                        }
                    });
                }
            },

            close: function () {
                if (!this.get('opened')) { return; }
                App.editorsCollection.closeOne(this);
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

        return Note;
    }
);
