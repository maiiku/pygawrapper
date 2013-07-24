# -*- coding: utf-8 -*-

import logging
from pygawrapper import signals
from pygawrapper.string_cookie_jar import StringCookieJar
from pygawrapper.models import Pygawrapper

class PygaWrapperMiddleware(object):

    def process_request(self, request):
        user_data ={}
        signals.pyga_user_query.send(sender=None, request=request, user_data=user_data)
        if not 'id' in user_data:
            raise NotImplemented ('you must implement pyga_user_query in your app')
        else:
            u = user_data['id']

        #if we have a user, continue
        if u:
            #retrive ga data from db
            ga = Pygawrapper.objects.get_or_create(user_id=u)
            #set session data for GA
            utmb = StringCookieJar(u.utmb)
            _utmb = StringCookieJar(request.COOKIES.get('__utmb'))
            if utmb != _utmb:
                u.profile.utmb = _utmb.dump()
                u.save()
            #save user cookie in DB
            utma = StringCookieJar(u.utma)
            _utma = StringCookieJar(request.COOKIES.get('__utma'))
            if utma != _utma:
                u.profile.utma = _utma.dump()
                u.save()

        return None

    def process_response(self, request, response):

        return response
