var $ = require('jquery');
var Backbone = require('backbone');
var FoldersCollection = require('../collections/Folders');
var FolderView = require('../views/Folder');

module.exports = Backbone.View.extend({
    collection: FoldersCollection,
    el: function () {
        return $('.sidebar-first .nav-sidebar');
    },

    initialize: function () {
        this.listenTo(this.collection, 'add', this.onAdd);
        this.listenTo(this.collection, 'change:parent_id', this.onMove);
        this.listenTo(this.collection, 'request', this.onAjaxStart);
        this.listenTo(this.collection, 'sync', this.onAjaxComplete);
        this.listenTo(this.collection, 'error', this.onError);

        this.render();
    },

    ajaxStart: function () {
        window.App.views.base.showLoadIcon();
    },

    ajaxComplete: function () {
        window.App.views.base.hideLoadIcon();
    },

    onError: function (collection, error) {
        window.App.views.base.hideLoadIcon();
        window.App.views.base.displayError('error', error);
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

        // Render folders from root
        that.collection.sortByField('title');
        that.collection.processTree(function (folder, lvl) {
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
