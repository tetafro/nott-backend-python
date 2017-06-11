var Backbone = require('backbone');
var App = require('../app');
var NotesCollection = require('../collections/NotesCollection');
var NotesCollectionView = require('../views/NotesCollectionView');

module.exports = Backbone.Model.extend({
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
        'request': this.ajaxStart,
        'sync': this.ajaxComplete,
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

    ajaxStart: function () {
        App.AppView.showLoadIcon();
    },

    ajaxComplete: function () {
        App.AppView.hideLoadIcon();
    },

    displayError: function (model, error) {
        App.AppView.hideLoadIcon();
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
