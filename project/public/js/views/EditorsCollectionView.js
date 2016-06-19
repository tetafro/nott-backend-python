define(
    [
        'jquery', 'backbone',
        'collections/EditorsCollection',
        'views/EditorHeadView', 'views/EditorContentView'
    ],
    function (
        $, Backbone,
        EditorsCollection,
        EditorHeadView, EditorContentView
    ) {
        var EditorsCollectionView = Backbone.View.extend({
            collection: EditorsCollection,
            el: $('#editor-block'),

            initialize: function () {
                this.listenTo(this.collection, 'add', this.onOpen);
            },

            onOpen: function (note) {
                var editorHeadView = new EditorHeadView({model: that});
                $('#editor-block > .nav-tabs').append(editorHeadView.$el);

                var editorContentView = new EditorContentView({model: that});
                $('#editor-block > .tab-content').append(editorContentView.$el);
                editorContentView.initEditor();
            }
        });

        return EditorsCollectionView;
    }
);