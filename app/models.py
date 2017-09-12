#!/usr/bin/python3


from config import engine
from datetime import datetime
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Text, TIMESTAMP
)
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """docstring for User"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    picture = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        onupdate=datetime.utcnow,
        server_onupdate=current_timestamp()
    )
    categories = relationship(
        'Category',
        order_by='desc(Category.created_at)',
        backref='user'
    )

    @property
    def serialize(self):
        """
            Returns Object data in an easily serializable format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Category(Base):
    """docstring for Category"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    menu_items = relationship(
        'MenuItem',
        order_by='desc(MenuItem.created_at)',
        backref='category'
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        onupdate=datetime.utcnow,
        server_onupdate=current_timestamp()
    )

    @property
    def serialize(self):
        """
            Returns Object data in an easily serializable format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }


class MenuItem(Base):
    """docstring for MenuItem"""
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        onupdate=datetime.utcnow,
        server_onupdate=current_timestamp()
    )

    @property
    def serialize(self):
        """
            Returns Object data in an easily serializable format.
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'category_id': self.category_id
        }


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("All the tables were created sucessfully!")
