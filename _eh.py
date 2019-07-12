"""PytSite Google Authentication Driver Plugin Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import metatag, router, lang
from plugins import auth, auth_google


def router_dispatch():
    """pytsite.router.dispatch
    """
    try:
        client_id = auth_google.get_client_id()
        metatag.t_set('google-signin-client_id', client_id)
        metatag.t_set('pytsite-auth-google-client-id', client_id)

    except auth_google.error.ClientIdNotDefined:
        if auth.get_current_user().has_role('dev'):
            router.session().add_warning_message(lang.t('auth_ui_google@plugin_setup_required_warning'))
