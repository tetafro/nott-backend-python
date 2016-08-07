define(
    [
        'underscore', 'backbone', 'app',
        'models/Notepad',
        'collections/NotesCollection',
        'views/NotesCollectionView', 'views/ModalView',
        'templates/NotepadTemplate'
    ],
    function (
        _, Backbone, App,
        Notepad,
        NotesCollection,
        NotesCollectionView, ModalView,
        NotepadTemplate
    ) {
        var NotepadView = Backbone.View.extend({
            model: Notepad,
            tagName: 'li',
            attributes: function () {
                return {
                    'data-type': 'notepad',
                    'data-id': this.model.get('id')
                };
            },
            template: _.template(NotepadTemplate),

            events: {
                'click .item': 'open',
                'click .edit': 'showModal',
                'click .del': 'showModal'
            },

            initialize: function () {
                this.listenTo(this.model, 'change:title', this.rename);
                this.listenTo(this.model, 'change:active', this.onOpen);
                this.listenTo(this.model, 'request', this.onAjaxStart);
                this.listenTo(this.model, 'sync', this.onAjaxComplete);
                this.listenTo(this.model, 'error', this.onError);
                this.listenTo(this.model, 'destroy', this.onDestroy);

                this.render();
            },

            onAjaxStart: function () {
                App.AppView.showLoadIcon();
            },

            onAjaxComplete: function () {
                App.AppView.hideLoadIcon();
            },

            onError: function (model, error) {
                App.AppView.hideLoadIcon();
                App.AppView.displayError(error);
            },

            onDestroy: function () {
                App.AppView.hideLoadIcon();
                this.remove();
            },

            // Open notepad
            open: function () {
                this.model.open();
            },

            // Change view when element activated/deactivated
            onOpen: function () {
                this.$el.toggleClass('active');
            },

            // Modal window with details for CRUD operation
            showModal: function (event) {
                // Since lists are nested, clicking on child element
                // is propagating to all parents. It shouldn't happen.
                event.stopPropagation();

                if ($(event.currentTarget).hasClass('edit')) {
                    App.AppView.showModal({
                        model: this.model,
                        action: 'edit'
                    });
                } else if ($(event.currentTarget).hasClass('del')) {
                    App.AppView.showModal({
                        model: this.model,
                        action: 'delete'
                    });
                }
            },

            rename: function () {
                this.$('> div > a > span').html(this.model.get('title'));
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
            }
        });

        return NotepadView;
    }
);
