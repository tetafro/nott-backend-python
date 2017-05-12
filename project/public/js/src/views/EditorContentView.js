define(
    [
        'underscore', 'backbone',
        'app',
        'models/Note',
        'templates/EditorContentTemplate'
    ],
    function (
        _, Backbone,
        App,
        Note,
        EditorContentTemplate
    ) {
        var EditorContentView = Backbone.View.extend({
            model: Note,
            tagName: 'div',
            id: function () {
                return 'tab-' + this.model.get('id');
            },
            className: 'tab-pane',
            attributes: {
                role: 'tabpanel'
            },
            template: _.template(EditorContentTemplate),

            events: {
                'click .btn-save': 'saveModel'
            },

            initialize: function () {
                // Initially opened == true
                this.listenTo(this.model, 'change:opened', this.remove);
                this.listenTo(this.model, 'change:active', this.onChangeActive);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            // Change view when element activated/deactivated
            onChangeActive: function () {
                this.$el.toggleClass('active');
            },

            saveModel: function (event) {
                var text = this
                    .$('#editor-' + this.model.get('id') + ' textarea')
                    .val();
                this.model.save({text: text});
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                this.$el.addClass('active');
            }
        });

        return EditorContentView;
    }
);
