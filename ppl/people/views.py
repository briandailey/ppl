import collections
from pyramid.view import view_config


Person = collections.namedtuple("Person", ['first', 'last', 'email'])
@view_config(route_name="people.list", match_param=('ext=json'), renderer="json")
@view_config(route_name="people.list", renderer="templates/people.html")
@view_config(route_name="people.list", request_param=("partial=true"), renderer="templates/people_partial.html")
def list(request):
    people = []
    for i in range(20):
        people.append(Person(first="John", last="Doe%s" % i, email="jdoe#%s@acme.com" % i))
    return {'people':people}

