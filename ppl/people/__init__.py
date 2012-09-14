def includeme(config):
    config.add_route('people.list', 'list.{ext}')
    config.scan()
