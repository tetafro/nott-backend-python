var Backbone = require('backbone');
var App = require('../app');
var NotesCollection = require('../collections/NotesCollection');

module.exports = Backbone.View.extend({
    collection: NotesCollection,
    el: $('#search-form'),

    events: {
        'click span.search': 'submit',
        'keypress [name="search"]': 'submit'
    },

    initialize: function () {},

    submit: function (event) {
        // Catch only pressing Enter
        if (event.type == 'keypress') {
            if (event.keyCode == 13) {
                event.preventDefault();
            } else {
                return;
            }
        }

        key = this.$('input[name="search"]').val();;
        this.collection.search(key);
    }
});
