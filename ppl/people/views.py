from pyramid.view import view_config

from ppl.models import Profile

@view_config(route_name="people.list", renderer="people/list.html")
def list(request):
    people = Profile.query.all()
    return {'people': people}

@view_config(route_name="people.detail", renderer="people/detail.html")
def detail(request):
    slug = request.matchdict['slug']
    profile = Profile.query.filter_by(slug=slug).one()
    return {'profile': profile}
