import json
import requests
from pyramid.view import view_config

from ppl.models import User, Profile, Session

from velruse import login_url
@view_config(
    route_name='login',
    renderer='account/login.html',
)
def login_view(request):
    return {
        'login_url': login_url,
        'providers': request.registry.settings['login_providers'],
    }

@view_config(
    context='velruse.providers.github.GithubAuthenticationComplete',
    renderer='account/result.html',
)
def gh_login_complete_view(request):
    context = request.context
    url = "https://api.github.com/user?access_token=%s"
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    token = context.credentials['oauthAccessToken']
    email = context.profile['emails'][0]['value']
    #r = requests.get(url%token)
    #create user
    user = User.query.filter_by(email=email).first()
    if user:
        #update token
        if user.access_token != token:
            user.access_token = token
            user.provider = 'github'
    else:
        user = User(
            email=email,
            access_token=token,
            provider="github"
        )
    Session.add(user)
    Session.commit()
    #login user
    headers = remember(request, login)
    request.session.flash(u'Logged in successfully.')
    return HTTPFound(location=request.route_url('home'))

