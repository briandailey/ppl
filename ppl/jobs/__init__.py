def list(request):
    return {}
def includeme(config):
    config.add_route('jobs.list', '')
    config.add_view(list, route_name='jobs.list', renderer='jobs/list.html')
    config.scan()

