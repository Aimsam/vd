__author__ = 'aimsam'
# coding=utf-8
from vd import settings
from sphinxapi import SphinxClient

class Sphinx(object):

    def __init__(self):
        self.client = SphinxClient()
        self.client.SetServer(settings.SPHINX['host'], settings.SPHINX['port'])

    #get author update number by unix_time_stamp
    def get_author_update_number(self, author_ids, unix_time_stamp):
        print unix_time_stamp
        self.client.SetFilterRange("ppp", unix_time_stamp, 9999999999)
        for author_id in author_ids:
            self.client.AddQuery(author_id, "video")
        query = self.client.RunQueries()
        result = []
        if query is not None:
            for row in query:
                result.append(row["total"])
        return result

    def search(self, words):
        return None

