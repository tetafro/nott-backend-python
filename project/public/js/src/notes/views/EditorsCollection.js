var $ = require('jquery');
var Backbone = require('backbone');
var EditorsCollection = require('../collections/Editors');
var EditorHeadView = require('../views/EditorHead');
var EditorContentView = require('../views/EditorContent');

module.exports = Backbone.View.extend({
    collection: EditorsCollection,
    el: function () {
        return $('.editor-block');
    },

    initialize: function () {
        this.listenTo(this.collection, 'add', this.onOpen);
    },

    // Make tab and open editor
    onOpen: function (note) {
        var editorHeadView = new EditorHeadView({model: note});
        $('.editor-block > .nav-tabs').append(editorHeadView.$el);

        var editorContentView = new EditorContentView({model: note});
        $('.editor-block > .tab-content').append(editorContentView.$el);
    }
});
