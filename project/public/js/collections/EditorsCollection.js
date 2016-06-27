define(
    [
        'backbone',
        'app',
        'models/Note'
    ],
    function (
        Backbone,
        App,
        Note
    ) {
        var EditorsCollection = Backbone.Collection.extend({
            model: Note,

            initialize: function () {
                this.listenTo(this, 'remove', this.onRemove);
            },

            // This fires when tab is closed and when model is destroyed
            onRemove: function (note) {
                // Make active first of remaining opened notes
                if (this.length && note.get('active')) {
                    this.at(0).set('active', true);
                }

                note.set({active: false, opened: false});
            },

            openOne: function(note) {
                var eachNote;
                this.each(function (eachNote) {
                    eachNote.set('active', false);
                });
                note.set({active: true, opened: true});

                if (!this.contains(note)) {
                    App.editorsCollection.add(note);
                }
            },

            closeOne: function(note) {
                // Remove from opened
                this.remove(note);
            }
        });

        return EditorsCollection;
    }
);