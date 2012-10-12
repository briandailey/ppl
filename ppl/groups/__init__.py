def list(request):
    return {}
def includeme(config):
    config.add_route('groups.list', '')
    config.add_view(list, route_name='groups.list', renderer='groups/list.html')
    config.scan()
