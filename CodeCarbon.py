# -*- coding: utf-8 -*-
import json
import re
import sublime
import sublime_plugin
import urllib

class CodecarbonApi:
    """
    Interfaces with codecarbon website to get concepts, methods and snippets
    """

    def __init__(self, username, key, api_url):
        self.username = username
        self.key      = key
        self.api_url  = api_url
    
    def get_authentication_params(self):
        """
        Returns authentication GET params for url
        """
        return "username="+str(self.username)+"&api_key="+str(self.key)

    # def get_concept_list(self):
    #     url = '/concept/?limit=100'
    #     return self.get_url_data(url, get_started=True)

    def search_concept(self, query):
        url = '/concept/search/?q=%s' % query
        return self.get_url_data(url, get_started=True)

    def get_concept_detail(self, id):
        url = '/concept/%d/' % id
        return self.get_url_data(url)

    def get_methods_detail(self, ids):
        """
        @ids is list of id values
        """
        url = '/method/set/%s/' % ";".join(map(str, ids))
        return self.get_url_data(url)

    def get_method_detail(self, id):
        url = '/method/%d/' % id
        return self.get_url_data(url)
        


    def get_url_data(self, url, get_started=False):
        """
        Retrieves data from REST url.
        Prepends api domain only relative path needed.
        @get_started means the url already contains ?, if authentication credentials are used they are appended using &.
        """
        get_symbol = "&" if get_started else "?"
        url = self.api_url + url + get_symbol + self.get_authentication_params()
        # print "opening: " + url
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        return data


required_settings = ['cc_user', 'cc_key', 'cc_api_url', ]

class CodecarbonCommand(sublime_plugin.TextCommand): # Codecarbon is not camelcased so action name is 'codecarbon' not 'code_carbon'
    """
    Search and inserts snippets from CodeCarbon.io website.
    """

    def run(self, edit):
        """
        Initialise api and show search window
        """
        self.init_api()
        if self.api:
            self.show_search_window()

    def init_api(self):
        """
        Retrieve user and package settings and start CodeCarbon api.
        """
        settings = self.view.settings()
        user = settings.get('cc_user')
        key = settings.get('cc_key')
        api_url = settings.get('cc_api_url')
        if user == None or key == None:
            sublime.error_message("Username and key need te defined (keys: 'cc_user' and 'cc_key'). Go to CodeCarbon.io for an account and key")
            return
        if api_url == None:
            sublime.error_message("Not all settings found. Did you set:\n" + "\n".join(required_settings))
            return
        self.api = CodecarbonApi(user, key, api_url)
            
    def show_search_window(self):
        self.view.window().show_input_panel('Search', '', self.on_search_done, None, None)

    def on_search_done(self, query):
        """
        User has entered search query
            perform search,
            if len results == 0, try searching again
            else show list of concepts to choose from
        """
        search_results = self.api.search_concept(query)
        objects = search_results.get('objects')
        if len(objects) == 0:
            sublime.message_dialog("No search results, please try again.")
            self.show_search_window()
        else:
            self.object_list = objects
            self.list = [x.get('name') for x in self.object_list]
            self.view.window().show_quick_panel(self.list, self.on_concept_chosen)



    def on_concept_chosen(self, index):
        """
        User has chosen a concept, get a list of methods to choose from and prompt user again.
        """
        if index == -1: return # No selection, exit

        concept_object = self.object_list[index]
        concept_id = concept_object.get('id')
        concept_detail = self.api.get_concept_detail(concept_id)
        method_list = concept_detail.get('methods')
        method_ids = [x.get('id') for x in method_list]
        method_details = self.api.get_methods_detail(method_ids)
        self.object_list = method_details.get('objects')
        self.list = []
        for obj in self.object_list:
            item = obj.get('main_language')
            title = obj.get('title')
            if title:
                item += "- " + title
            self.list.append(item)
        self.view.window().show_quick_panel(self.list, self.on_method_chosen)


    def on_method_chosen(self, index):
        """
        User has selected a method to insert, get all snippets for that method and prompt choice.
        """
        if index == -1: return # No selection, exit

        method_id = self.object_list[index].get('id')
        method_detail = self.api.get_method_detail(method_id)
        
        self.object_list = method_detail.get('snippets')
        self.list = [x.get('content')[:50] for x in self.object_list]
        self.view.window().show_quick_panel(self.list, self.on_snippet_chosen)


    def on_snippet_chosen(self, index):
        """
        User has selected a snippet, insert it at cursor.
        """
        if index == -1: return # No selection, exit
        snippet_object = self.object_list[index]
        snippet_content = snippet_object.get('content')
        self.insert_code(snippet_content)


    def insert_code(self, content):
        view_selection = self.view.sel()
        selection = view_selection[0] #store selection

        #actually insert snippet content:
        self.view.run_command(
                "insert_my_text", {"args":
                {'text': content}})

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