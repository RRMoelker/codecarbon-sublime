codecarbon-sublime
==================

CodeCarbon plugin for sublime text. Allows for insertion of code snippets from the website [CodeCarbon.io](http://codecarbon.io/) directly into sublime text.

## Important
This plugin is still *under development*. And an *user account* on CodeCarbon.io is *needed* for api authentication.


## Install
This package is not (yet) available in package control. The easiest install method is cloning the repo directly into your packages folder. To do so:

1. Go to your packages folder, if you do not know where it is, open Sublime and select Preferences -> Browse packages in the top menu.
1. Clone the repository or extract the zip in the packages folder.

## Configuration
An api key and user account are needed to use this plugin. Open the user settings by selecting Preferences > Settings - User in the top menu. Add the following lines to the end of the file:

    "cc_user": "<username>",
    "cc_key": "<apikey>"

Where `<username>` and `<apikey>` are replaced by your personal credentials. The result will probably look like:

    {
      <other setting>,
      <other settings>,
      "cc_user": "*********",
      "cc_key": "******************"
    }

## Usage
Every time you wish to insert a code snippet you need to start the plugin and then browse to the desired snippet. There are two ways to start the plugin.

1. Using the command pallete, ctrl+shift+p or cmd+shift+p opens the command pallete. Type codecarbon and press enter to select the CodeCarbon plugin.
1. Using the shortcut defined in the installation, default is ctrl+shift+x

Once the plugin is started you can start typing and press enter to search for a concept. Once navigated through the options the snippet will be inserted at the cursor position.
