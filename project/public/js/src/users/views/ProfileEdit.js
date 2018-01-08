var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var Config = require('../../config');
var User = require('../models/User');
var PageTemplate = require('raw-loader!../templates/ProfileEdit.html');

module.exports = Backbone.View.extend({
    model: User,
    el: function () {
        return $('#content');
    },
    template: _.template(PageTemplate),

    events: {
        'click a.goto': 'goto',
        'click button[type="submit"]': 'submit'
    },

    initialize: function () {
        this.model = window.App.currentUser;
        window.App.views.page = this;
        this.render();
    },

    goto: function (event) {
        event.preventDefault();
        var href = event.currentTarget.getAttribute('href');
        Backbone.history.navigate(href, true);
    },

    addError: function (msg, $element) {
        if (typeof $element !== 'undefined') {
            $element.closest('.form-group').addClass('has-error');
        }
        this.$('.auth-errors').html(
            this.$('.auth-errors').html() +
            '<p>' + msg + '</p>'
        );
    },

    clearErrors: function () {
        this.$('.form-group').removeClass('has-error');
        this.$('.auth-errors').text('');
    },

    submit: function (event) {
        var that = this;

        event.preventDefault();

        that.clearErrors();

        var email = that.$('input[name="email"]').val();
        var password = that.$('input[name="password"]').val();
        that.model.save(
            {
                email: email,
                password: password
            },
            {
                success: function (model, response) {
                    Backbone.history.navigate(Config.urls.pages.profile, true);
                },
                error: function (model, response) {
                    var data = response.responseJSON;

                    // Invalid responses
                    if (typeof data === 'undefined' || !('error' in data)) {
                        that.addError('Unexpected error');
                        return;
                    }

                    that.addError('Error: ' + data.error);
                },
                complete: function () {
                    // Clear model's password field
                    // NOTE: It will not be rewritten on backend on next
                    // sync, because password cannnot be empty
                    that.model.set('password', '');
                }
            }
        );
    },

    render: function () {
        var data = this.model.toJSON();
        data.created = data.created.toLocaleString();
        data.updated = data.updated.toLocaleString();

        this.$el.html(this.template(data));
    }
});
