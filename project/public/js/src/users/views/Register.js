var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var Config = require('../../config');
var RegisterTemplate = require('raw-loader!../templates/Register.html');

module.exports = Backbone.View.extend({
    tagName: 'div',
    attributes: {
        class: "page col-md-6 col-md-offset-3"
    },
    template: _.template(RegisterTemplate),

    events: {
        'click a.goto': 'goto',
        'click input[type="submit"]': 'register',
        'keypress input': 'register'
    },

    initialize: function () {
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

    validate: function () {
        var $username = this.$('input[name="username"]');
        var $email = this.$('input[name="email"]');
        var $password1 = this.$('input[name="password1"]');
        var $password2 = this.$('input[name="password2"]');

        var hasErrors = false;
        if ($username.val() == '') {
            this.addError('Username cannot be empty', $username);
            hasErrors = true;
        }
        if ($email.val() == '') {
            this.addError('Email cannot be empty', $email);
            hasErrors = true;
        }
        if ($password1.val() == '') {
            this.addError('Password cannot be empty', $password1);
            hasErrors = true;
        }
        if ($password1.val() != $password2.val()) {
            this.addError('Passwords do not match', $password2);
            hasErrors = true;
        }
        return hasErrors;
    },

    register: function (event) {
        var that = this;

        // Catch only pressing Enter
        if (event.type == 'keypress' && event.keyCode != 13) {
            return;
        }
        event.preventDefault();

        // Validate
        that.clearErrors();
        var hasErrors = that.validate();
        if (hasErrors) {
            return
        }

        var username = that.$('input[name="username"]').val();
        var email = that.$('input[name="email"]').val();
        var password1 = that.$('input[name="password1"]').val();
        var password2 = that.$('input[name="password2"]').val();

        // Register new user on backend, get auth token in response
        // and save it to local storage
        $.ajax({
            url: Config.urls.api.register,
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify({
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2
            }),
            success: function (response) {
                // Invalid response
                if (!('token' in response)) {
                    that.addError('Server did not provide token');
                    return;
                }

                window.App.login(response.token);
                Backbone.history.navigate('/', true);
            },
            error: function (response) {
                var data = response.responseJSON;

                // Invalid responses
                if (typeof data === 'undefined' || !('error' in data)) {
                    that.addError('Unexpected error');
                    return;
                }

                that.addError('Registration error: ' + data.error);
            }
        });
    },

    render: function () {
        this.$el.html(this.template());
        $('#content').html(this.el);
    }
});
