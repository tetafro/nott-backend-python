var $ = require('jquery');
var Backbone = require('backbone');
var LoginView = require('./users/views/Login');
var RegisterView = require('./users/views/Register');
var NotesView = require('./notes/views/Page');
var ProfileView = require('./users/views/Profile');

module.exports = Backbone.Router.extend({
    routes: {
        'login': 'login',
        'register': 'register',
        '': 'notes',
        'profile': 'profile'
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
        'profile': 'redirectItNotAuthenticated'
    },

    // Filters for URL to be applied after routing
    after: {
        '*any': function (fragment) {
            window.App.views.base.nav(fragment);
        }
    },

    // Redirect to root if current user is already authenticated
    redirectIfAuthenticated: function () {
        if (window.App.isAuthenticated()) {
            Backbone.history.navigate('/', true);
            return false;
        }
        return true;
    },

    // Redirect to login if current user is not authenticated
    redirectItNotAuthenticated: function () {
        if (!window.App.isAuthenticated()) {
            Backbone.history.navigate('login', true);
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
    }
});
