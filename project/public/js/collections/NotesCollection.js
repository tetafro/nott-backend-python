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
        var NotesCollection = Backbone.Collection.extend({
            model: Note,
            url: function () {
                return '/ajax/notes';
            },
            notepad: null,

            parse: function (response) {
                return response.notes;
            },

            openNotepad: function (notepad) {
                this.notepad = notepad;
                this.url = '/ajax/notes?notepad-id=' + notepad.get('id');
                this.fetch({reset: true});
            },

            createOne: function (note, title, notepadId) {
                var that = this,
                    notepadId = this.notepad.get('id');

                var note = new Note();
                note.save(
                    {
                        title: title,
                        notepad_id: notepadId
                    },
                    {
                        success: function (model, response) {
                            that.add(model);
                        }
                    }
                );

                return note;
            },

            editOne: function (note, title, notepadId) {
                note.save({
                    title: title,
                    notepad_id: notepadId
                });
            },

            deleteOne: function (note) {
                note.destroy({wait: true});
            }
        });

        return NotesCollection;
    }
);