from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse((
        'https',
        'api.vk.com',
        '/method/users.get',
        None,
        urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'domain')),
                              access_token=response['access_token'],
                              v='5.92')),
        None,
    ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

    if data['about']:
        user.userprofile.about_me = data['about']

    if data['domain']:
        user.userprofile.page_in_vkontakte = f"https://vk.com/{data['domain']}"

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age > 200:
            raise AuthForbidden('social_core.backends.vk.VKOAuth2. !!! Человеку больше 200 лет !!!')

    user.save()
