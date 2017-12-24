var $ = require('jquery');
var Bootstrap = require('bootstrap');
var Backbone = require('backbone');
var Config = require('./config');
var Router = require('./router');
var BaseView = require('./base/views/Base');

App = {
    init: function () {
        // Set token for all Backbone's requests
        var oldSync = Backbone.sync;
        Backbone.sync = function (method, model, options) {
            options.beforeSend = function (xhr) {
                var token = window.localStorage.getItem('token');
                xhr.setRequestHeader(
                    'Authorization',
                    'Token token="' + token + '"'
                );
            };
            return oldSync(method, model, options);
        };

        // Set timeout for all AJAX requests
        $.ajaxSetup({timeout: 5000});

        // Default AJAX error handler
        $(document).ajaxError(function (e, xhr, options) {
            // Unauthorized
            if (xhr.status == 401) {
                Backbone.history.navigate(Config.urls.pages.login, true);
            }
        });

        // Init routing system
        this.Router = new Router();

        // Render app frame
        new BaseView();

        // Init router
        // NOTE: you cannot do it inside Router.initialize() because it
        // needs BaseView to be rendered first, and BaseView needs Router
        // to be created to start listening to it's events.
        Backbone.history.start({pushState: true});

        // Redirect to login if there is no token
        var token = window.localStorage.getItem('token');
        if (token == '') {
            Backbone.history.navigate(href, true);
        }

        return this;
    }
};

$(document).ready(function () {
    window.App = App.init();
});
