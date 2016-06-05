define(
    [
        'jquery', 'backbone',
        'collections/FoldersCollection',
        'views/FolderView'
    ],
    function (
        $, Backbone,
        FoldersCollection,
        FolderView
    ) {
        var FoldersCollectionView = Backbone.View.extend({
            collection: FoldersCollection,
            el: $('.sidebar-first .nav-sidebar'),

            initialize: function () {
                this.listenTo(this.collection, 'add', this.onAdd);
                this.listenTo(this.collection, 'change:parent_id', this.onMove);
                this.render();
            },

            onAdd: function (folder) {
                var folderView = new FolderView({model: folder}),
                    parentId = folder.get('parent_id');

                if (parentId) {
                    this.$('#folder-' + parentId + '.children-block')
                        .append(folderView.$el);
                } else {
                    this.$el.append(folderView.$el);
                }
            },

            onMove: function (folder) {
                var $element = $('[data-type="folder"][data-id="' + folder.get('id') + '"]'),
                    $parent = $('#folder-' + folder.get('parent_id'));
                $element.appendTo($parent);
            },

            render: function() {
                var that = this;

                // Clear list of folders and notepads
                that.$el.empty();

                var folder,
                    folderView,
                    parentId;

                for (var i = 0; i < that.collection.length; i++) {
                    folder = that.collection.at(i);
                    folderView = new FolderView({model: folder});

                    parentId = folder.get('parent_id');
                    if (parentId) {
                        that.$('#folder-' + parentId + '.children-block')
                            .append(folderView.$el);
                    } else {
                        that.$el.append(folderView.$el);
                    }
                };
            }
        });

        return FoldersCollectionView;
    }
);