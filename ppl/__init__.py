import logging
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from .models import DBSession

log = logging.getLogger(__name__)
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings)
    config.include('pyramid_beaker')
    config.include('pyramid_jinja2')

    config.set_session_factory(session_factory)

    config.add_renderer('.html', factory='pyramid_jinja2.renderer_factory')
    config.add_jinja2_search_path("ppl:templates")

    providers = settings.get('login_providers', '')
    providers = filter(None, [p.strip()
                              for line in providers.splitlines()
                              for p in line.split(', ')])
    settings['login_providers'] = providers
    if not any(providers):
        log.warn('no login providers configured, double check your ini '
                 'file and add a few')

    for provider in providers:
        config.include('velruse.providers.%s' % provider)
        config.add_github_login_from_settings(prefix='%s.' % provider)

    config.include('ppl.people', route_prefix="/people")
    config.include('ppl.companies', route_prefix="/companies")
    config.include('ppl.account', route_prefix="/account")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

