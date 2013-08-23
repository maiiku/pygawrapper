# -*- coding: utf-8 -*-

import logging
from pygawrapper import signals
from pygawrapper.string_cookie_jar import StringCookieJar
from pygawrapper.models import Pygawrapper
from django.conf import settings
ADD_TRACKER = getattr(settings,'PYGA_SET_REQUEST_TRACKER', False)

class PygaWrapperMiddleware(object):

    def process_request(self, request):
        user_data ={}
        signals.pyga_user_query.send(sender=None, request=request, user_data=user_data)
        if not 'id' in user_data:
            raise NotImplementedError ('you must implement pyga_user_query in your app')
        else:
            u = user_data['id']

        #if we have a user, continue
        if u:
            #retrive ga data from db
            ga, created = Pygawrapper.objects.get_or_create(user_id=u)
            #set session data for GA
            utmb = StringCookieJar(ga.utmb)
            _utmb = StringCookieJar(request.COOKIES.get('__utmb'))
            if utmb != _utmb:
                ga.utmb = _utmb.dump()
                ga.save()
            #save user cookie in DB
            utma = StringCookieJar(ga.utma)
            _utma = StringCookieJar(request.COOKIES.get('__utma'))
            if utma != _utma:
                ga.utma = _utma.dump()
                ga.save()
            #init
            PygaMixin().get_ga_tracker(user_id=u)
            if ADD_TRACKER:
                from pygawrapper.mixins import PygaMixin
                request.tracker = PygaMixin().get_ga_tracker(user_id=u)
        else:
            #add anonymous tracker
            if ADD_TRACKER:
                from pygawrapper.mixins import PygaMixin
                request.tracker = PygaMixin().get_ga_tracker()
                request.tracker.set_utm(request.COOKIES.get('__utma'), request.COOKIES.get('__utmb'))

        return None

    def process_response(self, request, response):

        return response
