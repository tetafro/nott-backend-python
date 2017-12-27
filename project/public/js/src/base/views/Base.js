var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var BaseTemplate = require('raw-loader!../templates/Base.html');

module.exports = Backbone.View.extend({
    el: $('#app'),
    template: _.template(BaseTemplate),

    events: {
        'click a.goto': 'goto',
    },

    initialize: function () {
        // Listen to any routing event across the app
        this.listenTo(window.App.Router, 'route', this.onGoto);

        this.render();
    },

    goto: function (event) {
        event.preventDefault();
        var href = event.currentTarget.getAttribute("href");
        Backbone.history.navigate(href, true);
    },

    // Fire at any navigate() and highlight current section in navbar
    onGoto: function (target) {
        this.$('.nav.navbar-nav li').removeClass('active');
        var $a;
        switch (target) {
            case 'notes':
                $a = $('nav.navbar li a[href="/"]');
                break;
            case 'profile':
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

    render: function () {
        this.$el.html(this.template());

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
