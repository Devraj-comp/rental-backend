# services.py
from .models import *
from .serializers import *
from django.conf import settings
from django.core.exceptions import ValidationError
from jwt import decode
from typing import Dict, Any
import requests
import jwt
from django.utils.http import urlencode
from django.shortcuts import redirect
from rest_framework.response import Response


GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

def google_get_access_token(*, request, code: str, redirect_uri: str) -> str:
    code = request.GET.get("code")
    if not code:
        return Response({"error": "Authorization code not provided"}, status=400)

    # Exchange the authorization code for access and ID tokens
    token_endpoint = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,  # Add this to your Django settings
        "redirect_uri": "http://localhost:8000/user/api/v1/auth/google/callback/",
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_endpoint, data=data)
        response.raise_for_status()
        tokens = response.json()

        # Extract ID token and access token
        id_token = tokens.get("id_token")
        access_token = tokens.get("access_token")

        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
        print("the decodes: ",decoded_id_token)
        print("the google login callback function is triggered")

        return access_token
    except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=400)

# get user info from google
def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params = {'access_token': access_token}
    )
    if not response.ok:
        raise ValidationError('Cound not get user info from google.')
    print('the user info: ', response)
    return response.json()

# create JWT token from the profile data
def createJWTToken(validated_data):
    domain = settings.BASE_API_URL
    redirect_uri = 'http://localhost:8000/user/api/v1/auth/google/callback/'

    code = validated_data.get('code')
    error = validated_data.get('error')

    login_url = 'http://localhost:8000/user/login'

    # if error or not code:
    #     params = urlencode({'error': error})
    #     return redirect(f'{login_url}?{params}')
    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

    user_data = google_get_user_info(access_token=access_token)

    # create user in db if first time login
    User.objects.get_or_create(username = user_data.get('name'), email=user_data.get('email')),
    user = user_data.get('given_name')

    profile_data = {
        'email': user_data['email'],
        'username': user_data['given_name'],
        'password': user_data['given_name'],
        'role': 'renter'
    }
    jwt_token = jwt.encode(profile_data, settings.GOOGLE_OAUTH_CLIENT_SECRET, algorithm='HS256')

    print('the generated JWT token: ', jwt_token)
    return user_data, jwt_token


# def createJwtToken(validated_data):
#     domain = settings.BASE_API_URL
#     redirect_uri = f'{domain}/api/v1/auth/login/google/'

#     code = validated_data.get('code')
#     error = validated_data.get('error')
    
#     login_url = f'{settings.BASE_APP_URL}/login'

#     if error or not code:
#         params = urlencode({'error': error})
#         return redirect(f'{login_url}?{params}')

#     access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

#     user_data = google_get_user_info(access_token=access_token)

#     User.objects.get_or_create(username = user_data.get('name'), email = user_data['email'], 
#     first_name = user_data.get('given_name'), last_name = user_data.get('family_name'))
    
#     profile_data = {
#         'email': user_data['email'],
#         'first_name': user_data.get('given_name'),
#         'last_name': user_data.get('family_name'),
#     }

#     jwt_token = jwt.encode(profile_data, settings.SECRET_KEY, algorithm="HS256").decode('utf-8')

#     return user_data, jwt_token

# def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
#     response = requests.get(
#         GOOGLE_USER_INFO_URL,
#         params={'access_token': access_token}
#     )

#     if not response.ok:
#         raise ValidationError('Could not get user info from Google.')
    
#     return response.json()

# def google_get_access_token(*, code: str, redirect_uri: str) -> str:
#     data = {
#         'code': code,
#         'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
#         'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#         'redirect_uri': redirect_uri,
#         'grant_type': 'authorization_code'
#     }

#     response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
#     if not response.ok:
#         raise ValidationError('Could not get access token from Google.')
    
#     access_token = response.json()['access_token']

#     return access_token

# def validateJwtToken(jwt_token):
#     return jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])

# def getUserData(request):
#     jwt_data = validateJwtToken(request.headers.get('Authorization').split(' ')[1])
#     return jwt_data['email']