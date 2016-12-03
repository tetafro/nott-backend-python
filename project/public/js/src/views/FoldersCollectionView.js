define(
    [
        'jquery', 'backbone', 'app', 'helpers',
        'collections/FoldersCollection',
        'views/FolderView'
    ],
    function (
        $, Backbone, App, Helpers,
        FoldersCollection,
        FolderView
    ) {
        var FoldersCollectionView = Backbone.View.extend({
            collection: FoldersCollection,
            el: $('.sidebar-first .nav-sidebar'),

            initialize: function () {
                this.listenTo(this.collection, 'add', this.onAdd);
                this.listenTo(this.collection, 'change:parent_id', this.onMove);
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

            onAdd: function (folder) {
                var folderView = new FolderView({model: folder});
                var parentId = folder.get('parent_id');

                if (parentId) {
                    this.$('#folder-' + parentId + '.children-block')
                        .append(folderView.$el);
                } else {
                    this.$el.append(folderView.$el);
                }
            },

            onMove: function (folder) {
                var $element = $('[data-type="folder"][data-id="' + folder.get('id') + '"]');
                var $parent = $('#folder-' + folder.get('parent_id'));
                $element.appendTo($parent);
            },

            render: function () {
                var that = this;

                // Clear list of folders and notepads
                that.$el.empty();

                that.collection.sortBy('title');

                // Render folders from root
                Helpers.processTree(that.collection, 'parent_id', function (folder) {
                    var folderParentId = folder.get('parent_id');
                    var folderView = new FolderView({model: folder});

                    if (folderParentId == null) {
                        that.$el.append(folderView.$el);
                    } else {
                        that.$('#folder-' + folderParentId + '.children-block')
                            .append(folderView.$el);
                    }
                });
            }
        });

        return FoldersCollectionView;
    }
);
