from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ppl.models import Session, Company

@view_config(route_name='companies.list', renderer="companies/list.html")
def list(request):
    return {}
