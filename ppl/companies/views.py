from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ppl.models import DBSession, Company, Tag
from ppl.utils import get_object_or_404
from .forms import CompanyForm

@view_config(route_name='companies.list', renderer="companies/list.html")
def list(request):
    companies = Company.query.order_by('lower(companies.name) asc').all()
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

@view_config(route_name='companies.edit', renderer='companies/edit.html')
def edit(request):
    slug = request.matchdict['slug']
    company = Company.query.filter_by(slug=slug).one()
    form = CompanyForm(request.POST, company)
    if request.method == "POST" and form.validate():
        form.populate_obj(company)
        DBSession.add(company)
        DBSession.flush()
        request.session.flash(u'{} was updated, the version number is now {}'.format(company.name, company.version))
        url = request.route_url('companies.detail', slug=company.slug)
        return HTTPFound(location=url)

    return {'company': company, 'form': form}

@view_config(route_name='companies.new', renderer='companies/edit.html')
def new(request):
    form = CompanyForm(request.POST)
    if request.method == "POST" and form.validate():
        company = Company()
        form.populate_obj(company)
        DBSession.add(company)
        DBSession.flush()
        request.session.flash('{} has been created'.format(company.name))
        url = request.route_url('companies.detail', slug=company.slug)
        return HTTPFound(location=url)
    return {'form': form}

@view_config(route_name='companies.add_member')
def add_member(request):
    slug = request.matchdict['slug']
    company = get_object_or_404(Company, slug=slug)
    company.employees.append(request.user.profile)
    request.session.flash('You have been added to this company.')
    url = request.route_url('companies.detail', slug=company.slug)
    return HTTPFound(location=url)
