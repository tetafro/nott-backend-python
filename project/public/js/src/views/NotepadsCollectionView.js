var $ = require('jquery');
var Backbone = require('backbone');
var App = require('../app');
var NotepadsCollection = require('../collections/NotepadsCollection');
var NotepadView = require('../views/NotepadView');

module.exports = Backbone.View.extend({
    collection: NotepadsCollection,
    el: $('.sidebar-first .nav-sidebar'),

    initialize: function () {
        this.listenTo(this.collection, 'add', this.onAdd);
        this.listenTo(this.collection, 'change:folder_id', this.onMove);
        this.listenTo(this.collection, 'request', this.onAjaxStart);
        this.listenTo(this.collection, 'sync', this.onAjaxComplete);
        this.listenTo(this.collection, 'error', this.onError);

        this.render();
    },

    ajaxStart: function () {
        App.AppView.showLoadIcon();
    },

    ajaxComplete: function () {
        App.AppView.hideLoadIcon();
    },

    displayError: function (collection, error) {
        App.AppView.hideLoadIcon();
        App.AppView.displayError(error);
    },

    onAdd: function (notepad) {
        var notepadView = new NotepadView({model: notepad});
        var folderId = notepad.get('folder_id');

        if (folderId) {
            this.$('#folder-' + folderId + '.children-block')
                .append(notepadView.$el);
        } else {
            this.$el.append(notepadView.$el);
        }
    },

    onMove: function (notepad) {
        var $element = $('[data-type="notepad"][data-id="' + notepad.get('id') + '"]');
        var $parent = $('#folder-' + notepad.get('folder_id'));
        $element.appendTo($parent);
    },

    render: function () {
        // Clear previously rendered
        this.$('li[data-type="notepad"]').remove();

        this.collection.each(function (notepad) {
            var notepadView = new NotepadView({model: notepad});

            $('#folder-' + notepad.get('folder_id') + '.children-block')
                .append(notepadView.$el);
        });
    }
});
