"""PytSite Google Authentication Driver Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import html as _html, metatag as _metatag
from plugins import widget as _widget, form as _form, auth_ui as _auth_ui


class _SignInWidget(_widget.Abstract):
    """Google Sign In Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-google-sign-in'
        self._data['client_id'] = kwargs.get('client_id', '')
        self._js_module = 'auth-google-widget'

    def _get_element(self, **kwargs) -> _html.Element:
        return _html.Div(uid=self.uid, css='button-container')


class _SignInForm(_form.Form):
    """Google Sign In Form
    """

    def __init__(self, **kwargs):
        """Init.
        """
        self._client_id = kwargs.get('client_id')
        super().__init__(**kwargs)
        self._nocache = True

    def _on_setup_widgets(self):
        self.add_widget(_widget.input.Hidden(self.uid + '-id-token', form_area='hidden'))
        self.add_widget(_SignInWidget(self.uid + '-google-button', client_id=self._client_id))

        # Submit button is not necessary, form submit performs by JS code
        self.remove_widget('action-submit')


class UI(_auth_ui.Driver):
    """Auth UI Driver
    """

    def __init__(self, client_id: str):
        """Init
        """
        self._client_id = client_id

        if not self._client_id:
            raise RuntimeError("You should set configuration parameter 'auth.google.client_id'. " +
                               "See details at https://developers.google.com/identity/sign-in/web/devconsole-project")

    def get_name(self) -> str:
        """Get name of the driver
        """
        return 'google'

    def get_description(self) -> str:
        """Get description of the driver
        """
        return 'Google'

    def get_sign_up_form(self, **kwargs) -> _form.Form:
        """Get sign in form
        """
        return self.get_sign_in_form(**kwargs)

    def get_sign_in_form(self, **kwargs) -> _form.Form:
        """Get sign in form
        """
        _metatag.t_set('google-signin-client_id', self._client_id)

        return _SignInForm(client_id=self._client_id, **kwargs)
