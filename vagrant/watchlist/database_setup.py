import sys
#for data types
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text, SmallInteger
#for connecting
from sqlalchemy.ext.declarative import declarative_base
#for ForeignKey relationships
from sqlalchemy.orm import relationship
#for use at the end of the configuration file
from sqlalchemy import create_engine


Base = declarative_base()



"""
The Users class is designed to inherit from Base
"""
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    provider = Column(String(80), nullable = False)
    username = Column(String(80), nullable = False)
    firstName = Column(String(80))
    lastName = Column(String(80))
    motto = Column(String(80))
    email = Column(String(80), nullable = False)
    picture = Column(String(80))

class Passwords(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)
    password = Column(String(255), nullable = False)

"""
The watchlist class is designed to inherit from Base
"""
class Watchlist(Base):
    #__tablename__ is special in sqlalchemy to let python know the variablename we will use for tables
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

"""
The Media class is designed to inherit from Base
"""
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key = True)
    name = Column(String(250))
    imdb_id = Column(Integer)
    art = Column(String(250))
    type = Column(String(250))
    rating = Column(SmallInteger)
    comments = Column(Text)
    watchlist_id = Column(Integer, ForeignKey('watchlist.id'))
    #creating the reference for the ForeignKey to use
    watchlist = relationship(Watchlist)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'imdb_id': self.imdb_id,
            'art': self.art,
            'type': self.type,
            'rating': self.rating,
            'comments': self.comments
        }

#end of file wrap up
engine = create_engine('sqlite:///Watchlists.db')
#adds the class to the db
Base.metadata.create_all(engine)
