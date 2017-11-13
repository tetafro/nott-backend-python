var $ = require('jquery');
var Backbone = require('backbone');
var App = require('../app');
var NotesCollection = require('../collections/NotesCollection');
var NoteView = require('../views/NoteView');

module.exports = Backbone.View.extend({
    collection: NotesCollection,
    el: $('.sidebar-second .nav-sidebar'),

    initialize: function () {
        this.listenTo(this.collection, 'add', this.onAdd);
        this.listenTo(this.collection, 'rerender', this.render);
        this.listenTo(this.collection, 'request', this.onAjaxStart);
        this.listenTo(this.collection, 'sync', this.onAjaxComplete);
        this.listenTo(this.collection, 'error', this.onError);

        this.render();
    },

    onAjaxStart: function () {
        App.AppView.showLoadIcon();
    },

    onAjaxComplete: function () {
        App.AppView.hideLoadIcon();
    },

    onError: function (collection, error) {
        App.AppView.hideLoadIcon();
        App.AppView.displayError(error);
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

        $('.search-form').hide();
    }
});
