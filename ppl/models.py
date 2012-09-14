from sqlalchemy import (
    func,
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    Boolean
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

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Base.query = DBSession.query_property()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    admin = Column(Boolean, default=False)
    sign_in_count = Column(Integer, default=0)
    remember_token = Column(String)
    #t.datetime "remember_created_at"
    #t.datetime "current_sign_in_at"
    #t.datetime "last_sign_in_at"
    #t.string   "current_sign_in_ip"
    #t.string   "last_sign_in_ip"
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    twitter = Column(String)
    url = Column(String)
    bio = Column(Text)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now, onupdate=func.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref=backref("person", uselist=False))
    name = Column(String)
    imported_from_provider = Column(String)
    imported_from_id = Column(String)
    location = Column(String)
    reviewed = Column(Boolean, default=False)
    imported_from_screen_nane = Column(String)
    mentor = Column(Boolean)
    mentee = Column(Boolean)
    mentor_topics = Column(Text)
    mentee_topics = Column(Text)
    slug = Column(String)

