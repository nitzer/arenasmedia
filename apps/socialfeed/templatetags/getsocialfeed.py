from django.conf import settings
from django import template
from django.core.cache import cache
import urllib
import re
import datetime
from pytz import timezone, utc

try:
    import json as simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        from django.utils import simplejson

register = template.Library()

try:
    TW_ID = settings.SOCIALFEED_TWITTER_ID
except:
    TW_ID = 'twitterapi'
try:
    TW_COUNT = settings.SOCIALFEED_TWITTER_COUNT
except:
    TW_COUNT = 10

local_time = timezone(settings.TIME_ZONE)

@register.tag(name='twitter_feed')
def do_get_twitter_feed(parser, token):
    """ get latest feed from twitter """
    twitter_id = TW_ID
    count = TW_COUNT
    return TwitterFeed(twitter_id, count)

class TwitterFeed(template.Node):
    def __init__(self, twitter_id, count):
        self.twitter_id = twitter_id
        self.count = count

    def render(self, context):
        parsedate = lambda x: (utc.localize(datetime.datetime.strptime(u''.join(re.split('[\+|\-]+\d{4}\s', x)), '%a %b %d %H:%M:%S %Y'))).astimezone(local_time)
        url = "http://twitter.com/statuses/user_timeline/%s.json?count=%s" % (self.twitter_id, self.count)

        ret = cache.get('twitterfeed')
        if ret is None:
            twobjs = urllib.urlopen(url)
            twjson = simplejson.loads(twobjs.read())
            ret = [{'user': i['user']['name'], 'screen_name': i['user']['screen_name'], 'text': i['text'], 'created_at': parsedate(i['created_at'])} for i in twjson]
            cache.set('twitterfeed', ret, 60)

        context['twitterfeed'] = ret
        return ''


try:
    FB_ID = settings.SOCIALFEED_FACEBOOK_ID
except:
    FB_ID = 'facebook'
try:
    FB_COUNT = settings.SOCIALFEED_FACEBOOK_COUNT
except:
    FB_COUNT = 10
@register.tag(name="facebook_feed")
def do_get_facebook_feed(parser, token):
    """ get latest feed from facebook """
    facebook_id = FB_ID
    count = FB_COUNT
    return FacebookFeed(facebook_id, count)

class FacebookFeed(template.Node):
    def __init__(self, facebook_id, count):
        self.facebook_id = facebook_id
        self.count = count
    
    def get_picture(self, uid=None):
        if not uid:
            uid = self.facebook_id
        pic = cache.get('pic_%s' % uid)
        if pic is None:
            objpic = urllib.urlopen('https://graph.facebook.com/%s/picture' % uid)
            pic = objpic.url
            cache.set('pic_%s' % uid, pic, 3600)
        return pic


    def render(self, context):
        validate = lambda x, y, z: x[y] if x.has_key(y) else ' '.join((x[z],x['link'])) if x.has_key(z) else ''
        parsedate = lambda x: (utc.localize(datetime.datetime.strptime(u''.join(re.split('[\+|\-]+\d{4}', x)), '%Y-%m-%dT%H:%M:%S'))).astimezone(local_time)
        url = 'https://graph.facebook.com/%s/feed?count=%s' % (self.facebook_id, self.count)
        
        ret = cache.get('facebookfeed')
        if ret is None:

            fbobjs = urllib.urlopen(url)
            fbjson = simplejson.loads(fbobjs.read())
            """
            for c,i in enumerate(fbjson['data']):
                print "%s %s: %s\n%s\n\n" % (c, i['from']['name'], i['type'], i['created_time'])
            """
            ret = [{'picture': self.get_picture(i['from']['id']), 'uid':i['from']['id'], 'user': i['from']['name'], 'message': validate(i, 'message', 'name'), 'created_time': parsedate(i['created_time'])} for i in fbjson['data'][:self.count]]
            cache.set('facebookfeed', ret, 60)

        context['facebookfeed'] = ret
        return ''



YT_TYPE = getattr(settings, 'SOCIALFEED_YOUTUBE_TYPE', 'uploads')

try:
    YT_ID = settings.SOCIALFEED_YOUTUBE_ID
except:
    YT_ID = 'cnn'
try:
    YT_COUNT = settings.SOCIALFEED_YOUTUBE_COUNT
except:
    YT_COUNT = 1
@register.tag(name="youtube_feed")
def do_get_youtube_feed(parser, token):
    """ get latest feed from youtube """
    youtube_id = YT_ID
    count = YT_COUNT
    yttype = YT_TYPE
    return YoutubeFeed(youtube_id, count, yttype)

class YoutubeFeed(template.Node):
    def __init__(self, youtube_id, count, yttype):
        self.youtube_id = youtube_id
        self.count = count
        self.yttype = yttype
        self.apiname = 'apisite'
    
    def render(self, context):
        validate = lambda x, y, z: x[y] if x.has_key(y) else ' '.join((x[z],x['link'])) if x.has_key(z) else ''
        linkvideo = lambda x: re.findall('video\:([a-zA-Z0-9]+)', x).pop(0)
        parsedate = lambda x: datetime.datetime.strptime(u''.join(re.split('[\+|\-|\.]+\d{3,4}[zZ]+', x)), '%Y-%m-%dT%H:%M:%S')
        url = 'http://gdata.youtube.com/feeds/api/users/%s/%s?v=2&alt=jsonc&orderby=published&max-results=%s' % \
                (self.youtube_id, self.yttype, self.count)
        #url = 'http://gdata.youtube.com/feeds/base/users/%s/uploads?alt=json&v=2&orderby=published&client=%s&max-results=%s' % \
        #        (self.youtube_id, self.apiname, self.count)

        ret = cache.get('youtubefeed')
        if ret is None:

            ytobjs = urllib.urlopen(url)
            ytjson = simplejson.loads(ytobjs.read())
            """
            for c,i in enumerate(ytjson['feed']['entry']):
                print "%s %s: %s\n%s\n\n" % (c, i['updated']['$t'], i['title']['$t'], i['content']['$t'])
            """
            if self.yttype == 'favorites':
                ret = [{'title': i['video']['title'], 'id': i['video']['id'], 'description': i['video']['description']} for i in ytjson['data']['items']]
            else:
                ret = [{'title': i['title'], 'id': i['id'], 'description': i['description']} for i in ytjson['data']['items']]

            cache.set('youtubefeed', ret, 60)

        context['youtubefeed'] = ret
        return ''



