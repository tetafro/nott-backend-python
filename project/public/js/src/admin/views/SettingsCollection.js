var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var SettingsCollection = require('../collections/Settings');
var SettingView = require('../views/Setting');
var SettingsCollectionTemplate = require('raw-loader!../templates/SettingsCollection.html');

module.exports = Backbone.View.extend({
    collection: SettingsCollection,
    el: function () {
        return $('#tab-settings');
    },
    template: _.template(SettingsCollectionTemplate),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.html(this.template());

        var form = this.$('.settings-list');
        this.collection.each(function (setting) {
            var settingView = new SettingView({model: setting});
            form.append(settingView.$el);
        });
    }
});
