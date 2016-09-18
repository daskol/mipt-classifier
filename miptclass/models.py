#   encoding: utf8
#   models.py

from datetime import datetime
from miptclass import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey, PrimaryKeyConstraint, String, func, create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


db = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(settings.DATABASE_URI, pool_recycle=3600)
))


@as_declarative()
class Base(object):

    __session__ = db

    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, server_default=func.now(), default=datetime.now, onupdate=datetime.now, nullable=False)


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    deactivated = Column(String(16))
    hidden = Column(Boolean, default=False)
    sex = Column(Integer, default=0, nullable=False)


class Group(Base):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    screen_name = Column(String(255))
    is_closed = Column(Boolean, default=False, nullable=False)
    description = Column(String(1023))
    members_count = Column(Integer, default=0)
    type = Column(String(16))


class University(Base):

    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(Integer, default=1, nullable=False)
    city = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return '<User[%d] `%r`>' % (self.id, self.name)


class UserGroups(Base):

    __tablename__ = 'user_groups'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)


class UserFriends(Base):

    __tablename__ = 'user_friends'

    id = Column(Integer, primary_key=True, nullable=False)
    friend_id = Column(Integer, primary_key=True, nullable=False)

    PrimaryKeyConstraint('id', 'friend_id')

class UserUniversities(Base):

    __tablename__ = 'user_universities'

    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)

    def __repr__(self):
        return '<UserUniversity %d - %d>' % (self.id, self.university_id)


class AccessToken(Base):

    __tablename__ = 'access_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False)
    valid = Column(Boolean, default=True, nullable=False)
    expires_in = Column(DateTime, default=datetime.max, nullable=False)
