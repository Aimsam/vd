__author__ = 'aimsam'
import re

def deleteUnicode(unicode_str):
    result = re.sub(r"u'", "'", unicode_str)
    result = str(result)
    result = re.sub(r'\\{2}', "%", result)
    result = str(result)
    result = re.sub(r'\\u', "%u", result)

    return result