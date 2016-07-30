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

            events: {
                'click #show-search': 'toggleSearchMode',
                'click .sidebar-first > h4 > .pull-right': 'showModal',
                'click .sidebar-second > h4 > .pull-right': 'showModal'
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

            showModal: function (event) {
                // Create folder/notepad from link at the top of the list
                if ($(event.currentTarget).attr('id') == 'new-folder-notepad') {
                    new ModalView({
                        action: 'create',
                        type: 'folder'
                    });
                // Create note
                } else if ($(event.currentTarget).attr('id') == 'new-note') {
                    new ModalView({
                        action: 'create',
                        type: 'note'
                    });
                }
            },

            // This method is used for all errors over the app
            displayError: function (msg) {
                var $errorBlock = this.$('#flash-message');

                $errorBlock.find('.message').text(msg);

                $errorBlock.fadeIn(300);
                setTimeout(function () {
                    $errorBlock.fadeOut(300);
                }, 2000);

                console.log('ERROR: ' + msg);
            },

            showLoadIcon: function () {
                this.$('#loading-icon').show();
            },

            hideLoadIcon: function () {
                this.$('#loading-icon').hide();
            },

            render: function () {
                // Fetch and render all folders and notepads
                App.AppView.showLoadIcon();
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
                    },
                    error: function () {
                        App.AppView.displayError('Request timeout. Try again later.');
                    },
                    complete: function () {
                        App.AppView.hideLoadIcon();
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
