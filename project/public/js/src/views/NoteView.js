define(
    [
        'underscore', 'backbone', 'app',
        'models/Note',
        'views/ModalView',
        'templates/NoteTemplate'
    ],
    function (
        _, Backbone, App,
        Note,
        ModalView,
        NoteTemplate
    ) {
        var NoteView = Backbone.View.extend({
            model: Note,
            tagName: 'li',
            attributes: function () {
                return {
                    'data-type': 'note',
                    'data-id': this.model.get('id')
                };
            },
            template: _.template(NoteTemplate),

            events: {
                'click .item': 'open',
                'click .edit': 'showModal',
                'click .del': 'showModal'
            },

            initialize: function () {
                this.listenTo(this.model, 'change:title', this.rename);
                this.listenTo(this.model, 'change:active', this.onChangeActive);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            open: function () {
                this.model.open();
            },

            // Change view when element activated/deactivated
            onChangeActive: function () {
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
                // In case of rendering model, which is opened in tabs
                if (this.model.get('active')) {
                    this.$el.addClass('active');
                }
            }
        });

        return NoteView;
    }
);
