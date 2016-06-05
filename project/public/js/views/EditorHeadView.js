define(
    [
        'jquery', 'backbone',
        'models/Note'
    ],
    function (
        $, Backbone,
        Note
    ) {
        var EditorHeadView = Backbone.View.extend({
            model: Note,
            tagName: 'li',
            attributes: function () {
                return {
                    'data-id': this.model.get('id')
                }
            },
            template: _.template(
                `<a href="#tab-<%= id %>" role="tab" data-toggle="tab">
                    <%= title %><div class="tab-close">&times;</div>
                </a>`
            ),

            events: {
                'click li': 'open',
                'click .tab-close': 'close'
            },

            initialize: function () {
                // Initially opened == true
                this.listenTo(this.model, 'change:opened', this.remove);
                this.listenTo(this.model, 'change:active', this.onChangeActive);
                this.listenTo(this.model, 'destroy', this.remove);
                this.render();
            },

            open: function () {
                this.model.open();
            },

            close: function () {
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