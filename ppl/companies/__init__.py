def includeme(config):
    config.add_route('companies.list', '')
    config.add_route('companies.new', 'new')
    config.add_route('companies.detail', '{slug}')
    config.add_route('companies.tag', 'tag/{tag}')
    config.add_route('companies.edit', 'edit/{slug}')
    config.add_route('companies.add_member', 'add_member/{slug}')

