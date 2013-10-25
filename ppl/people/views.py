from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound
from ppl.models import Profile, Tag

@view_config(route_name="people.list", renderer="people/list.html")
def list(request):
    people = Profile.query.order_by(Profile.created_ts).all()
    return {'people': people}

@view_config(route_name="people.detail", renderer="people/detail.html")
def detail(request):
    slug = request.matchdict['slug']
    try:
        profile = Profile.query.filter_by(slug=slug).one()
    except NoResultFound:
        raise HTTPNotFound('No person found')
    return {'profile': profile}

@view_config(route_name='people.tag', renderer="people/list.html")
def tag(request):
    tag_name = request.matchdict['tag']
    tag = Tag.query.filter(Tag.name.ilike(tag_name)).first()
    profiles = []
    if tag:
        profiles = tag.profile_parents
    return {'people': profiles}

def edit(request):
    return {}
