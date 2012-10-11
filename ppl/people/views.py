from pyramid.view import view_config

from ppl.models import Profile

@view_config(route_name="people.list", renderer="people/list.html")
def list(request):
    people = Profile.query.all()
    return {'people': people}

