"""PytSite Google Authentication Driver Plugin Events Handlers
"""
from pytsite import metatag as _metatag, router as _router, lang as _lang, reg as _reg
from plugins import auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    if _reg.get('auth_google.client_id'):
        _metatag.t_set('google-signin-client_id', _reg.get('auth_google.client_id'))

    c_user = _auth.get_current_user()
    if not (_reg.get('auth_google.client_id') and _reg.get('auth_google.client_secret')) \
            and c_user.has_permission('auth_google@manage_reg'):
        _router.session().add_warning_message(_lang.t('auth_google@plugin_setup_required_warning'))

    if _reg.get('auth_google.client_id'):
        _metatag.t_set('pytsite-auth-google-client-id', _reg.get('auth_google.client_id'))
