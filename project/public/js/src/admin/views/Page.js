var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var PageTemplate = require('raw-loader!../templates/Page.html');

module.exports = Backbone.View.extend({
    tagName: 'div',
    template: _.template(PageTemplate),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.html(this.template());
        $('#content').html(this.el);
    }
});
