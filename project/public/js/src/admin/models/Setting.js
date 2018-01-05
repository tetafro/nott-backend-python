var Backbone = require('backbone');
var Config = require('../../config');

module.exports = Backbone.Model.extend({
    defaults: {
        id: null,
        code: null,
        name: null,
        datatype: null,
        value: null
    },
    idAttribute: 'id',
    urlRoot: Config.urls.api.settings
});
