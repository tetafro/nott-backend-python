var Backbone = require('backbone');
var App = require('../app');

module.exports = Backbone.Model.extend({
    defaults: {
        id: null,
        title: null,
        parent_id: null
    },
    // To be able to determine what object type is current model
    type: 'folder',
    idAttribute: 'id',
    urlRoot: '/ajax/folders/',

    events: {
        'request': this.ajaxStart,
        'sync': this.ajaxComplete,
        'error': 'displayError'
    },

    ajaxStart: function () {
        App.AppView.showLoadIcon();
    },

    ajaxComplete: function () {
        App.AppView.hideLoadIcon();
    },

    displayError: function (model, error) {
        App.AppView.hideLoadIcon();
        App.AppView.displayError(error);
    },

    validate: function (attributes) {
        if (!attributes.title) {
            return 'Title cannot be empty';
        }
        if (attributes.title.length > 80) {
            return 'Title is too long';
        }
    }
});
