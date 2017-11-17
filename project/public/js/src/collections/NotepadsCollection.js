var Backbone = require('backbone');
var App = require('../app');
var Notepad = require('../models/Notepad');

module.exports = Backbone.Collection.extend({
    model: Notepad,
    url: '/ajax/notepads/',
    active: null,

    parse: function (response) {
        return response.notepads;
    },

    sortByField: function(field) {
        var oldComparator = this.comparator;

        this.comparator = function(model) {
            return model.get(field);
        }
        this.sort();

        this.comparator = oldComparator;
    },

    createOne: function (title, folderId) {
        var that = this;
        var notepad = new Notepad();

        notepad.save(
            {
                title: title,
                folder_id: folderId
            },
            {
                success: function (model, response) {
                    that.add(model);
                }
            }
        );

        return notepad;
    },

    editOne: function (notepad, title, folderId) {
        notepad.save({
            title: title,
            folder_id: folderId
        });
    },

    deleteOne: function (notepad) {
        notepad.destroy({wait: true});
    },

    setActive: function (activeNotepad) {
        this.each(function (notepad) {
            notepad.set('active', false);
        });
        activeNotepad.set('active', true);
        this.active = activeNotepad;
    }
});
