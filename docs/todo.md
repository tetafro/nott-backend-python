# TODO

* Compare Docker images as a base images for the app;
* Search;
* Hotkey for edit mode;
* Open note on creation;
* Sort list on any item creation;
* Validation in modal window;
* Test for making notepad for non-existing folder;
* Email confirmation;
* Password restore;
* Cascade delete for auth_user;
* Lists animations on moving/removing items;
* Add folder names to tabs;
* Admin panel:
    * Open/close registrations;
    * Remove/block users.
* Custom error pages (404, 500, etc) using nginx;
* Service usage statistics;
* OAuth using external services;
* Design [https://app.keeweb.info/](https://app.keeweb.info/);
* Testing;
* Log rotate;
* Drag'n'drop for all items.

# Bugs

* Opened notes are not destroyed on removing notes;
* Folders are not destoroyed when moving to the root;
* No csrf_failure on duplicate login send (for example on network errors);
* Tabs are destroyed on removing opened notepad.
