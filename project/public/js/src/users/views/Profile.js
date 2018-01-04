var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var User = require('../models/User');
var PageTemplate = require('raw-loader!../templates/Profile.html');

module.exports = Backbone.View.extend({
    model: User,
    tagName: 'div',
    template: _.template(PageTemplate),

    initialize: function () {
        this.model = window.App.currentUser;

        this.render();
    },

    render: function () {
        var data = this.model.toJSON();
        data.created = data.created.toLocaleString();
        data.updated = data.updated.toLocaleString();

        this.$el.html(this.template(data));
        $('#content').html(this.el);
    }
});
