var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var Bootstrap = require('bootstrap');
var Helpers = require('./helpers');

module.exports = {
    init: function () {
        var token = Helpers.getCSRF();

        // Set CSRF token for all Backbone's requests
        var oldSync = Backbone.sync;
        Backbone.sync = function (method, model, options) {
            options.beforeSend = function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', token);
            };
            return oldSync(method, model, options);
        };

        // Set timeout for all ajax requests
        $.ajaxSetup({timeout: 5000});

        return this;
    }
};
