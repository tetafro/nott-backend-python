define(
    [
        'underscore', 'backbone',
        'app',
        'models/Note'
    ],
    function (
        _, Backbone,
        App,
        Note
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
            template: _.template('<div id="editor-<%= id %>" class="editor"></div>'),
            templateSaveButton: `
                <button type="button" class="btn btn-sm btn-save" title="Save">
                    <i class="glyphicon glyphicon-ok-circle"></i>
                </button>`,

            // Trumbowyg
            editorOptions: {
                btns: [
                    'viewHTML',
                    ['bold', 'italic'],
                    ['foreColor']
                ],
                removeformatPasted: true,
                fullscreenable: false,
                svgPath: '/public/images/trumbowyg-icons.svg'
            },

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
                var text = this.$('#editor-' + this.model.get('id')).trumbowyg('html');
                this.model.save({text: text});
            },

            // This code is not in the render method, because tab for the editor
            // must be already on the page before editor renders so it can
            // calculate it's height
            initEditor: function () {
                var that = this;
                var modelId = that.model.get('id');

                // Load WYSIWYG editor
                that.$('.editor')
                    .attr('spellcheck', 'false') // TODO: move to template string above
                    .trumbowyg(that.editorOptions)
                    .trumbowyg('empty'); // explicitly clear editor

                that.$('.editor')
                    .trumbowyg('html', this.model.get('text'));

                // Append self-made save button
                that.$('.trumbowyg-button-pane').append(this.templateSaveButton);
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                this.$el.addClass('active');
            }
        });

        return EditorContentView;
    }
);
