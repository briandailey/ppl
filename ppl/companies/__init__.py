def includeme(config):
    config.add_route('companies.list', '')
    config.add_route('companies.detail', '{slug}')
    config.scan()
