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
                var that = this,
                    len = that.collection.length;

                // Clear list of folders and notepads
                that.$el.empty();

                // Recursion function for rendering tree
                var renderChildren = function (parentFolder) {
                    var folder,
                        folderView,
                        parentFolderId = parentFolder.get('id'),
                        parentFolderParentId = parentFolder.get('parent_id');

                    folderView = new FolderView({model: parentFolder});
                    if (parentFolderParentId == null) {
                        that.$el.append(folderView.$el);
                    } else {
                        that.$('#folder-' + parentFolderParentId + '.children-block')
                            .append(folderView.$el);
                    }

                    for (var i = 0; i < len; i++) {
                        folder = that.collection.at(i);
                        if (parentFolderId == folder.get('parent_id')) {
                            renderChildren(folder);
                        }
                    };
                }

                that.collection.sortBy('title');

                // Render folders from root
                var folder;
                for (var i = 0; i < len; i++) {
                    folder = that.collection.at(i);
                    if (!folder.get('parent_id')) {
                        renderChildren(folder);
                    }
                };
            }
        });

        return FoldersCollectionView;
    }
);