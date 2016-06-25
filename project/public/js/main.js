require.config({
    paths: {
        jquery: 'libs/jquery.min',
        underscore: 'libs/underscore.min',
        backbone: 'libs/backbone.min',
        bootstrap: 'libs/bootstrap.min',
        trumbowyg: 'libs/trumbowyg.min',
        trumbowygColors: 'libs/trumbowyg-colors.min'
    },
    shim : {
        'bootstrap': {
            'deps': ['jquery']
        },
        'trumbowyg': {
            'deps': ['jquery']
        },
        'trumbowygColors': {
            'deps': ['jquery', 'trumbowyg']
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