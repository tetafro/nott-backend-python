var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var Folder = require('../models/Folder');
var FoldersCollection = require('../collections/Folders');
var NotepadsCollection = require('../collections/Notepads');
var NotesCollection = require('../collections/Notes');
var EditorsCollection = require('../collections/Editors');
var FoldersCollectionView = require('../views/FoldersCollection');
var NotepadsCollectionView = require('../views/NotepadsCollection');
var NotesCollectionView = require('../views/NotesCollection');
var EditorsCollectionView = require('../views/EditorsCollection');
var ModalView = require('../views/Modal');
var SearchFormView = require('../views/SearchForm');
var PageTemplate = require('raw-loader!../templates/Page.html');

module.exports = Backbone.View.extend({
    el: function () {
        return $('#content');
    },
    template: _.template(PageTemplate),
    modal: null, // link to modal window

    events: {
        'click .sidebar-first > h4 > .pull-right': 'callModal',
        'click .sidebar-second > h4 > .pull-right': 'callModal'
    },

    initialize: function () {
        var that = this;
        var folders = new FoldersCollection();
        var notepads = new NotepadsCollection();
        var notes = new NotesCollection();
        var editors = new EditorsCollection();

        // Add global links to collections
        window.App.collections.folders = folders;
        window.App.collections.notepads = notepads;
        window.App.collections.notes = notes;
        window.App.collections.editors = editors;

        window.App.views.page = that;

        that.render();

        // Render child views
        folders.fetch({
            success: function () {
                new FoldersCollectionView({collection: folders});

                notepads.fetch({
                    success: function () {
                        new NotepadsCollectionView({collection: notepads});
                    }
                });
            }
        });
        new NotesCollectionView({collection: notes});
        new EditorsCollectionView({collection: editors});
        new SearchFormView({collection: notes});
    },

    callModal: function (event) {
        var objectType;

        // Create folder/notepad from link at the top of the list
        if ($(event.currentTarget).attr('id') == 'new-folder-notepad') {
            objectType = 'folder';
        // Create note
        } else if ($(event.currentTarget).attr('id') == 'new-note') {
            objectType = 'note';
        }

        this.showModal({
            action: 'create',
            type: objectType
        });
    },

    showModal: function (options) {
        this.modal = new ModalView(options);
    },

    render: function () {
        this.$el.html(this.template());
    }
});
