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
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

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
#Base = declarative_base()
class Base(object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)
Base = declarative_base(cls=Base)
Base.query = Session.query_property()


def initialize_sql(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine

class TagAssociation(Base):
    """Associates a collection of Tag objects
    with a particular parent.

    """
    __tablename__ = "tag_association"

    @classmethod
    def creator(cls, discriminator):
        """Provide a 'creator' function to use with
        the association proxy."""

        return lambda tags: TagAssociation(
            tags=tags,
            discriminator=discriminator)

    discriminator = Column(String)
    """Refers to the type of parent."""

    @property
    def parent(self):
        """Return the parent object."""
        return getattr(self, "%s_parent" % self.discriminator)

class Tag(Base):
    """The Address class.

    This represents all address records in a
    single table.

    """
    association_id = Column(Integer,
                            ForeignKey("tag_association.id")
                            )
    name = Column(String)
    association = relationship(
        "TagAssociation",
        backref="tags")

    parent = association_proxy("association", "parent")

    def __repr__(self):
        return self.name

class HasTags(object):
    """HasTags mixin, creates a relationship to
    the address_association table for each parent.

    """
    @declared_attr
    def tag_association_id(cls):
        return Column(Integer,
                      ForeignKey("tag_association.id"))

    @declared_attr
    def tag_association(cls):
        discriminator = cls.__name__.lower()
        cls.tags = association_proxy(
            "tag_association", "tags",
            creator=TagAssociation.creator(discriminator)
        )
        return relationship("TagAssociation",
                            backref=backref("%s_parent" % discriminator,
                            uselist=False))

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

class Profile(HasTags, Base):
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

class Company(HasTags, Base):
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
class Group(HasTags, Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, onupdate=create_slug, default=create_slug)
    description = Column(Text)
    url = Column(String)
    mailing_list = Column(String)
    meeting_info = Column(Text)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, default=func.now(), onupdate=func.now())
    members = relationship("Profile", secondary=group_membership)
