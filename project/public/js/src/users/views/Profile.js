var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var PageTemplate = require('raw-loader!../templates/Profile.html');

module.exports = Backbone.View.extend({
    tagName: 'div',
    template: _.template(PageTemplate),

    initialize: function (id) {
        this.render(id);
    },

    render: function (id) {
        this.$el.html(this.template({id: id}));
        $('#content').html(this.el);
    }
});
