from sqlalchemy import func
from pyramid.view import view_config
from ppl.models import DBSession, Profile, Company, Group


@view_config(context=HTTPNotFound, renderer='404.html')
def not_found(self, request):
    request.response.status_int = 404
    return {}

@view_config(route_name='home', renderer='index.html')
def home(request):
    session = DBSession()
    people = session.query(func.count(Profile.id)).scalar()
    companies = session.query(func.count(Company.id)).scalar()
    groups = session.query(func.count(Group.id)).scalar()
    return {'people': people, 'companies': companies,'groups': groups}


