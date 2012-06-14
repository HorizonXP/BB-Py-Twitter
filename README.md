BB-Py Twitter
=============

A sample twitter application built using BB-Py
----------------------------------------------

This is a sample application built in Python using BB-Py for the BlackBerry
PlayBook. It allows a user to login to their twitter account via OAuth, and
view their own timeline, and their friends. The user can send a boilerplate
tweet about the BB-Py project, and can logout from the application. 

It its current form, the program is quite simplistic and crude. However, all of
the foundation is in place to create a fairly complete twitter app. 

### How to run
There are two branches in this sample, the master and desktop branches. 

To run on the Desktop, simply checkout the desktop branch and run:

    python main.py

And the sample app will run on your desktop, provided you have Python 3, Qt,
and PySide installed.

To run it on the BlackBerry PlayBook, checkout the master branch. Then, you
need to edit `build.sh` so that the `-debugToken` argument points to your own
debug token. Ensure that the first `source` command in the file is pointing to
the location where your NDK is installed. Next, edit `deploy.sh` so that your
device's IP address and password are specified. Make sure the `source` command
in this file points to the right place too. Then simply run the following
commands: 

    ./build.sh
    ./deploy.sh

At this point, you should see a BB-Py Twitter app icon on your PlayBook. If
you've installed the BB-Py libraries into your `shared/misc` folder, the app
should run. If you haven't installed these libraries, go ahead and do so.
