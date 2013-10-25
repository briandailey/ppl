from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound
from ppl.models import Group, Tag, DBSession
from ppl.utils import get_object_or_404

from .forms import GroupForm
def list_groups(request):
    groups = Group.query.all()
    return {'groups': groups}

def detail(request):
    slug = request.matchdict['slug']
    try:
        group = Group.query.filter_by(slug=slug).one()
    except NoResultFound:
        raise HTTPNotFound('Group not found')
    return {'group': group}

def tag(request):
    tag_name = request.matchdict['tag']
    tag = Tag.query.filter(Tag.name.ilike(tag_name)).first()
    groups = []
    if tag:
        groups = tag.group_parents
    return {'groups': groups}

def edit(request):
    slug = request.matchdict['slug']
    group = Group.query.filter_by(slug=slug).one()
    form = GroupForm(request.POST, group)
    if request.method == "POST" and form.validate():
        form.populate_obj(group)
        DBSession.add(group)
        DBSession.flush()
        request.session.flash(u'{} was updated, the version number is now {}'.format(group.name, group.version))
        url = request.route_url('groups.detail', slug=group.slug)
        return HTTPFound(location=url)

    return {'group': group, 'form': form}

def new(request):
    form = GroupForm(request.POST)
    if request.method == "POST" and form.validate():
        group = Group()
        form.populate_obj(group)
        DBSession.add(group)
        DBSession.flush()
        request.session.flash('{} has been created'.format(group.name))
        url = request.route_url('groups.detail', slug=group.slug)
        return HTTPFound(location=url)
    return {'form': form}


def add_member(request):
    slug = request.matchdict['slug']
    group = get_object_or_404(Group, slug=slug)
    group.members.append(request.user.profile)
    request.session.flash('You have been added to this group.')
    url = request.route_url('groups.detail', slug=group.slug)
    return HTTPFound(location=url)

def includeme(config):
    config.add_route('groups.list', '')
    config.add_route('groups.new', 'new')
    config.add_route('groups.detail', '{slug}')
    config.add_route('groups.edit', 'edit/{slug}')
    config.add_route('groups.tag', 'tag/{tag}')
    config.add_route('groups.add_member', 'add_member/{slug}')
    config.add_view(list_groups, route_name='groups.list', renderer='groups/list.html')
    config.add_view(detail, route_name='groups.detail', renderer='groups/detail.html')
    config.add_view(tag, route_name='groups.tag', renderer='groups/list.html')
    config.add_view(edit, route_name='groups.edit', renderer='groups/edit.html')
    config.add_view(new, route_name='groups.new', renderer='groups/edit.html')
    config.add_view(add_member, route_name='groups.add_member')
