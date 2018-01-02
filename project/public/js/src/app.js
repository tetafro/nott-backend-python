var $ = require('jquery');
require('bootstrap');
var Backbone = require('backbone');
require('backbone-route-filter');
var Config = require('./config');
var Router = require('./router');
var BaseView = require('./base/views/Base');

USER = {username: 'Bob'};

App = {
    currentUser: null,
    collections: {},
    views: {},
    router: {},

    init: function () {
        var token = this.getToken();
        if (token != null) {
            this.setAuthHeader(token);
        }

        // Set timeout for all AJAX requests
        $.ajaxSetup({timeout: 5000});

        // Default AJAX error handler
        $(document).ajaxError(function (e, xhr, options) {
            // Unauthorized
            if (xhr.status == 401) {
                Backbone.history.navigate(Config.urls.pages.login, true);
            }
        });

        // Fetch user if token is not empty
        var token = window.localStorage.getItem('token');
        if (token != null) {
            window.App.currentUser = USER;
        }

        // Render app frame
        this.views.base = new BaseView(this);

        // Init routing system
        this.router = new Router();

        return this;
    },

    getToken: function () {
        return window.localStorage.getItem('token');
    },

    setToken: function (token) {
        window.localStorage.setItem('token', token);
    },

    removeToken: function () {
        window.localStorage.removeItem('token');
    },

    isAuthenticated: function () {
        return this.currentUser != null;
    },

    // Set token for all Backbone's requests
    setAuthHeader: function (token) {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader(
                    'Authorization',
                    'Token token="' + token + '"'
                );
            }
        });
    },

    // Unset token for Backbone's requests
    unsetAuthHeader: function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {}
        });
    },

    login: function (token) {
        this.currentUser = USER;
        this.setToken(token);
        this.setAuthHeader(token);

        // Rerender frame to show navigation
        window.App.views.base.render();
    },

    logout: function () {
        this.currentUser = null;
        this.removeToken();
        this.unsetAuthHeader();

        // Rerender frame to hide navigation
        window.App.views.base.render();
    }
};

$(document).ready(function () {
    window.App = App.init();
});
