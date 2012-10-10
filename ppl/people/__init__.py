def includeme(config):
    config.add_route('people.ext', 'list.{ext}')
    config.add_route('people.list', '')
    config.scan()

