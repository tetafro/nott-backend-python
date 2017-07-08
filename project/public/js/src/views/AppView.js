var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var App = require('../app');
var Folder = require('../models/Folder');
var FoldersCollection = require('../collections/FoldersCollection');
var NotepadsCollection = require('../collections/NotepadsCollection');
var NotesCollection = require('../collections/NotesCollection');
var EditorsCollection = require('../collections/EditorsCollection');
var FoldersCollectionView = require('../views/FoldersCollectionView');
var NotepadsCollectionView = require('../views/NotepadsCollectionView');
var NotesCollectionView = require('../views/NotesCollectionView');
var EditorsCollectionView = require('../views/EditorsCollectionView');
var ModalView = require('../views/ModalView');

module.exports = Backbone.View.extend({
    el: '#app',
    modal: null, // link to modal window

    events: {
        'click #show-search': 'toggleSearchMode',
        'click .sidebar-first > h4 > .pull-right': 'callModal',
        'click .sidebar-second > h4 > .pull-right': 'callModal'
    },

    initialize: function () {
        // Add global links to collections
        App.foldersCollection = new FoldersCollection();
        App.notepadsCollection = new NotepadsCollection();
        App.notesCollection = new NotesCollection();
        App.editorsCollection = new EditorsCollection();
        App.AppView = this;

        this.listenTo(App.notepadsCollection, 'change:active', this.onNotepadActivate);

        this.render();
    },

    onNotepadOpen: function () {
        this.$('#new-note').show();
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

    // This method is used for all errors over the app
    displayError: function (msg) {
        // If modal window is visible, show error in it
        if (this.modal) {
            this.modal.displayError(null, msg);
            return;
        }

        var $errorBlock = this.$('#flash-message');

        // Text to show
        text = 'Something went wrong';
        if (typeof msg == 'string') {
            text = msg;
        } else if (typeof msg == 'object') {
            if (msg.responseJSON) {
                text = msg.responseJSON.error;
            }
        }

        $errorBlock.find('.message').text(text);
        $errorBlock.fadeIn(300);
        setTimeout(function () {
            $errorBlock.fadeOut(300);
        }, 2000);
    },

    showLoadIcon: function () {
        this.$('#loading-icon').show();
    },

    hideLoadIcon: function () {
        this.$('#loading-icon').hide();
    },

    render: function () {
        // Fetch and render all folders and notepads
        App.foldersCollection.fetch({
            success: function () {
                new FoldersCollectionView({
                    collection: App.foldersCollection
                });

                App.notepadsCollection.fetch({
                    success: function () {
                        new NotepadsCollectionView({
                            collection: App.notepadsCollection
                        });
                    }
                });
            }
        });

        // List of notes in left panel
        new NotesCollectionView({
            collection: App.notesCollection
        });
        // List of notes in left panel
        new EditorsCollectionView({
            collection: App.editorsCollection
        });
    }
});
