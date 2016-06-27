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
                // Remove from opened and set unactive
                this.remove(note);

                // Make active first of remaining opened notes
                if (this.length && note.get('active')) {
                    this.at(0).set('active', true);
                }

                note.set({active: false, opened: false});
            }
        });

        return EditorsCollection;
    }
);