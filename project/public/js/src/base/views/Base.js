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
        'click button.logout': 'logout'
    },

    initialize: function () {
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
            case 'profile':
            case 'profile/edit':
                $a = $('nav.navbar li a[href="/profile"]');
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
        event.preventDefault();

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

    showLoadIcon: function () {
        this.$('#loading-icon').show();
    },

    hideLoadIcon: function () {
        this.$('#loading-icon').hide();
    },

    // This method is used for all errors over the app
    displayError: function (level, msg) {
        var $errorBlock = this.$('#popup');

        var header;
        switch (level) {
            case 'error':
                header = 'ERROR:'
                break;
            case 'info':
                header = 'INFO:'
                break;
        }
        console.log(level, msg)

        $errorBlock.find('.header').text(header);
        $errorBlock.find('.message').text(msg);
        $errorBlock.fadeIn(300);
        setTimeout(function () {
            $errorBlock.fadeOut(300);
        }, 2000);
    },

    render: function () {
        this.$el.html(this.template({user: window.App.currentUser}));
    }
});
