var Backbone = require('backbone');
var Config = require('../../config');
var Setting = require('../models/Setting');

module.exports = Backbone.Collection.extend({
    model: Setting,
    url: Config.urls.api.settings,

    parse: function (response) {
        return response.settings;
    }
});
