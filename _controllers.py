"""PytSite Google Authentication Driver Plugin Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from oauth2client.client import OAuth2WebServerFlow
from pytsite import routing, router, lang
from plugins import auth, auth_google


class Authorization(routing.Controller):
    def exec(self):
        # Check for error from Google
        error = self.arg('error')
        if error == 'access_denied':
            raise self.forbidden(lang.t('auth_ui_google@user_declined_authorization'))

        # Check for code from Google
        code = self.arg('code')
        if code:
            # Restore flow from session
            flow = router.session().get('google_oauth2_flow')  # type: OAuth2WebServerFlow
            if not flow:
                raise self.forbidden('Cannot retrieve stored OAuth2 flow')

            # Exchange code to credentials
            credentials = flow.step2_exchange(code)
            user = auth.get_current_user()
            user.set_option('google_oauth2_credentials', credentials.to_json())
            user.save()

            final_redirect = router.session().get('google_oauth2_final_redirect', router.base_url())

            router.session().pop('google_oauth2_flow')
            router.session().pop('google_oauth2_final_redirect')

            return self.redirect(final_redirect)

        else:
            # Request new code from Google
            scope = self.args.pop('scope')  # type: str
            if scope and ',' in scope:
                scope = scope.split(',')
            flow = auth_google.create_oauth2_flow(scope, router.current_url(True, query=dict(self.args)))
            router.session()['google_oauth2_flow'] = flow
            router.session()['google_oauth2_final_redirect'] = self.args.pop('__redirect', router.base_url())

            return self.redirect(flow.step1_get_authorize_url())
