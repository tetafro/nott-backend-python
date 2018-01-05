var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var ErrorTemplate = require('raw-loader!../templates/Error.html');

module.exports = Backbone.View.extend({
    el: function () {
        return $('#content');
    },
    template: _.template(ErrorTemplate),

    initialize: function (message) {
        this.render(message);
    },

    render: function (message) {
        this.$el.html(this.template({message: message}));
    }
});
