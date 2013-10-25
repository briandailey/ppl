from hashlib import sha1
from pyramid.view import view_config
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound

from ppl.models import User, Profile, DBSession
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

_SALT = 'as9091oksdfsf0-o0pkl;k1jdf'
@view_config(
    context='velruse.AuthenticationComplete',
    renderer='account/result.html',
)
def login_complete_view(request):
    context = request.context
    session = DBSession()
    #url = "https://api.github.com/user?access_token=%s"
    result = {
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    token = context.credentials['oauthAccessToken']
    provider = context.profile.get('accounts')[0]
    identifier = sha1(str(provider.get('userid')) + _SALT).hexdigest()
    emails = [item['value'] for item in context.profile['emails']]
    email = emails[0]
    logger.warn(result)
    #r = requests.get(url%token)
    #create user
    user = User.query.filter_by(identifier=identifier).first()
    if user:
        #update token
        user.auth_token = token
        user.provider = context.provider_name
    else:
        print context.profile['displayName']
        user = User(
            email=email,
            auth_token=token,
            provider=context.provider_name,
        )
        profile = Profile(
            user=user,
            name=context.profile['displayName'].strip() or context.profile['preferredUsername']
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
    if request.method == "POST" and form.validate():
        form.populate_obj(profile)
        DBSession.add(profile)
    return {'profile': profile, 'form': form}


