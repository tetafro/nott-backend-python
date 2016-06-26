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
                var that = this;

                // Make active first of remaining opened notes
                if (note.get('active') && that.length > 1) {
                    var newActiveNote = (that.at(0).get('id') == note.get('id')) ?
                        that.at(1) : that.at(0);
                    that.openOne(newActiveNote);
                }

                // Remove from opened and set unactive
                that.remove(note);
                note.set({active: false, opened: false});
            }
        });

        return EditorsCollection;
    }
);