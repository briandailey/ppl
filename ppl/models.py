from sqlalchemy import (
    func,
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    Table
)
from sqlalchemy.orm import (
    relationship,
    backref
)
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

#from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import unauthenticated_userid
from ppl.utils import slugify

from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow
class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'post')
    ]

    def __init__(self, request):
        pass  # pragma: no cover

#Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Session = scoped_session(sessionmaker(autocommit=True))
Base = declarative_base()
Base.query = Session.query_property()


def initialize_sql(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine

def get_user(request):
    # the below line is just an example, use your own method of
    # accessing a database connection here (this could even be another
    # request property such as request.db, implemented using this same
    # pattern).
    userid = unauthenticated_userid(request)
    if userid is not None:
        # this should return None if the user doesn't exist
        # in the database
        return User.query.filter_by(id=userid).first()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    admin = Column(Boolean, default=False)
    sign_in_count = Column(Integer, default=0)
    access_token = Column(String, nullable=False)
    access_token_secret = Column(Text)
    provider = Column(String)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())

def create_slug(context):
    return slugify(context.current_parameters['name'])

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref("person", cascade="delete", uselist=False), lazy=False, innerjoin=True)
    slug = Column(String, onupdate=create_slug, default=create_slug, unique=True)
    name = Column(String, nullable=False)
    bio = Column(Text)
    location = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    url = Column(String)
    twitter = Column(String)
    github_name = Column(String)
    imported_from_provider = Column(String)
    imported_from_id = Column(String)
    reviewed = Column(Boolean, default=False)
    imported_from_screen_nane = Column(String)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, onupdate=create_slug, default=create_slug)
    url = Column(String)
    address = Column(Text)
    description = Column(Text)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    location = Column(String)
    email = Column(String)
    #employees = relationship("Profile", secondary=company_membership)

group_membership = Table(
    "group_members", Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('public', Boolean, default=True)
)
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, onupdate=create_slug, default=create_slug)
    description = Column(Text)
    url = Column(String)
    mailing_list = Column(String)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    members = relationship("Profile", secondary=group_membership)
