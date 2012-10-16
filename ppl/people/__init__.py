def includeme(config):
    config.add_route('people.list', '')
    config.add_route('people.detail', '{slug}')
    config.scan()

