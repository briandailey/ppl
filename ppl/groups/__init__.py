from ppl.models import Group
def list_groups(request):
    groups = Group.query.all()
    return {'groups': groups}

def detail(request):
    slug = request.matchdict['slug']
    group = Group.query.filter_by(slug=slug).one()
    return {'group': group}

def includeme(config):
    config.add_route('groups.list', '')
    config.add_route('groups.detail', '{slug}')
    config.add_view(list_groups, route_name='groups.list', renderer='groups/list.html')
    config.add_view(detail, route_name='groups.detail', renderer='groups/detail.html')
    config.scan()
