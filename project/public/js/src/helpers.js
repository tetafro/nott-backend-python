var $ = require('jquery');

module.exports = {
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
        var processChildren = function (element, lvl) {
            process(element, lvl);
            collection.each(function (el) {
                if (element.get('id') == el.get(parentIdField)) {
                    processChildren(el, lvl+1);
                }
            })
        };

        collection.each(function (element) {
            if (!element.get(parentIdField)) {
                processChildren(element, 0);
            }
        });
    }
};
