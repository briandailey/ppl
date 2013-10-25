def route_path_filter(route_name, *elements, **kw):
    request = get_current_request()
    return request.route_path(route_name, *elements, **kw)
