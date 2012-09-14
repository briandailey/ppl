import collections
from pyramid.view import view_config


Person = collections.namedtuple("Person", ['first', 'last', 'email'])
@view_config(route_name="people.ext", match_param=('ext=json'), renderer="json")
@view_config(route_name="people.list", renderer="people/list.html")
@view_config(route_name="people.list", request_param=('format=json'), renderer="json")
@view_config(route_name="people.list", request_param=("format=partial"), renderer="people/list_partial.html")
def list(request):
    people = []
    for i in range(20):
        people.append(Person(first="John", last="Doe%s" % i, email="jdoe#%s@acme.com" % i))
    return {'people':people}

