var $ = require('jquery');
var Backbone = require('backbone');
var NotesCollection = require('../collections/Notes');
var NoteView = require('../views/Note');

module.exports = Backbone.View.extend({
    collection: NotesCollection,
    el: function () {
        return $('.sidebar-second .nav-sidebar');
    },

    initialize: function () {
        this.listenTo(this.collection, 'add', this.onAdd);
        this.listenTo(this.collection, 'rerender', this.render);
        this.listenTo(this.collection, 'request', this.onAjaxStart);
        this.listenTo(this.collection, 'sync', this.onAjaxComplete);
        this.listenTo(this.collection, 'error', this.onError);

        this.render();
    },

    onAjaxStart: function () {
        window.App.views.base.showLoadIcon();
    },

    onAjaxComplete: function () {
        window.App.views.base.hideLoadIcon();
    },

    onError: function (collection, error) {
        window.App.views.base.hideLoadIcon();
        window.App.views.base.displayError('error', error);
    },

    createOne: function () {
        var that = this;

        // Catch only pressing Enter
        if (event.type == 'keypress') {
            if (event.keyCode == 13) {
                event.preventDefault();
            } else {
                return;
            }
        }

        var $input = $(event.target).closest('form').find('input');
        var title = $input.val();

        that.collection.createOne(title);
    },

    onAdd: function (note) {
        var noteView = new NoteView({model: note});
        this.$el.append(noteView.$el);
    },

    render: function () {
        var that = this;

        // Clear list of notes
        that.$el.empty();

        var note;
        var noteView;

        // Sort and render
        this.collection.sortByField('title');
        this.collection.each(function (note) {
            var noteView = new NoteView({model: note});
            that.$el.append(noteView.$el);
        });
    }
});
