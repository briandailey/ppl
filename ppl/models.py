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
    backref,
    validates
)
import itertools
from urlparse import urlparse
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base, declared_attr
#from sqlalchemy.ext.associationproxy import association_proxy

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

from .history_meta import Versioned, versioned_session
class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit')
    ]

    def __init__(self, request):
        pass  # pragma: no cover

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
versioned_session(DBSession)
class Base(object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)
Base.query = DBSession.query_property()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

class Tag(Base):
    """The Tag class.

    This represents all tag records in a
    single table.

    """
    __tablename__ = 'tags'
    name = Column(String)

    @property
    def all_owners(self):
        return list(
            itertools.chain(*[
                getattr(self, attr)
                for attr in [a for a in dir(self) if a.endswith("_parents")]
            ])
        )

    def __repr__(self):
        return self.name

class HasTags(object):
    """HasTags mixin, creates a relationship to
    the address_association table for each parent.

    """

    @declared_attr
    def tags(cls):
        tag_association = Table(
            "%s_taggings" % cls.__tablename__,
            cls.metadata,
            Column("tag_id", ForeignKey("tags.id"), primary_key=True),
            Column("%s_id" % cls.__tablename__,
                                ForeignKey("%s.id" % cls.__tablename__),
                                primary_key=True),
        )
        return relationship(Tag, secondary=tag_association, backref="%s_parents" % cls.__name__.lower())

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
    admin = Column(Boolean, default=False)
    sign_in_count = Column(Integer, default=0)

    auth_token = Column(String, unique=True)
    auth_secret = Column(String, nullable=True)
    provider = Column(String)
    identifier = Column(String, unique=True)

    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())

class Profile(HasTags, Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref("profile", cascade="delete", uselist=False, lazy=False, innerjoin=True), lazy=False, innerjoin=True)
    slug = Column(String, unique=True)
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

    @validates('name')
    def _set_slug(self, key, value):
        self.slug = slugify(value)
        return value

company_membership = Table(
    'company_employees', Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id')),
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('public', Boolean, default=True)
)
class Company(HasTags, Versioned, Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String)
    url = Column(String)
    address = Column(Text)
    description = Column(Text)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    location = Column(String)
    email = Column(String)
    employees = relationship("Profile", secondary=company_membership, backref="companies")

    @validates('name')
    def _set_slug(self, key, value):
        self.slug = slugify(value)
        return value

    def get_url(self):
        if urlparse(self.url).scheme:
            return self.url
        else:
            return 'http://{}'.format(self.url)

group_membership = Table(
    "group_members", Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('public', Boolean, default=True)
)
class Group(HasTags, Versioned, Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String)
    description = Column(Text)
    url = Column(String)
    mailing_list = Column(String)
    meeting_info = Column(Text)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    members = relationship("Profile", secondary=group_membership, backref="groups")

    @validates('name')
    def _set_slug(self, key, value):
        self.slug = slugify(value)
        return value

    def get_url(self):
        if urlparse(self.url).scheme:
            return self.url
        else:
            return 'http://{}'.format(self.url)
