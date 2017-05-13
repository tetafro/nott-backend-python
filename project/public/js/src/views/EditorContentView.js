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

            // Save and re-read rendered HTML from server
            saveModel: function (event) {
                var that = this,
                    text = that
                    .$('#editor-' + that.model.get('id') + ' textarea')
                    .val();
                that.model.save({text: text}, {
                    success: function (model, response) {
                        model.fetch({
                            success: function () {
                                that.$('div.editor-content')
                                    .html(model.get('html'));
                            }
                        })
                    }
                });
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                this.$el.addClass('active');
            }
        });

        return EditorContentView;
    }
);
