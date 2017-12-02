"""PytSite Google Authentication Driver Plugin Events Handlers
"""
from pytsite import metatag as _metatag, router as _router, lang as _lang
from plugins import auth as _auth, auth_google

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    client_id = auth_google.get_client_id()

    if client_id:
        _metatag.t_set('google-signin-client_id', client_id)
        _metatag.t_set('pytsite-auth-google-client-id', client_id)

    else:
        client_secret = auth_google.get_client_secret()
        if not (client_id and client_secret) and \
                _auth.get_current_user().has_permission('auth_ui_google@manage_settings'):
            _router.session().add_warning_message(_lang.t('auth_ui_google@plugin_setup_required_warning'))
