"""PytSite Google Authentication Driver Plugin Settings Form
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang, reload
from plugins import widget, settings


class Form(settings.Form):
    def _on_setup_widgets(self):
        """Hook
        """
        self.add_widget(widget.input.Text(
            uid='setting_client_id',
            weight=10,
            label=lang.t('auth_ui_google@client_id'),
            required=True,
            help=lang.t('auth_ui_google@client_id_setup_help'),
        ))

        self.add_widget(widget.input.Text(
            uid='setting_client_secret',
            weight=20,
            label=lang.t('auth_ui_google@client_secret'),
            required=True,
            help=lang.t('auth_ui_google@client_secret_setup_help'),
        ))

        super()._on_setup_widgets()

    def _on_submit(self):
        reload.set_flag()

        return super()._on_submit()
