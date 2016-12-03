define(
    [
        'underscore', 'backbone',
        'app', 'helpers',
        'templates/ModalTemplate'
    ],
    function (
        _, Backbone,
        App, Helpers,
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

            getElementsList: function (elementType) {
                var that = this;
                var parentIdField = 'parent_id';
                var parentId;
                switch (elementType) {
                    case 'folder':
                        parentId = that.model ? that.model.get('parent_id') : null;
                        break;
                    case 'notepad':
                        parentId = that.model ? that.model.get('folder_id') : null;
                        break;
                    case 'note':
                        parentId = App.notepadsCollection.active.get('id');
                        break;
                }

                // Rewrite parentId if it's defined in options
                if (that.options.parentId) {
                    parentId = that.options.parentId;
                }

                // TODO: Skip current model and all of it's children to avoid loops.
                var $elementsList = $('<select name="move" class="form-control"></select>')
                $elementsList.append('<option></option>'); // empty element for root
                Helpers.processTree(App.foldersCollection, parentIdField, function (folder, lvl) {
                    var text = '--'.repeat(lvl) + ' ' + folder.get('title');
                    var selected = '';
                    if (elementType != 'note' && folder.get('id') == parentId) {
                        selected = 'selected';
                    }
                    var $folder = $(`
                        <option value=${folder.get('id')} ${selected}>
                            ${text}
                        </option>
                    `);
                    $elementsList.append($folder);

                    // Add notepads to the tree
                    if (elementType == 'note') {
                        $folder.prop('disabled', true);
                        App.notepadsCollection.each(function (notepad) {
                            if (notepad.get('folder_id') == folder.get('id')) {
                                selected = notepad.get('id') == parentId ? 'selected' : '';
                                text = '--'.repeat(lvl+1) + ' ' + notepad.get('title');
                                $folder.append(`
                                    <option value=${notepad.get('id')} ${selected}>
                                        ${text}
                                    </option>
                                `);
                            }
                        });
                    }
                });

                return $elementsList.html();
            },

            render: function () {
                var that = this;

                var windowTitle;
                var elementType;
                switch (that.options.action) {
                    case 'create':
                        elementType = that.options.type;
                        windowTitle = 'Create ' + elementType;
                        break;
                    case 'edit':
                        elementType = that.model.type;
                        windowTitle = 'Edit ' + elementType;
                        break;
                    case 'delete':
                        elementType = that.model.type;
                        windowTitle = 'Delete ' + elementType;
                        break;
                }

                var elementsList = that.getElementsList(elementType);

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
