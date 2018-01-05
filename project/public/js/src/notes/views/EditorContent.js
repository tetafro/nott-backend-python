var _ = require('underscore');
var Backbone = require('backbone');
var Note = require('../models/Note');
var EditorContentTemplate = require('raw-loader!../templates/EditorContent.html');

module.exports = Backbone.View.extend({
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
        'shown.bs.tab a.editor-edit': 'activateEditor',
        'click .btn-save': 'saveModel',
        'keypress textarea.editor-content': 'checkHotkey'
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

    activateEditor: function () {
        this.$('textarea.editor-content').focus();
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
                        // Update rendered content
                        that.$('div.editor-content')
                            .html(model.get('html'));
                        // Open view tab
                        that.switchMode('view');
                    }
                });
            }
        });
    },

    // Handle hotkeys
    checkHotkey: function (event) {
        // Save note on CTRL+Enter
        if (event.keyCode == 10 && event.ctrlKey) {
            this.saveModel(event.keyCode);
        }
    },

    // Open view or edit tab of the note
    switchMode: function (mode) {
        var viewTab = '#editor-' + this.model.get('id');
        if (mode == 'edit') {
            viewTab += '-edit';
        } else {
            viewTab += '-view';
        }
        this.$('.nav-pills a[href="' + viewTab + '"]').tab('show');
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.addClass('active');
    }
});
