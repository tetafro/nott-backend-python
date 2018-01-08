var Backbone = require('backbone');
var NotesCollection = require('../collections/Notes');

module.exports = Backbone.View.extend({
    collection: NotesCollection,
    el: function () {
        return $('#search-form');
    },

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

        key = this.$('input[name="search"]').val();
        this.collection.search(key);
    }
});
