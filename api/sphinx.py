__author__ = 'aimsam'
# coding=utf-8
from vd import settings
from sphinxapi import SphinxClient
import util

class Sphinx(object):

    def __init__(self):
        self.client = SphinxClient()
        self.client.SetServer(settings.SPHINX['host'], settings.SPHINX['port'])

    #get author update number by unix_time_stamp
    def get_author_update_number(self, follow_dict):
        try:
#            follow_dict = util.deleteUnicode(follow_dict)
            arr = follow_dict.split('))')
            for row in arr:
                split = row.split('**')
                if len(split) == 2:
                    id = split[0]
                    unix_time_stamp = split[1].split("--")[1].split('__')[0]
                    self.client.ResetFilters()
                    self.client.SetFilterRange("date_added", int(unix_time_stamp), 9999999999)
                    self.client.AddQuery(id, "video")
            query = self.client.RunQueries()

            result = []
            for row in query:
                result.append(row["total"])
            return "{'code': 500, 'message': 'success', 'list':" + str(result) + "}"
        except Exception:
            return "{'code': 502, 'message' : 'unknown exception'}"

    def search(self, words):
        return None

