define(
    [
        'underscore', 'backbone',
        'models/Folder',
        'views/ModalView',
        'templates/FolderTemplate'
    ],
    function (
        _, Backbone,
        Folder,
        ModalView,
        FolderTemplate
    ) {
        var FolderView = Backbone.View.extend({
            model: Folder,
            tagName: 'li',
            attributes : function () {
                return {
                    'data-type': 'folder',
                    'data-id': this.model.get('id')
                };
            },
            template: _.template(FolderTemplate),

            events: {
                'click .expand': 'expand',
                'click .add': 'showModal',
                'click .edit': 'showModal',
                'click .del': 'showModal'
            },

            initialize: function () {
                this.listenTo(this.model, 'change:title', this.rename);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            // Open folder: show subfolder and change icon
            expand: function (event) {
                event.stopPropagation();
                this.$('> ul').collapse('toggle');
                this.$('> div > a > i')
                    .toggleClass('glyphicon-folder-open')
                    .toggleClass('glyphicon-folder-close');
            },

            // Modal window with details for CRUD operation
            showModal: function (event) {
                // Since lists are nested, clicking on child element
                // is propagating to all parents. It shouldn't happen.
                event.stopPropagation();

                if ($(event.currentTarget).hasClass('add')) {
                    new ModalView({
                        action: 'create',
                        parentId: this.model.get('id'),
                        type: 'folder'
                    });
                } else if ($(event.currentTarget).hasClass('edit')) {
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

        return FolderView;
    }
);