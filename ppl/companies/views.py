from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ppl.models import DBSession, Company, Tag

@view_config(route_name='companies.list', renderer="companies/list.html")
def list(request):
    companies = Company.query.all()
    return {'companies': companies}

@view_config(route_name='companies.detail', renderer="companies/detail.html")
def detail(request):
    slug = request.matchdict['slug']
    try:
        item = Company.query.filter_by(slug=slug).one()
    except NoResultFound:
        raise HTTPNotFound('Company not found')
    return {'item': item}

@view_config(route_name='companies.tag', renderer="companies/list.html")
def tag(request):
    tag_name = request.matchdict['tag']
    tag = Tag.query.filter(Tag.name.ilike(tag_name)).first()
    companies = []
    if tag:
        companies = tag.company_parents
    return {'companies': companies}
