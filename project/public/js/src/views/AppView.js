define(
    [
        'jquery', 'underscore', 'backbone', 'app',
        'models/Folder',
        'collections/FoldersCollection', 'collections/NotepadsCollection',
        'collections/NotesCollection', 'collections/EditorsCollection',
        'views/FoldersCollectionView', 'views/NotepadsCollectionView',
        'views/NotesCollectionView', 'views/EditorsCollectionView', 'views/ModalView'
    ],
    function (
        $, _, Backbone, App,
        Folder,
        FoldersCollection, NotepadsCollection,
        NotesCollection, EditorsCollection,
        FoldersCollectionView, NotepadsCollectionView,
        NotesCollectionView, EditorsCollectionView, ModalView
    ) {
        var AppView = Backbone.View.extend({
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
                    objectType = 'folder'
                // Create note
                } else if ($(event.currentTarget).attr('id') == 'new-note') {
                    objectType = 'note'
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

        return AppView;
    }
);
