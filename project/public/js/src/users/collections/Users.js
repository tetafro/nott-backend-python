var Backbone = require('backbone');
var Config = require('../../config');
var User = require('../models/User');

module.exports = Backbone.Collection.extend({
    model: User,
    url: Config.urls.api.users,

    parse: function (response) {
        return response.users;
    }
});
