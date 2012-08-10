=============================================
Manage a diffusion email list with AlwaysData
=============================================

This is a little Django App, that help to manage a list of contacts,
sort them in diffusion email addresses.

Features
========

* Copy/Paste import from Excel or text files.
* Auto configure the AlwaysData sieve script
* Stop SPAM
* Define private diffusion addresses

Install
=======

::

    $ make virtualenv
    $ source apps/bin/activate
    $ make upgrade

Configure the `settings.py` using `settings.py.example`

::

    $ make syncdb
    $ make runserver

You must to configure your AlwaysData access.
When defining a new email address, you have to setup it AlwaysData email ID::

    https://admin.alwaysdata.com/email/EMAIL_ID/

Licence
=======

This project is released under the BSD Licence, see LICENCE file for
futher informations.

**Please fork me**

Authors
=======

* Rémy HUBSCHER <remy.hubscher@ionyse.com>

Wishlist
========

* Create and configure a new email address in the AlwaysData admin when adding a group
* Add a boolean to ask if the diffusion should be private
* Be able to configure the diffusion list access
* Create a link for subscription/unsubscription and add it at the end of a mail

Tags
====

Django, Python, Email, AlwaysData, Diffusion, List, Mailing, Contacts management
