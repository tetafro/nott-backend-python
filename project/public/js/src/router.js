var $ = require('jquery');
var Backbone = require('backbone');
var LoginView = require('./users/views/Login');
var RegisterView = require('./users/views/Register');
var NotesView = require('./notes/views/Page');
var AdminView = require('./admin/views/Page');
var ProfileView = require('./users/views/Profile');

module.exports = Backbone.Router.extend({
    routes: {
        'login': 'login',
        'register': 'register',
        '': 'notes',
        'notes': 'notes',
        'admin': 'admin',
        'users/:id': 'profile'
    },

    login: function () {
        new LoginView();
    },

    register: function () {
        new RegisterView();
    },

    notes: function () {
        new NotesView();
    },

    admin: function () {
        new AdminView();
    },

    profile: function (id) {
        new ProfileView(id);
    }
});
