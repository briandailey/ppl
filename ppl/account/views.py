import json
from pyramid.view import view_config

from ppl.models import User 

from velruse import login_url
@view_config(
    route_name='login',
    renderer='account/login.html',
)
def login_view(request):
    #/login/github/callback
    return {
        'login_url': login_url,
        'providers': request.registry.settings['login_providers'],
    }

@view_config(
    context='velruse.AuthenticationComplete',
    renderer='account/result.html',
)
def login_complete_view(request):
    context = request.context
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    #create user

    #create auth?
    return {
        'result': json.dumps(result, indent=4),
        'context': context
    }
