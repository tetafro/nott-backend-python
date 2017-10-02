var Backbone = require('backbone');
var App = require('../app');
var Folder = require('../models/Folder');

module.exports = Backbone.Collection.extend({
    model: Folder,
    url: '/ajax/folders/',

    parse: function (response) {
        return response.folders;
    },

    sortByField: function(field) {
        var oldComparator = this.comparator;

        this.comparator = function(model) {
            return model.get(field);
        }
        this.sort();

        this.comparator = oldComparator;
    },

    createOne: function (title, parentId) {
        var that = this;
        var folder = new Folder();

        folder.save(
            {
                title: title,
                parent_id: parentId
            },
            {
                success: function (model, response) {
                    that.add(model);
                }
            }
        );

        return folder;
    },

    editOne: function (folder, title, parentId) {
        folder.save({
            title: title,
            parent_id: parentId
        });
    },

    deleteOne: function (folder) {
        folder.destroy({wait: true});
    }
});
