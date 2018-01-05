var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var User = require('../../users/models/User');
var UserTemplate = require('raw-loader!../templates/User.html');

module.exports = Backbone.View.extend({
    model: User,
    tagName: 'tr',
    template: _.template(UserTemplate),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
    }
});
