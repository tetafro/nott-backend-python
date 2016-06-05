define(
    [
        'underscore', 'backbone',
        'models/Notepad',
        'collections/NotesCollection',
        'views/NotesCollectionView', 'views/ModalView',
        'templates/NotepadTemplate'
    ],
    function (
        _, Backbone,
        Notepad,
        NotesCollection,
        NotesCollectionView, ModalView,
        NotepadTemplate
    ) {
        var NotepadView = Backbone.View.extend({
            model: Notepad,
            tagName: 'li',
            attributes : function () {
                return {
                    'data-type': 'notepad',
                    'data-id': this.model.get('id')
                };
            },
            template: _.template(NotepadTemplate),

            events: {
                'click .item': 'activate',
                'click .edit': 'showModal',
                'click .del': 'showModal'
            },

            initialize: function () {
                this.listenTo(this.model, 'change:title', this.rename);
                this.listenTo(this.model, 'change:active', this.onActivate);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            // Run activation
            activate: function () {
                this.model.activate();
            },

            // Change view when element activated/deactivated
            onActivate: function () {
                this.$el.toggleClass('active');
            },

            // Modal window with details for CRUD operation
            showModal: function (event) {
                // Since lists are nested, clicking on child element
                // is propagating to all parents. It shouldn't happen.
                event.stopPropagation();

                if ($(event.currentTarget).hasClass('edit')) {
                    new ModalView({
                        model: this.model,
                        action: 'edit'
                    });
                } else if ($(event.currentTarget).hasClass('del')) {
                    new ModalView({
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