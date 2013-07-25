from pygawrapper.models import Pygawrapper
from pyga.requests import Tracker, Transaction, Item as gaItem, Visitor, Session, Page
from pygawrapper.string_cookie_jar import StringCookieJar
class PygaMixin(object):
    """
    Add function to retrive ga data.
    """
    def get_utma(self, user_id, *args, **kwargs):
        if not hasattr(self, '_utma'):
            ga = Pygawrapper.objects.get_or_create(user_id=user_id)
            self._utma = StringCookieJar(ga.utma)._cookies
        return self._utma

    def get_utmb(self, user_id, *args, **kwargs):
        if not hasattr(self, '_utmb'):
            ga = Pygawrapper.objects.get_or_create(user_id=user_id)
            self._utmb = StringCookieJar(ga.utmb)._cookies
        return self._utmb

    def get_ga_visitor(self, *args, **kwargs):
        if not hasattr(self, 'ga_visitor'):
            self.ga_visitor = Visitor().extract_from_utma(self.get_utma(kwargs['user_id']))
        return self.ga_visitor

    def get_ga_session(self, *args, **kwargs):
        if not hasattr(self, 'ga_session'):
            self.ga_session = Session().extract_from_utmb(self.get_utmb(kwargs['user_id']))
        return self.ga_session

    def get_ga_tracker(self, GOOGLE_ANALYTICS_CODE, GOOGLE_ANALYTICS_SITE, user_id, *args, **kwargs):
        if not hasattr(self, 'ga_tracker'):
            self.ga_tracker = Tracker(GOOGLE_ANALYTICS_CODE, GOOGLE_ANALYTICS_SITE)
            self.get_ga_session(user_id)
            self.get_ga_visitor(user_id)
        return self.ga_tracker

    def track_transaction(self, transaction):
        self.ga_tracker.track_transaction(transaction=transaction,session=self.ga_session,visitor=self.ga_visitor)

    def track_pageview(self, path):
        page = Page(path)
        self.ga_tracker.track_pageview(page=page,session=self.ga_session,visitor=self.ga_visitor)