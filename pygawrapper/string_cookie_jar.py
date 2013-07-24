import cookielib, pickle

class StringCookieJar(cookielib.CookieJar):
    def __init__(self, cookie_string="", policy=None):
        cookielib.CookieJar.__init__(self, policy)
        if cookie_string:
            try:
                self._cookies = pickle.loads(str(cookie_string))
            except IndexError:
                 self._cookies = cookie_string
            except KeyError:
                 self._cookies = cookie_string
    def dump(self):
            return pickle.dumps(self._cookies)