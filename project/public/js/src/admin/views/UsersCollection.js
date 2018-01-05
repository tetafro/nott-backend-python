var _ = require('underscore');
var $ = require('jquery');
var Backbone = require('backbone');
var UsersCollection = require('../../users/collections/Users');
var UserView = require('../views/User');
var UsersCollectionTemplate = require('raw-loader!../templates/UsersCollection.html');

module.exports = Backbone.View.extend({
    collection: UsersCollection,
    el: function () {
        return $('#tab-users');
    },
    template: _.template(UsersCollectionTemplate),

    initialize: function () {
        this.collection.fetch();
        this.render();
    },

    render: function () {
        this.$el.html(this.template());

        var tbody = this.$('tbody')
        this.collection.each(function (user) {
            var userView = new UserView({model: user});
            tbody.append(userView.$el);
        });
    }
});
