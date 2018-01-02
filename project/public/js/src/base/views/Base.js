var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var Config = require('../../config');
var BaseTemplate = require('raw-loader!../templates/Base.html');

module.exports = Backbone.View.extend({
    el: $('#app'),
    template: _.template(BaseTemplate),

    events: {
        'click a.goto': 'goto',
        'click .logout': 'logout'
    },

    initialize: function (router) {
        this.render();
    },

    goto: function (event) {
        event.preventDefault();
        var href = event.currentTarget.getAttribute("href");
        Backbone.history.navigate(href, true);
    },

    // Fire at any navigate() and highlight current section in navbar
    nav: function (href) {
        this.$('.nav.navbar-nav li').removeClass('active');
        var $a;
        switch (href) {
            case '':
            case 'notes':
                $a = $('nav.navbar li a[href="/"]');
                break;
            case 'users/me':
                $a = $('nav.navbar li a[href="/users/me"]');
                break;
            case 'admin':
                $a = $('nav.navbar li a[href="/admin"]');
                break;
            default:
                return;
        }
        $a.parent().addClass('active');
    },

    logout: function () {
        $.ajax({
            url: Config.urls.api.logout,
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            data: '{}',
            complete: function (response) {
                window.App.logout();
                Backbone.history.navigate(Config.urls.pages.login, true);
            }
        });
    },

    render: function () {
        this.$el.html(this.template({user: window.App.currentUser}));

        // Make current page active in navbar
        var path = window.location.pathname;
        if (path.startsWith("/users/")) {
            path = '/users/me';
        }
        this.$('nav.navbar li a[href="' + path + '"]')
            .parent()
            .addClass('active');
    }
});
