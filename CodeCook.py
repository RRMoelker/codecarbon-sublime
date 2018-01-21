# -*- coding: utf-8 -*-
import re
import sublime
import sublime_plugin

from .API import CodecookApi


class CodecookCommand(sublime_plugin.TextCommand):  # Codecook is not camel cased so action name is 'codecook' not 'code_cook'
    """
    Search and inserts snippets from CodeCook.io website.
    """

    def run(self, edit):
        """
        Initialise API and show search window
        """
        self.edit = edit
        self.init_api()
        if self.api:
            self.show_search_window()

    def init_api(self):
        """
        Retrieve user and package settings and start CodeCook api.
        """
        settings = self.view.settings()
        user = settings.get('cc_user')
        key = settings.get('cc_key')

        api_server = settings.get('cc_api_server', None)

        if user == None or key == None:
            sublime.error_message("Username and key need to be defined (keys: 'cc_user' and 'cc_key'). Go to CodeCook.io for an account and key")
            return

        self.api = CodecookApi()
        if api_server:
            self.api.configure(user, key, api_server)
        else:
            self.api.configure(user, key)

    def show_search_window(self):
        self.view.window().show_input_panel('Search', '', self.on_search_done, None, None)


    def on_search_done(self, query):
        """
        User has entered search query
            perform search,
            if len results == 0, try searching again
            else show list of concepts to choose from
        """
        # sublime.message_dialog("No search results, please try again.")
        search_results = self.api.search_concept(query)
        objects = search_results.get('data').get('snippets');

        if len(objects) == 0:
            sublime.message_dialog("No search results, please try again.")
            self.show_search_window()
        else:
            self.object_list = objects
            self.list = [x.get('name') for x in self.object_list]
            self.view.window().show_quick_panel(self.list, self.on_snippet_chosen)


    def on_snippet_chosen(self, index):
        """
        User has selected a snippet, insert it at cursor.
        """
        if index == -1: return # No selection, exit
        snippet_object = self.object_list[index]
        snippet_content = snippet_object.get('code')
        snippet_parameters = snippet_object.get('parameters')

        view = sublime.active_window().active_view()
        view.run_command(
            "insert_text_codecook_bypass_sublime_limitations", {
                'content': snippet_content,
                'parameters': snippet_parameters
            }
        )


class InsertTextCodecookBypassSublimeLimitationsCommand(sublime_plugin.TextCommand):
    """
    Inserts text, command required because plugin API is very very limited.
    Anything async in a TextCommand destroys the abbility to interact with the editor in that command.
    https://forum.sublimetext.com/t/how-to-run-part-of-my-plugin-in-the-second-thread-properly/18962
    """
    def run(self, edit, content, parameters):
        view_selection = self.view.sel()
        selection = view_selection[0]  # store selection

        # actually insert snippet content:
        # print("inserting: " + str(content))
        self.view.insert(edit, self.view.sel()[0].begin(), content)

        # Find first {{}} pattern and select multiple if available
        start = selection.a
        pattern = "\{\{\w+\}\}"
        first_match = self.view.find(pattern, start)
        if first_match != None:
            match_string = self.view.substr(first_match)
            match_regex = re.escape(match_string)
            matches = self.view.find_all(match_regex, )

            # Select {{}}
            view_selection.clear()
            for match in matches:
                view_selection.add(match)

