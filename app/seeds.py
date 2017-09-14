#!/usr/bin/python3


from config import (
    engine, USER_EMAIL_FOR_DB_SEEDS, USER_NAME_FOR_DB_SEEDS
)
from models import Base, Category, MenuItem, User
from sqlalchemy.orm import sessionmaker


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(
    name=USER_NAME_FOR_DB_SEEDS,
    email=USER_EMAIL_FOR_DB_SEEDS
)

session.add(user1)
session.commit()

categories = [
    {
        'name': 'Soccer',
        'slug': 'soccer',
        'user_id': user1.id,
        'menu_items': [
            {
                'name': 'Soccer Ball',
                'slug': 'soccer_ball',
                'description': None,
            },
            {
                'name': 'Soccer Pads',
                'slug': 'soccer_pads',
                'description': None,
            },
            {
                'name': 'Soccer Shoes',
                'slug': 'soccer_shoes',
                'description': None,
            },
            {
                'name': 'Soccer Pants',
                'slug': 'soccer_pants',
                'description': None,
            },
        ]
    },
    {
        'name': 'Basketball',
        'slug': 'basketball',
        'user_id': user1.id,
        'menu_items': [
            {
                'name': 'Basketball',
                'slug': 'basketball',
                'description': None,
            },
            {
                'name': 'Basketball Sneakers',
                'slug': 'basketball_sneakers',
                'description': None,
            },
            {
                'name': 'Basketball Pants',
                'slug': 'basketball_pants',
                'description': None,
            },
        ]
    },
    {
        'name': 'Baseball',
        'slug': 'baseball',
        'user_id': user1.id,
        'menu_items': [
            {
                'name': 'Baseball',
                'slug': 'baseball',
                'description': None,
            },
            {
                'name': 'Baseball Bat',
                'slug': 'baseball_bat',
                'description': None,
            },
            {
                'name': 'Baseball Gloves',
                'slug': 'baseball_gloves',
                'description': None,
            },
        ]
    },
    {
        'name': 'Hockey',
        'slug': 'hockey',
        'user_id': user1.id,
        'menu_items': [
            {
                'name': 'Hockey Ball',
                'slug': 'hockey_ball',
                'description': None,
            },
            {
                'name': 'Hockey Stick',
                'slug': 'hockey_stick',
                'description': None,
            },
            {
                'name': 'Hockey Helmet',
                'slug': 'hockey_helmet',
                'description': None,
            },
        ]
    },
    {
        'name': 'Cricket',
        'slug': 'cricket',
        'user_id': user1.id,
        'menu_items': [
            {
                'name': 'Cricket Ball',
                'slug': 'cricket_ball',
                'description': 'A cricket ball made with a core of cork, which is layered with tightly wound string, and covered by a leather case with a slightly raised sewn seam.'
            },
            {
                'name': 'Cricket Bat',
                'slug': 'cricket_bat',
                'description': "A cricket bat is a specialised piece of equipment used by batsmen in the sport of cricket to hit the ball, typically consisting of a cane handle attached to a flat-fronted willow-wood blade. The length of the bat may be no more than 38 inches (965 mm) and the width no more than 4.25 inches (108 mm). Its use is first mentioned in 1624. Since 1979, the rule change stipulated that bats can only be made from wood.",
            },
            {
                'name': 'Cricket Helmet',
                'slug': 'cricket_helmet',
                'description': "In the sport of cricket, batsmen often wear a helmet to protect themselves from injury or concussion by the cricket ball, which is very hard and can be bowled to them at speeds over 90 miles per hour (140 km/h). Cricket helmets cover the whole of the skull, and have a grill or perspex visor to protect the face. Often constructed with a carbon fibre and Kevlar shell, the helmet is designed to deflect cricket balls as well as shield the wearer from impact, and its liner includes an inflatable element to tightly fit the helmet to its wearer's head.",
            },
            {
                'name': 'Batting Gloves',
                'slug': 'cricket_batting_gloves',
                'description': None,
            },
            {
                'name': 'Wicketkeeping Gloves',
                'slug': 'cricket_wicketkeeping_gloves',
                'description': None,
            },
            {
                'name': 'Batting Pads',
                'slug': 'cricket_batting_pads',
                'description': None,
            },
            {
                'name': 'Spiked Shoes',
                'slug': 'cricket_spiked_shoes',
                'description': None,
            },
        ]
    },
]


for category in categories:
    newCategory = Category(
        name=category['name'],
        slug=category['slug'],
        user_id=category['user_id']
    )
    session.add(newCategory)
    session.commit()
    for menuItem in category['menu_items']:
        newMenuItem = MenuItem(
            name=menuItem['name'],
            slug=menuItem['slug'],
            description=menuItem['description'],
            category_id=newCategory.id
        )
        session.add(newMenuItem)
        session.commit()


session.close()
print('All tables were seeded successfully!')
