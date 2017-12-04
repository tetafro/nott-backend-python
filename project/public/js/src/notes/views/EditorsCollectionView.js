var $ = require('jquery');
var Backbone = require('backbone');
var EditorsCollection = require('../collections/EditorsCollection');
var EditorHeadView = require('../views/EditorHeadView');
var EditorContentView = require('../views/EditorContentView');

module.exports = Backbone.View.extend({
    collection: EditorsCollection,
    el: $('.editor-block'),

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
