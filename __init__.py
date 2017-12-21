"""PytSite Google Authentication UI Driver
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_less(__name__)
        assetman.t_js(__name__)
        assetman.js_module('auth-google-widget', __name__ + '@js/auth-google-widget')

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load():
    _register_assetman_resources()


def plugin_load_uwsgi():
    from pytsite import lang, router
    from plugins import permissions, settings, auth_ui, auth_google
    from . import _driver, _eh, _settings_form, _controllers

    # Language resources
    lang.register_package(__name__)
    lang.register_global('auth_ui_google_admin_settings_url', lambda language, args: settings.form_url('auth_google'))

    # Permissions
    permissions.define_permission('auth_ui_google@manage_settings', 'auth_ui_google@manage_auth_google_settings', 'app')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)

    # Settings
    settings.define('auth_google', _settings_form.Form, 'auth_ui_google@auth_google', 'fa fa-google',
                    'auth_ui_google@manage_settings')

    try:
        auth_ui.register_driver(_driver.UI(auth_google.get_client_id()))
        router.handle(_controllers.Authorization, '/auth_google/authorization', 'auth_ui_google@authorization',
                      filters=auth_ui.AuthFilterController)

    except auth_google.error.ClientIdNotDefined:
        pass
