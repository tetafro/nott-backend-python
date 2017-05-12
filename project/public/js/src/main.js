require.config({
    paths: {
        jquery: '../libs/jquery.min',
        underscore: '../libs/underscore.min',
        backbone: '../libs/backbone.min',
        bootstrap: '../libs/bootstrap.min',
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }
});

require(
    ['app', 'views/AppView'],
    function (App, AppView) {
        App.init();

        // Render main view
        var appView = new AppView();
    }
);
