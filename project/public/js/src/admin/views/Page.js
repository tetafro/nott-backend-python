var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var Config = require('../../config');
var UsersCollection = require('../../users/collections/Users');
var SettingsCollection = require('../collections/Settings');
var SettingsCollectionView = require('../views/SettingsCollection');
var UsersCollectionView = require('../views/UsersCollection');
var PageTemplate = require('raw-loader!../templates/Page.html');


module.exports = Backbone.View.extend({
    el: function () {
        return $('#content');
    },
    template: _.template(PageTemplate),

    initialize: function () {
        var settings = new SettingsCollection(),
            users = new UsersCollection();

        window.App.views.page = this;
        this.render();

        // Render child views
        settings.fetch({
            success: function () {
                new SettingsCollectionView({collection: settings});
            }
        });
        users.fetch({
            success: function () {
                new UsersCollectionView({collection: users});
            }
        });
    },

    getVersion: function () {
        var version = 'Unknown';
        $.ajax({
            async: false,
            url: Config.urls.api.version,
            contentType: 'application/json',
            type: 'GET',
            success: function (response) {
                if ('version' in response) {
                    version = response.version;
                }
            }
        });
        return version;
    },

    render: function () {
        var version = this.getVersion();
        this.$el.html(this.template({version: version}));
    }
});
