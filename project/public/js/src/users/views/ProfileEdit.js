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
        var href = event.currentTarget.getAttribute("href");
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
        that.model.save(
            {
                email: email
            },
            {
                success: function (model, response) {
                    Backbone.history.navigate(Config.urls.pages.profile, true);
                },
                error: function (model, response) {
                    console.log(response)
                    var data = response.responseJSON;

                    // Invalid responses
                    if (typeof data === 'undefined' || !('error' in data)) {
                        that.addError('Unexpected error');
                        return;
                    }

                    that.addError('Error: ' + data.error);
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
