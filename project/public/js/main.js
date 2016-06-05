require.config({
    paths: {
        // jquery: 'libs/jquery.min',
        jquery: 'libs/jquery',
        underscore: 'libs/underscore.min',
        backbone: 'libs/backbone.min',
        bootstrap: 'libs/bootstrap.min',
        trumbowyg: 'libs/trumbowyg.min'
    },
    shim : {
        'bootstrap': {
            'deps': ['jquery']
        },
        'trumbowyg': {
            'deps': ['jquery']
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