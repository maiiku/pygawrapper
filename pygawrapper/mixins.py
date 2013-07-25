from pygawrapper.models import Pygawrapper
from pyga.requests import Tracker, Transaction, Item as gaItem, Visitor, Session, Page
from pygawrapper.string_cookie_jar import StringCookieJar
class PygaMixin(object):
    """
    Add function to retrive ga data.
    """
    def get_utma(self, user_id, request, *args, **kwargs):
        ga = Pygawrapper.objects.get_or_create(user_id=user_id)
        return StringCookieJar(ga.utma)._cookies

    def get_utmb(self, user_id, request, *args, **kwargs):
        ga = Pygawrapper.objects.get_or_create(user_id=user_id)
        return StringCookieJar(ga.utmb)._cookies

    def get_ga_visitor(self, *args, **kwargs):
        self.ga_visitor = Visitor().extract_from_utma(self.get_utma())
        return self.ga_visitor

    def get_ga_session(self, *args, **kwargs):
        self.ga_session = Session().extract_from_utma(self.get_utmb())
        return self.ga_session

    def get_ga_tracker(self, GOOGLE_ANALYTICS_CODE, GOOGLE_ANALYTICS_SITE, *args, **kwargs):
        self.ga_tracker = Tracker(GOOGLE_ANALYTICS_CODE, GOOGLE_ANALYTICS_SITE)
        self.ga_session()
        self.get_ga_visitor()
        return self.ga_tracker

    def track_transaction(self, transaction):
        self.ga_tracker.track_transaction(transaction=transaction,session=self.ga_session,visitor=self.ga_visitor)

    def track_pageview(self, path):
        page = Page(path)
        self.ga_tracker.track_pageview(page=page,session=self.ga_session,visitor=self.ga_visitor)