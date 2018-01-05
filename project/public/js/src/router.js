var $ = require('jquery');
var Backbone = require('backbone');
var LoginView = require('./users/views/Login');
var RegisterView = require('./users/views/Register');
var NotesView = require('./notes/views/Page');
var ProfileView = require('./users/views/Profile');
var ProfileEditView = require('./users/views/ProfileEdit');
var AdminView = require('./admin/views/Page');
var ErrorView = require('./base/views/Error');

module.exports = Backbone.Router.extend({
    routes: {
        'login': 'login',
        'register': 'register',
        '': 'notes',
        'profile': 'profile',
        'profile/edit': 'editProfile',
        'admin': 'admin',
        '*any': 'default'
    },

    initialize: function () {
        Backbone.history.start({pushState: true});
    },

    // Filters for URL to be applied before routing
    before: {
        'login': 'redirectIfAuthenticated',
        'register': 'redirectIfAuthenticated',
        '': 'redirectItNotAuthenticated',
        'notes': 'redirectItNotAuthenticated',
        'profile': 'redirectItNotAuthenticated',
        'profile/edit': 'redirectItNotAuthenticated',
        'admin': 'redirectItNotAdmin'
    },

    // Filters for URL to be applied after routing
    after: {
        '*any': function (fragment) {
            window.App.views.base.nav(fragment);
        }
    },

    // Redirect to root if current user is already authenticated
    redirectIfAuthenticated: function () {
        if (window.App.currentUser != null) {
            Backbone.history.navigate('/', true);
            return false;
        }
        return true;
    },

    // Redirect to login if current user is not authenticated
    redirectItNotAuthenticated: function () {
        if (window.App.currentUser == null) {
            Backbone.history.navigate('login', true);
            return false;
        }
        return true;
    },

    // Redirect to root if current user is not admin
    redirectItNotAdmin: function () {
        var role = window.App.currentUser.get('role').name;
        if (role != 'admin') {
            Backbone.history.navigate('/', true);
            return false;
        }
        return true;
    },

    // Handlers

    login: function () {
        new LoginView();
    },

    register: function () {
        new RegisterView();
    },

    notes: function () {
        new NotesView();
    },

    profile: function (id) {
        new ProfileView(id);
    },

    editProfile: function (id) {
        new ProfileEditView(id);
    },

    admin: function () {
        new AdminView();
    },

    default: function () {
        new ErrorView('Page not found');
    }
});
