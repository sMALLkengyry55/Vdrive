from google.oauth2.credentials import Credentials
from django.conf import settings


def get_google_credentials(user):
    social = user.social_auth.filter(provider='google-oauth2').first()
    credentials = Credentials(social.extra_data['access_token'], social.extra_data['refresh_token'],
                              token_uri=settings.TOKEN_URI, client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                              client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)
    return credentials
