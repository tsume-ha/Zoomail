from urllib import request
# from jose import jwt
import jwt
from social_core.backends.oauth import BaseOAuth2


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
    ]

    def authorization_url(self):
        return 'https://' + self.setting('DOMAIN') + '/authorize'

    def access_token_url(self):
        return 'https://' + self.setting('DOMAIN') + '/oauth/token'

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get('id_token')
        jwks = request.urlopen('https://' + self.setting('DOMAIN') + '/.well-known/jwks.json')
        issuer = 'https://' + self.setting('DOMAIN') + '/'
        audience = self.setting('KEY')  # CLIENT_ID
        payload = jwt.decode(id_token, jwks.read(), algorithms=['RS256'], audience=audience, issuer=issuer)
        # payload = jwt.decode(id_token, jwks.read(), algorithms="RS256", audience=audience, issuer=issuer)
        return {'username': payload['nickname'],
                'first_name': payload['name'],
                'picture': payload['picture'],
                'user_id': payload['sub'],
                'email': payload['email']}


# {"issuer":"https://patient-bar-7812.auth0.com/",
# "authorization_endpoint":"https://patient-bar-7812.auth0.com/authorize",
# "token_endpoint":"https://patient-bar-7812.auth0.com/oauth/token",
# "userinfo_endpoint":"https://patient-bar-7812.auth0.com/userinfo",
# "mfa_challenge_endpoint":"https://patient-bar-7812.auth0.com/mfa/challenge",
# "jwks_uri":"https://patient-bar-7812.auth0.com/.well-known/jwks.json",
# "registration_endpoint":"https://patient-bar-7812.auth0.com/oidc/register",
# "revocation_endpoint":"https://patient-bar-7812.auth0.com/oauth/revoke",
# "scopes_supported":[
#     "openid",
#     "profile",
#     "offline_access",
#     "name",
#     "given_name",
#     "family_name",
#     "nickname",
#     "email",
#     "email_verified",
#     "picture",
#     "created_at",
#     "identities",
#     "phone",
#     "address"],
# "response_types_supported":[
#     "code",
#     "token",
#     "id_token",
#     "code token",
#     "code id_token",
#     "token id_token",
#     "code token id_token"],
# "code_challenge_methods_supported":[
#     "S256",
#     "plain"],
# "response_modes_supported":[
#     "query",
#     "fragment",
#     "form_post"],
# "subject_types_supported":["public"],
# "id_token_signing_alg_values_supported":["HS256","RS256"],
# "token_endpoint_auth_methods_supported":["client_secret_basic","client_secret_post"],
# "claims_supported":[
#     "aud",
#     "auth_time",
#     "created_at",
#     "email",
#     "email_verified",
#     "exp",
#     "family_name",
#     "given_name",
#     "iat",
#     "identities",
#     "iss",
#     "name",
#     "nickname",
#     "phone_number",
#     "picture",
#     "sub"],
# "request_uri_parameter_supported":false,
# "device_authorization_endpoint":"https://patient-bar-7812.auth0.com/oauth/device/code"}