import './index.scss';

const $ = require('jquery');
const assetman = require('@pytsite/assetman');
const pytsiteAuth = require('@pytsite/auth-http-api');
const google = require('@pytsite/google');

/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
require('@pytsite/widget').onWidgetLoad('plugins.auth_ui_google._driver._SignInWidget', (widget) => {
    const form = $('.auth-ui-sign-in.driver-google');

    form.on('submit:form:pytsite', function () {
        let q = assetman.parseLocation().query;
        window.location.href = q.hasOwnProperty('__redirect') ? q.__redirect : window.location.origin;
    });

    google.ready(function (gapi) {
        gapi.load('auth2', function () {
            gapi.auth2.init().then(function () {
                pytsiteAuth.me().fail(function (e) {
                    if (e.status === 403) {
                        gapi.auth2.getAuthInstance().signOut();
                        gapi.signin2.render(widget.uid, {
                            onSuccess: function (user) {
                                form.find('input[name="id_token"]').val(user.getAuthResponse().id_token);
                                form.submit();
                            }
                        });
                    }
                });
            });
        });
    });
});
