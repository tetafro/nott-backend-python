var _ = require('underscore');
var Backbone = require('backbone');
var Config = require('../../config');

module.exports = Backbone.Model.extend({
    defaults: {
        id: null,
        title: null,
        text: null,
        html: null,
        notepad_id: null,
        created: null,
        updated: null,

        opened: false, // tab is opened (need for the view to fire close event)
        active: false // tab is active
    },
    // Interface fields, not stored in DB
    dontSync: [
        'html',
        'opened',
        'active'
    ],
    // To be able to determine what object type is current model
    type: 'note',
    idAttribute: 'id',
    urlRoot: Config.urls.api.notes,

    validate: function (attributes) {
        if (!attributes.title) {
            return 'Title cannot be empty';
        }
        if (attributes.title.length > 80) {
            return 'Title is too long';
        }
    },

    // Load from server or activate if already loaded
    open: function () {
        var that = this;

        // Model is already opened - make it's tab active
        if (that.get('opened')) {
            window.App.collections.editors.openOne(that);
        // Fetch model and open it in new tab
        } else {
            that.fetch({
                success: function () {
                    window.App.collections.editors.openOne(that);
                }
            });
        }
    },

    close: function () {
        if (!this.get('opened')) {
            return;
        }
        window.App.collections.editors.closeOne(this);
    },

    // Filter the data to send to the server
    save: function (attrs, options) {
        attrs || (attrs = _.clone(this.attributes));
        options || (options = {});

        attrs = _.omit(attrs, this.dontSync);
        options.data = JSON.stringify(attrs);

        // Proxy the call to the original save function
        return Backbone.Model.prototype.save.call(this, attrs, options);
    }
});
