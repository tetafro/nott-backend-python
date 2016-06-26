define(
    [
        'jquery', 'backbone',
        'collections/NotesCollection',
        'views/NoteView'
    ],
    function (
        $, Backbone,
        NotesCollection,
        NoteView
    ) {
        var NotesCollectionView = Backbone.View.extend({
            collection: NotesCollection,
            el: $('.sidebar-second .nav-sidebar'),

            initialize: function () {
                this.listenTo(this.collection, 'add', this.onAdd);
                // this.listenTo(this.collection, 'reset', this.render);
                this.listenTo(this.collection, 'rerender', this.render);
                this.render();
            },

            createOne: function () {
                var that = this;

                // Catch only pressing Enter
                if (event.type == 'keypress') {
                    if (event.keyCode == 13) {
                        event.preventDefault();
                    } else {
                        return;
                    }
                }

                var $input = $(event.target).closest('form').find('input'),
                    title = $input.val();

                that.collection.createOne(title);
            },

            onAdd: function (note) {
                var noteView = new NoteView({model: note});
                this.$el.append(noteView.$el);
            },

            render: function() {
                var that = this;

                // Clear list of notes
                that.$el.empty();

                var note,
                    noteView;

                for (var i = 0; i < that.collection.length; i++) {
                    note = that.collection.at(i);
                    noteView = new NoteView({model: note});

                    that.$el.append(noteView.$el);
                };

                $('.search-form').hide();
            }
        });

        return NotesCollectionView;
    }
);