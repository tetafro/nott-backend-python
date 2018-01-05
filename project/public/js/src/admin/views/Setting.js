var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var Setting = require('../models/Setting');
var SettingTemplate = require('raw-loader!../templates/Setting.html');

module.exports = Backbone.View.extend({
    model: Setting,
    tagName: 'tr',
    template: _.template(SettingTemplate),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
    }
});
