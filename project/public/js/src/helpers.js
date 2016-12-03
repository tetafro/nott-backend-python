define(
    [
        'jquery'
    ],
    function (
        $
    ) {
        var Helpers = {
            // Get CSRF token for making AJAX requests
            getCSRF: function () {
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
            },

            // Make a tree from plain array and
            // do something with each element
            processTree: function (collection, parentIdField, process) {
                var len = collection.length;

                var processChildren = function (parentElement) {
                    process(parentElement);

                    var element;
                    for (var i = 0; i < len; i++) {
                        element = collection.at(i);
                        if (parentElement.get('id') == element.get(parentIdField)) {
                            processChildren(element);
                        }
                    };
                };

                var element;
                for (var i = 0; i < len; i++) {
                    element = collection.at(i);
                    if (!element.get(parentIdField)) {
                        processChildren(element);
                    }
                };
            }
        };

        return Helpers;
    }
);
