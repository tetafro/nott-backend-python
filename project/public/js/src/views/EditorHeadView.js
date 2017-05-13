define(
    [
        'jquery', 'backbone',
        'models/Note',
        'templates/EditorHeadTemplate'
    ],
    function (
        $, Backbone,
        Note,
        EditorHeadTemplate
    ) {
        var EditorHeadView = Backbone.View.extend({
            model: Note,
            tagName: 'li',
            attributes: function () {
                return {
                    'data-id': this.model.get('id')
                };
            },
            template: _.template(EditorHeadTemplate),

            events: {
                'click': 'open',
                'click .tab-close': 'close'
            },

            initialize: function () {
                // Initially opened == true
                this.listenTo(this.model, 'change:opened', this.remove);
                this.listenTo(this.model, 'change:active', this.onChangeActive);
                this.listenTo(this.model, 'change:title', this.rename);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            open: function (event) {
                this.model.open();
            },

            rename: function () {
                this.$('> a > span').text(this.model.get('title'));
            },

            close: function (event) {
                event.stopPropagation();
                this.model.close();
            },

            onChangeActive: function () {
                this.$el.toggleClass('active');
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                this.$el.addClass('active');
            }
        });

        return EditorHeadView;
    }
);
