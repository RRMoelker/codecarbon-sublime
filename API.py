# -*- coding: utf-8 -*-
import json
import urllib

from .helpers import singleton

# cc_api_server = "https://codecook.io"
# cc_api_path   = "/api/dev"
cc_api_server = "http://localhost:4000"
cc_api_path   = "/graphql"

@singleton
class CodecookApi:
    """
    Interfaces with CodeCook.io website to get concepts, methods and snippets
    """

    def configure(self, username, key, api_server=cc_api_server, api_path=cc_api_path):
        self.username   = username
        self.key        = key
        # self.api_server = api_server
        # self.api_path   = api_path
        self.api_url    = api_server + api_path

    def search_concept(self, query):
        graphqlQuery =  """{
            snippets(query: \"%s\") {
                name
                code,
                parameters {
                  name,
                  default
                }
            }
        }""" % (query)
        return self.query_api(graphqlQuery)


    def query_api(self, graphqlQuery):
        """
        Retrieves data from Graphql API,
        each request is authenticated using authorization header.
        """
        data = {
            'query': graphqlQuery
        }
        # base64string = '%s:%s' % (self.username, self.key)
        headers = {
            'Content-Type': 'application/json'
            # 'Authorization': "ApiKey %s" % base64string,
        }

        jsonData = json.dumps(data).encode('utf8')

        req = urllib.request.Request(self.api_url,
            data=jsonData,
            method='POST',
            headers=headers
        )
        with urllib.request.urlopen(req) as response:
            charset = response.info().get_param('charset', 'utf8')
            raw = response.read()
            data = json.loads(raw.decode(charset));
            return data
