from pygawrapper.models import Pygawrapper
from pyga.requests import Tracker, Transaction, Item as gaItem, Visitor, Session, Page, Event
from pygawrapper.string_cookie_jar import StringCookieJar
from django.conf import settings
GA_CODE = getattr(settings,'GOOGLE_ANALYTICS_CODE', None)
GA_SITE = getattr(settings,'GOOGLE_ANALYTICS_SITE', None)
from django.core.exceptions import ObjectDoesNotExist

class PygaMixin(object):
    """
    Add function to retrive ga data.
    """
    def get_utma(self, *args, **kwargs):
        """
        Gets stored __utma cookie
        """
        user_id = kwargs.get('user_id')
        if not hasattr(self, '_utma') or ('force' in kwargs and 'user_id' in kwargs):
            try:
                ga = Pygawrapper.objects.get(user_id=user_id)
                _utma = ga.utma
            except Pygawrapper.DoesNotExist:
                _utma = None
            if not _utma:
                raise ObjectDoesNotExist('__utma for user %s does not exist in database. PygaMiddleware must set it first!')
            self._utma = StringCookieJar(_utma)._cookies
        elif not hasattr(self, '_utma') and ('force' in kwargs and 'user_id' not in kwargs) :
            raise ObjectDoesNotExist('You are trying to re-initialize pygwarapper but have not set utm values or forgot to pass user_id!')
        return self._utma

    def get_utmb(self, *args, **kwargs):
        """
        Gets stored __utmb cookie
        """
        user_id = kwargs.get('user_id')
        if not hasattr(self, '_utmb') or ('force' in kwargs and 'user_id' in kwargs):
            try:
                ga = Pygawrapper.objects.get(user_id=user_id)
                _utmb = ga.utmb
            except Pygawrapper.DoesNotExist:
                _utmb = None
            if not _utmb:
                raise ObjectDoesNotExist('__utmb for user %s does not exist in database. PygaMiddleware must set it first!')
            self._utmb = StringCookieJar(_utmb)._cookies
        elif not hasattr(self, '_utmb') and ('force' in kwargs and 'user_id' not in kwargs) :
            raise ObjectDoesNotExist('You are trying to re-initialize pygwarapper but have not set utm values or forgot to pass user_id!')
        return self._utmb

    def set_utma(self, utma):
        self._utma = utma

    def set_utmb(self, utmb):
        self._utmb = utmb

    def set_utm(self, utma, utmb):
        self.set_utma(utma)
        self.set_utmb(utmb)
        self.get_ga_tracker(force=True)

    def get_ga_visitor(self, *args, **kwargs):
        """
        Gets a visitor and optionally feeds it with __utma data if user_id is provided
        """
        if not hasattr(self, 'ga_visitor') or 'force' in kwargs:
            if 'user_id' in kwargs or 'force' in kwargs:
                self.get_utma(**kwargs)
            try:
                self._utma.split('.')
            except:
                self.ga_visitor = Visitor()
            else:
                self.ga_visitor = Visitor().extract_from_utma(self._utma)

        return self.ga_visitor

    def get_ga_session(self, *args, **kwargs):
        """
        Gets a session and optionally feeds it with __utmb data if user_id is provided
        """
        if not hasattr(self, 'ga_session') or 'force' in kwargs:
            if 'user_id' in kwargs or 'force' in kwargs:
                self.get_utmb(**kwargs)
            try:
                self._utmb.split('.')
            except:
                self.ga_session = Session()
            else:
                self.ga_session = Session().extract_from_utmb(self.get_utmb)
        return self.ga_session

    def get_ga_tracker(self, GOOGLE_ANALYTICS_CODE=GA_CODE, GOOGLE_ANALYTICS_SITE=GA_SITE, *args, **kwargs):
        """
        Creates a tracker and fills it with session and visitor, optionally matched with given user if user_id is provided
        Returns self for convenient use of other wrapped functions
        Pass force=True in to re-initiate the tracker
        """
        if not hasattr(self, 'ga_tracker') or 'force' in kwargs:
            self.ga_tracker = Tracker(GOOGLE_ANALYTICS_CODE, GOOGLE_ANALYTICS_SITE)
            self.get_ga_session(**kwargs)
            self.get_ga_visitor(**kwargs)
        return self

    def track_pageview(self, path, **kwargs):
        """
        @variable str page
        @variable dict kwargs (optional) {'title', 'charset', 'referrer', 'load_time'}
        Sends page hit to GA with given path as the page
        """
        page = Page(path)
        page.title = kwargs.get('title', None)
        page.charset = kwargs.get('charset', None)
        page.referrer = kwargs.get('referrer', None)
        page.load_time = kwargs.get('load_time', None)
        self.ga_tracker.track_pageview(page=page,session=self.ga_session,visitor=self.ga_visitor)

    def track_transaction(self, transaction, items):
        """
        @variable dict transaction {'order_id', 'order_id', 'tax', u'affiliation', 'shipping', u'city', u'state',
                                    u'country'}
        @variable list of dicts items  [{'sku', u'name', 'variation', 'price', 'quantity' }, {...}]
        Sends transaction to GA e-commerce
        """
        trans = Transaction()
        trans.order_id = transaction.get('order_id', None)
        trans.total = transaction.get('total', None)
        trans.tax = transaction.get('tax', None)
        trans.affiliation = transaction.get('affiliation', None)
        trans.shipping = transaction.get('shipping', None)
        trans.city = transaction.get('city', None)
        trans.state = transaction.get('state', None)
        trans.country = transaction.get('country', None)

        for item in items:
            gitem = gaItem()
            gitem.sku = item.get('sku', None)
            gitem.name = item.get('name', None)
            gitem.variation = item.get('variation', None)
            gitem.price = item.get('price', None)
            gitem.quantity = item.get('quantity', 1)
            trans.add_item(gitem)

        self.ga_tracker.track_transaction(transaction=trans,session=self.ga_session,visitor=self.ga_visitor)

    def track_event(self,  category=None, action=None, label=None, value=None, noninteraction=False):
        """
        @variable str category
        @variable str action
        @variable str label
        @variable str value
        @variable  bool noninteraction
        Sends event to GA
        """
        e = Event(category=category, action=action, label=label, value=value)

        self.ga_tracker.track_event(event=e,session=self.ga_session,visitor=self.ga_visitor)