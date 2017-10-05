module.exports = {
    // Make a tree from plain array and
    // do something with each element
    processTree: function (collection, parentIdField, process) {
        var processChildren = function (element, lvl) {
            process(element, lvl);
            collection.each(function (el) {
                if (element.get('id') == el.get(parentIdField)) {
                    processChildren(el, lvl+1);
                }
            });
        };

        collection.each(function (element) {
            if (!element.get(parentIdField)) {
                processChildren(element, 0);
            }
        });
    }
};
