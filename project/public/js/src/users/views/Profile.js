var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var User = require('../models/User');
var PageTemplate = require('raw-loader!../templates/Profile.html');

module.exports = Backbone.View.extend({
    model: User,
    el: function () {
        return $('#content');
    },
    template: _.template(PageTemplate),

    initialize: function () {
        this.model = window.App.currentUser;
        window.App.views.page = this;
        this.render();
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
    }
});
