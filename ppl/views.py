from sqlalchemy import func
from pyramid.view import view_config
from ppl.models import Session, Profile, Company
@view_config(route_name='home', renderer='index.html')
def home(request):
    session = Session()
    people = session.query(func.count(Profile.id)).scalar()
    companies = session.query(func.count(Company.id)).scalar()
    return {'people': people, 'companies': companies}


