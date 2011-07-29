import urllib
import urllib2
import json

API_URL = "http://disqus.com/api/"
USER_API_KEY = u"h0QWC4jDudjKBL5rYrfGlKz41QgYQpIkhrEL5vnLW10BMgg0k4M8Dt7UnqA9IAkU" # xavierlesa

FORUM_ID = 455195 # linkbblog
FORUM_API_KEY = u"X28B89JpCy4vcnSDLbIeUWJWz1Rc06n1V0Af3bJ4OyVKPGEIpfyEIrchi9kP8sQ0" # linkbblog

def api_get(method, values={}, api_version='1.1', is_post=False):
    
    values.update({'user_api_key': USER_API_KEY})
    values.update({'api_version': api_version})

    data = urllib.urlencode(values)
    if not is_post:
        response = urllib2.urlopen("%s%s?%s" % (API_URL, method, data)).read()
    else:
        response = urllib2.urlopen("%s%s" % (API_URL, method), data).read()
    return json.loads(response)


def get_user_name():
    return api_get('get_user_name', is_post=True)

def get_forum_api_key(forum_id=FORUM_ID):
    return api_get('get_forum_api_key', {'forum_id': forum_id})

def get_forum_list():
    return api_get('get_forum_list')

def get_forum_posts(forum_id=FORUM_ID):
    return api_get('get_forum_posts', {'forum_id': forum_id})

def get_num_posts(thread_ids):
    return api_get('get_num_posts', {'thread_ids': thread_ids})

def get_thread_by_url(url, forum_api_key=FORUM_API_KEY):
    return api_get('get_thread_by_url', {'url': url, 'forum_api_key': forum_api_key})
