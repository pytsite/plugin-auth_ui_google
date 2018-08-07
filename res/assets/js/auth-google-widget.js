/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
define(['jquery', 'assetman', 'auth-http-api', 'pytsite-google'], function ($, assetman, pytsiteAuth, google) {
    return function (widget) {
        let form = $('.auth-ui-sign-in.driver-google');

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
    }
});
