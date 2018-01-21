codecook-sublime
==================

CodeCook plugin for sublime text. Allows for insertion of code snippets from the website [CodeCook.io](http://codecook.io/) directly into sublime text.


![Plugin impression](https://raw.githubusercontent.com/RRMoelker/codecook-sublime/master/codecook_sublimeplugin_impression.png)

## Important
This plugin is still *under development*. You need sublime text *version 3* for it to function. And an *user account* on CodeCook.io is *needed* for api authentication.


## Install
This package is not (yet) available in package control. The easiest install method is cloning the repo directly into your packages folder. To do so:

1. Go to your packages folder, if you do not know where it is, open Sublime and select Preferences -> Browse packages in the top menu.
1. Clone the repository or extract the zip in the packages folder.
1. Rename the folder to CodeCook, after this step the folder structure should be {package_folder}/CodeCook/{files}. 

## Configuration
An api key and user account are needed to use this plugin. Open the user settings by selecting Preferences > Settings - User in the top menu. Add the following lines to the end of the file:

    "cc_user": "<username>",
    "cc_key": "<apikey>"

Where `<username>` and `<apikey>` are replaced by your personal credentials. The result will probably look like:

    {
      ...
      "cc_user": "*********",
      "cc_key": "******************"
    }

## Usage
Every time you wish to insert a code snippet you need to start the plugin and then browse to the desired snippet. There are two ways to start the plugin.

1. Using the command palette, ctrl+shift+p or cmd+shift+p opens the command palette. Type codecook and press enter to select the CodeCook plugin.
1. Using the shortcut defined in the installation, default is ctrl+shift+x

Once the plugin is started you can start typing and press enter to search for a concept. Once navigated through the options the snippet will be inserted at the cursor position.

## Requirements

* Sublime Text 3

## Development

To develop and test app, symlink from packages folder to codecook-sublime folder naming the link `CodeCook`.

Sublime Text packages folder can be openened from "preferences > browse packages" or something of the sorts.

NOTE:
Beware that Sublime will not reload properly:
"Sublime Text will reload topmost Python modules as they change (perhaps because you are editing a .py file within Packages). By contrast, Python subpackages won’t be reloaded automatically, and this can lead to confusion while you’re developing plugins. Generally speaking, it’s best to restart Sublime Text after you’ve made changes to plugin files, so all changes can take effect."
src: http://docs.sublimetext.info/en/latest/reference/plugins.html#automatic-plugin-reload

**Probably need build tool that creates a single file from normal Python code (eventually)**.


Also use: https://packagecontrol.io/packages/AutomaticPackageReloader
!!!Even with AutomaticPackageReloader it still requires saving the entire import tree!!!


