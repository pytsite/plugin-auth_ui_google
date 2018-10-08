"""PytSite Google Authentication UI Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load_wsgi():
    from pytsite import lang, router
    from plugins import settings, auth_ui, auth_google
    from . import _driver, _eh, _settings_form, _controllers

    # Language globals
    lang.register_global('auth_ui_google_admin_settings_url', lambda language, args: settings.form_url('auth_google'))

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)

    # Settings
    settings.define('auth_google', _settings_form.Form, 'auth_ui_google@auth_google', 'fa fa-google', 'dev')

    try:
        auth_ui.register_driver(_driver.UI(auth_google.get_client_id()))
        router.handle(_controllers.Authorization, '/auth_google/authorization', 'auth_ui_google@authorization',
                      filters=auth_ui.AuthFilter)

    except auth_google.error.ClientIdNotDefined:
        pass
