var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var Bootstrap = require('bootstrap');

module.exports = {
    // Get CSRF token for making AJAX requests
    getCSRF: function () {
        var token = null;
        if (document.cookie) {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, 10) == 'csrftoken=') {
                    token = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return token;
    },

    init: function () {
        var token = this.getCSRF();

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
