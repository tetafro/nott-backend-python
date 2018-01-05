var _ = require('underscore');
var Backbone = require('backbone');
var Note = require('../models/Note');
var ModalView = require('../views/Modal');
var NoteTemplate = require('raw-loader!../templates/Note.html');

module.exports = Backbone.View.extend({
    model: Note,
    tagName: 'li',
    attributes: function () {
        return {
            'data-type': 'note',
            'data-id': this.model.get('id')
        };
    },
    template: _.template(NoteTemplate),

    events: {
        'click .item': 'open',
        'click .edit': 'showModal',
        'click .del': 'showModal'
    },

    initialize: function () {
        this.listenTo(this.model, 'change:title', this.rename);
        this.listenTo(this.model, 'change:active', this.onChangeActive);
        this.listenTo(this.model, 'change:notepad_id', this.onMove);
        this.listenTo(this.model, 'request', this.onAjaxStart);
        this.listenTo(this.model, 'sync', this.onAjaxComplete);
        this.listenTo(this.model, 'error', this.onError);
        this.listenTo(this.model, 'destroy', this.onDestroy);

        this.render();
    },

    onAjaxStart: function () {
        window.App.views.base.showLoadIcon();
    },

    onAjaxComplete: function () {
        window.App.views.base.hideLoadIcon();
    },

    onError: function (model, error) {
        window.App.views.base.hideLoadIcon();
        window.App.views.base.displayError('error', error);
    },

    // Remove note view when moving, because only one notepad
    // can be opened at a time so there is no place to move
    // this view
    onMove: function () {
        this.remove();
    },

    onDestroy: function () {
        window.App.views.base.hideLoadIcon();
        this.remove();
    },

    open: function () {
        this.model.open();
    },

    // Change view when element activated/deactivated
    onChangeActive: function () {
        this.$el.toggleClass('active');
    },

    // Modal window with details for CRUD operation
    showModal: function (event) {
        // Since lists are nested, clicking on child element
        // is propagating to all parents. It shouldn't happen.
        event.stopPropagation();

        if ($(event.currentTarget).hasClass('edit')) {
            window.App.views.page.showModal({
                model: this.model,
                action: 'edit'
            });
        } else if ($(event.currentTarget).hasClass('del')) {
            window.App.views.page.showModal({
                model: this.model,
                action: 'delete'
            });
        }
    },

    rename: function () {
        this.$('> div > a > span').html(this.model.get('title'));
    },

    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        // In case of rendering model, which is opened in tabs
        if (this.model.get('active')) {
            this.$el.addClass('active');
        }
    }
});
