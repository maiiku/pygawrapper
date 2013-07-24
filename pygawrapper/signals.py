from django.dispatch import Signal

pyga_user_query = Signal(providing_args=['request', 'user_data'])
pyga_user_query.__doc__ = """
Sent to ask for filling user additional data:
    user_data['id']:		user id
Signal passes request from within middleware, asking receiver to proved user
id based on that request.

returned user_data MUST contain id key. If there's no user, set id to None

This data cannot be filled by ``pygawrapper`` because it is host's structure
agnostic. After filling values just do return.
"""

'''
#--------------------------------------------#
# example implementation                     #
#--------------------------------------------#
def pyga_user_query_listener(sender, request, user_data, **kwargs):
    from django.contrib.auth.models import User
    login = request.user.username
    user = get_object_or_404(User, username__iexact=self.login)
    user_data.update({'id':user.pk})

signals.pyga_user_query.connect(pyga_user_query_listener)
'''