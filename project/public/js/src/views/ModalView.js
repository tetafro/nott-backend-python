define(
    [
        'underscore', 'backbone',
        'app',
        'templates/ModalTemplate'
    ],
    function (
        _, Backbone,
        App,
        ModalTemplate
    ) {
        var ModalView = Backbone.View.extend({
            model: null,
            tagName: 'div',
            id: 'modal-crud',
            className: 'modal fade',
            attributes: {
                tabindex: '-1',
                role: 'dialog'
            },
            template: _.template(ModalTemplate),

            events: {
                'click [name="save"]': 'submit',
                'click [name="delete"]': 'submit',
                'keypress [name="title"]': 'submit',
                'click [name="type"]': 'onChangeType',
                'hidden.bs.modal': 'remove' // built-in remove
            },

            initialize: function (options) {
                this.options = options;
                this.listenTo(this.model, 'sync', this.hide);
                this.render();
            },

            show: function () {
                this.$el.modal('show');
            },

            hide: function () {
                this.$el.modal('hide');
            },

            submit: function (event) {
                // Catch only pressing Enter
                if (event.type == 'keypress') {
                    if (event.keyCode == 13) {
                        event.preventDefault();
                    } else {
                        return;
                    }
                }

                var that = this;
                var parentId = parseInt(that.$('select[name="move"]').val()) || null;
                var elementTitle = that.$('input[name="title"]').val();
                var elementType = that.$('input[name="type"]:checked').val();
                var collection;

                switch (elementType) {
                    case 'folder':
                        collection = App.foldersCollection;
                        break;
                    case 'notepad':
                        collection = App.notepadsCollection;
                        break;
                    case 'note':
                        collection = App.notesCollection;
                        break;
                }

                switch (that.options.action) {
                    case 'create':
                        that.model = collection.createOne(elementTitle, parentId);
                        // Reassign events
                        that.listenTo(this.model, 'sync', this.hide);
                        that.listenTo(this.model, 'error', this.displayError);
                        break;
                    case 'edit':
                        collection.editOne(that.model, elementTitle, parentId);
                        break;
                    case 'delete':
                        collection.deleteOne(that.model);
                        break;
                }
            },

            onChangeType: function (event) {
                var $firstOption = this.$('select > option').first();
                var type = this.$('[name="type"]:checked').val();

                // Remove blank option for notepads - they must have parent folder
                if (type == 'folder' && $firstOption.val() != '') {
                    $('<option></option>').insertBefore($firstOption);
                } else if (type == 'notepad' && $firstOption.val() == '') {
                    $firstOption.remove();
                }
            },

            displayError: function (model, msg) {
                var $errorBlock = this.$('.error-message');

                // Text to show
                text = 'Something went wrong';
                if (typeof msg == 'string') {
                    text = msg;
                } else if (typeof msg == 'object') {
                    if (msg.responseJSON) {
                        text = msg.responseJSON.error;
                    }
                }

                this.$('.error-message').html(text);
            },

            render: function () {
                var that = this;
                var windowTitle;
                var elementType;

                if (that.options.action == 'create') {
                    elementType = that.options.type;
                    windowTitle = 'Create ' + elementType;
                } else if (that.options.action == 'edit') {
                    elementType = that.model.type;
                    windowTitle = 'Edit ' + elementType;
                } else if (that.options.action == 'delete') {
                    elementType = that.model.type;
                    windowTitle = 'Delete ' + elementType;
                }

                // Get list of all folders
                var selected;
                var parentId;
                var elementsList = '<option></option>'; // empty element for root

                if (that.options.parentId) {
                    parentId = that.options.parentId;
                } else if (elementType == 'folder') {
                    parentId = that.model ? that.model.get('parent_id') : null;
                } else if (elementType == 'notepad') {
                    parentId = that.model ? that.model.get('folder_id') : null;
                } else if (elementType == 'note') {
                    parentId = App.notepadsCollection.active.get('id');
                }

                var collection;
                if (elementType == 'folder' || elementType == 'notepad') {
                    collection = App.foldersCollection;
                } else {
                    collection = App.notepadsCollection;
                }

                var prevParentId;
                collection.each(function (element) {
                    // TODO: Skip not only current model, but all it's children
                    // to avoid loops.
                    if (that.model && (
                            element.get('id') == that.model.get('id') ||  // skip current model
                            element.get('id') == prevParentId // skip all children of current model
                        )
                    ) {
                        prevParentId = element.get('id');
                        return true;
                    } else if (element.get('id') == parentId) {
                        selected = 'selected';
                    } else {
                        selected = '';
                    }

                    elementsList +=
                        '<option value=' + element.get('id') + ' ' + selected + '>' +
                            element.get('title') +
                        '</option>';
                });

                that.$el.html(that.template({
                    action: that.options.action,
                    windowTitle: windowTitle,
                    elementTitle: that.model ? that.model.get('title') : '',
                    elementType: elementType,
                    elementsList: elementsList
                }));

                $('#app').append(that.$el);
                that.show();
            }
        });

        return ModalView;
    }
);
