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
        this.render();
    },

    goto: function (event) {
        event.preventDefault();
        var href = event.currentTarget.getAttribute("href");
        Backbone.history.navigate(href, true);

        this.$('.nav.navbar-nav li').removeClass('active');
        var $li = $(event.currentTarget).parent();
        if ($li.parent().hasClass('navbar-nav')) {
            $li.addClass('active');
        } else {
            // Click on home link
            this.$('.nav.navbar-nav a[href="/"]')
                .parent()
                .addClass('active');
        }
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
