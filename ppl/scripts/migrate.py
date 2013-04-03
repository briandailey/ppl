import os
import sys

from sqlalchemy import engine_from_config, MetaData, Table, func
from sqlalchemy.sql import select
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    Profile,
    User,
    Company,
    Group,
    initialize_sql,
    DBSession,
    group_membership,
    company_membership,
    Tag
)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def load_tables(metadata):
    Table('authentications', metadata, autoload=True)
    Table('companies', metadata, autoload=True)
    Table('company_projects', metadata, autoload=True)
    Table('employments', metadata, autoload=True)
    Table('friendly_id_slugs', metadata, autoload=True)
    Table('group_memberships', metadata, autoload=True)
    Table('group_projects', metadata, autoload=True)
    Table('groups', metadata, autoload=True)
    Table('people', metadata, autoload=True)
    Table('project_memberships', metadata, autoload=True)
    Table('projects', metadata, autoload=True)
    Table('resource_links', metadata, autoload=True)
    Table('schema_migrations', metadata, autoload=True)
    Table('sponsorships', metadata, autoload=True)
    Table('taggings', metadata, autoload=True)
    Table('tags', metadata, autoload=True)
    Table('users', metadata, autoload=True)
    return metadata

def move_user_info(metadata):
    conn = metadata.bind.connect()
    users = metadata.tables['users']
    auth = metadata.tables['authentications']
    people = metadata.tables['people']
    #result = conn.execute(select([users, auth], users.c.id == auth.c.user_id).apply_labels())
    result = conn.execute(select([users]).apply_labels())
    session = DBSession()
    for row in result:
        #get auth info
        user = User(
            id=row['users_id'],
            email=row['users_email'],
            sign_in_count=row['users_sign_in_count'],
            access_token='',
            #access_token=row['authentications_access_token'],
            #access_token_secret=row['authentications_access_token_secret'],
            #provider=row['authentications_provider'],
            created_ts=row['users_created_at'],
            updated_ts=row['users_updated_at']
        )
        query = people.select()
        user_id = row['users_id']
        person = conn.execute(query.where(people.c.user_id == user_id)).fetchone()
        #save profile info
        if person:
            profile = Profile(
                id=person['id'],
                twitter=person['twitter'],
                name=person['name'],
                bio=person['bio'],
                user=user,
                #slug=person['slug'],
                url=person['url'],
                location=person['location'],
                created_ts=person['created_at'],
                updated_ts=person['updated_at']
            )
            session.add(profile)
        session.add(user)
    result.close()
    session.flush()

def move_group_info(metadata):
    conn = metadata.bind.connect()
    groups = metadata.tables['groups']
    membership = metadata.tables['group_memberships']
    #people = metadata.tables['people']
    result = conn.execute(select([groups]))
    session = DBSession()
    for row in result:
        group = Group(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            url=row['url'],
            mailing_list=row['mailing_list'],
            created_ts=row['created_at'],
            updated_ts=row['updated_at'],
            meeting_info=row['meeting_info']
        )
        session.add(group)
        session.flush()
        #get all members
    member_query = membership.select()
    #person = people.select()
    for membership in conn.execute(member_query):
        #get old user
        #print membership
        group_id = membership['group_id']
        person_id = membership['person_id']
        try:
            Profile.query.filter_by(id=person_id).one()
            session.execute(group_membership.insert().values(profile_id=person_id, group_id=group_id))
        except:
            pass
        #old_user = conn.execute(person.where(membership))
#            old_user = conn.execute(person.where())
        #lookup user by email
        #add profile to membership
        #pass
    session.flush()

def move_company_info(metadata):
    conn = metadata.bind.connect()
    companies = metadata.tables['companies']
    membership = metadata.tables['employments']
    result = conn.execute(select([companies]))
    session = DBSession()
    for row in result:
        company = Company(
            id=row['id'],
            name=row['name'],
            url=row['url'],
            address=row['address'],
            description=row['description'],
            created_ts=row['created_at'],
            updated_ts=row['updated_at']
        )
        session.add(company)
    member_query = membership.select()
    for member in conn.execute(member_query):
        company_id = member['company_id']
        person_id = member['person_id']
        try:
            Profile.query.get(person_id)
            session.execute(company_membership.insert().values(profile_id=person_id, company_id=company_id))
        except:
            pass
    result.close()
    session.flush()

def delete_extras():
    session = DBSession()
    rows = session.query(User.email).group_by(User.email).having(func.count(User.email) > 1).all()
    for row in rows:
        user = User.query.filter_by(email=row[0]).filter_by(provider='twitter').one()
        session.delete(user)
    session.flush()

def tags(metadata):
    conn = metadata.bind.connect()
    session = DBSession()
    taggings = metadata.tables['taggings']
    tags = metadata.tables['tags']
    tag_result = conn.execute(select([tags]))
    for row in tag_result:
        tag = Tag(id=row['id'], name=row['name'])
        session.add(tag)
    session.flush()
    result = conn.execute(select([taggings]))
    for row in result:
        #get type
        tag_type = row['taggable_type']
        if tag_type == 'Group':
            Model = Group
        elif tag_type == 'Person':
            Model = Profile
        elif tag_type == 'Company':
            Model = Company
        #get tag id
        tag = Tag.query.get(row['tag_id'])
        obj = Model.query.get(row['taggable_id'])
        obj.tags.append(tag)
        #get taggable id
        session.flush()

def update_sequences():
    session = DBSession()

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    citizenry_engine = engine_from_config(settings, 'citizenry.')
    metadata = MetaData(bind=citizenry_engine)
    load_tables(metadata)
    move_user_info(metadata)
    delete_extras()
    move_group_info(metadata)
    move_company_info(metadata)
    tags(metadata)
