def includeme(config):
    config.add_route('people.list', '')
    config.add_route('people.detail', '{slug}')
    config.add_route('people.edit', '/edit')
    config.add_route('people.tag', 'tag/{tag}')

