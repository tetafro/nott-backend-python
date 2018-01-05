var Backbone = require('backbone');
var Config = require('../../config');

module.exports = Backbone.Model.extend({
    defaults: {
        id: null,
        username: null,
        avatar_url: null,
        email: null,
        role: null,
        created: null,
        updated: null
    },
    idAttribute: 'id',
    urlRoot: Config.urls.api.users,

    parse: function (response) {
        user = response;
        user.created = new Date(response.created);
        user.updated = new Date(response.updated);
        return user;
    }
});
