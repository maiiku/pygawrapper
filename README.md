'''
/* pygawrapper README file
 * ====================================================
 * @author Michal Korzeniowski <mko_san@lafiel.net>
 * @version 1.1
 * @date 07-2013
 * ==================================================*/
'''

Description:
------------
A wrapper class for pyga (Python Google Analitycs) providing middleware and mixin for integration with django


Requirements:
-------------
pyga >= 2.2.1
django


Installing:
-----------

run from console:
pip install -e git+https://github.com/maiiku/pygawrapper.git#egg=pygawrapper


Setup:
------
1. add pygawrapper to installed apps in your django settings

    INSTALLED_APPS = (
        ...
        'pygawrapper',
        ...
    )
  
2. add pygawrapper middleware in your django settings anywhere AFTER django auth middlware

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'pygawrapper.middleware.PygaWrapperMiddleware',
        ...
    )

3. implement a reciver for pygawrapper's user request signal

    #example implementation
    
    def pyga_user_query_listener(sender, request, user_data, **kwargs):
        from django.contrib.auth.models import User
        if request.user.is_authenticated():
            pk = request.user.pk
        else:
            pk = None
        user_data.update({'id':pk})


4. add PygaMixin to desired class you wish to extend with pyga's functions

    #example (extending user profile):
    
    from pygawrapper.mixins import PygaMixin
    class Profile(PygaMixin, AccountsLanguageBaseProfile):
    ...

6. runc syncdb to create pygawrapper's table

    in your project root run
    python manage.py syncdb
    
5. See optional setup below


Optional setup:
---------------

You cen set site and code in you django setting, and wrapper mixin will use it

GOOGLE_ANALYTICS_CODE = 'GA-XXXXXX'
GOOGLE_ANALYTICS_SITE = 'example.com'


Example usage:
--------------
(to be written)
