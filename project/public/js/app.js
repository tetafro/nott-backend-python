define(
    [
        'jquery', 'underscore', 'backbone', 'bootstrap', 'trumbowyg'
    ],
    function (
        $, _, Backbone
    ) {
        // Get CSRF token for making AJAX requests
        var getCSRF = function () {
            var token = null;
            if (document.cookie) {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = $.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, 10) == 'csrftoken=') {
                        token = decodeURIComponent(cookie.substring(10));
                        break;
                    }
                }
            }
            return token;
        };

        var App = {
            init: function() {
                var token = getCSRF();

                // Set CSRF token for all Backbone's requests
                var oldSync = Backbone.sync;
                Backbone.sync = function (method, model, options) {
                    options.beforeSend = function (xhr) {
                        xhr.setRequestHeader('X-CSRFToken', token);
                    };
                    return oldSync(method, model, options);
                };

                return this;
            },

            displayError: function (msg) {
                console.log(msg);
            }
        };

        return App;
    }
);