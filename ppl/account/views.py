from pyramid.view import view_config
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound

from ppl.models import User, Profile, Session
from ppl.account.forms import ProfileForm

from velruse import login_url
import logging
logger = logging.getLogger(__name__)
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
    context='velruse.AuthenticationComplete',
    renderer='account/result.html',
)
def login_complete_view(request):
    context = request.context
    session = Session()
    #url = "https://api.github.com/user?access_token=%s"
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    token = context.credentials['oauthAccessToken']
    email = context.profile['emails'][0]['value']
    logger.debug(result)
    #r = requests.get(url%token)
    #create user
    user = User.query.filter_by(email=email).first()
    if user:
        #update token
        if user.access_token != token:
            user.access_token = token
            user.provider = context.provider_name
    else:
        user = User(
            email=email,
            access_token=token,
            provider=context.provider_name
        )
        profile = Profile(
            user=user,
            name=context.profile['displayName']
        )
        if context.provider_name == 'github':
            profile.github_name = context.profile['preferredUsername']
        session.add(profile)
    #create profile if needed
    session.add(user)
    session.flush()
    #login user
    headers = remember(request, user.id)
    request.session.flash(u'Logged in successfully.')
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)

@view_config(route_name="profile", renderer="account/profile.html")
def profile(request):
    #user_id = authenticated_userid(request)
    #user = User.query.get(user_id)
    profile = request.user.profile
    form = ProfileForm(request.POST, profile)
    return {'profile': profile, 'form': form}


