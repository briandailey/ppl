from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ppl.models import DBSession, Company

@view_config(route_name='companies.list', renderer="companies/list.html")
def list(request):
    companies = Company.query.all()
    return {'companies': companies}

@view_config(route_name='companies.detail', renderer="companies/detail.html")
def detail(request):
    slug = request.matchdict['slug']
    item = Company.query.filter_by(slug=slug).one()
    return {'item': item}
