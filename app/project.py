#!/usr/bin/python3


import config
from flask import (
    Flask, abort, redirect, render_template, make_response,
    request, url_for, flash, jsonify, session as login_session
)
from functools import wraps
import httplib2
import json
from models import Base, Category, MenuItem, User
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
import string
from sqlalchemy import desc
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import random
import requests


Base.metadata.bind = config.engine
DBSession = sessionmaker(bind=config.engine)
session = DBSession()

emptyValues = [None, False, "", []]

app = Flask(__name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def home():
    """Show main landing page."""
    if 'categories' not in login_session:
        categories = session.query(Category).order_by(Category.name).all()
        login_session['categories'] = [c.serialize for c in categories]

    menuItems = session.query(MenuItem).options(
        joinedload(MenuItem.category)
    ).order_by(desc(MenuItem.created_at)).limit(10).all()

    return render_template('home.html', menuItems=menuItems)


@app.route('/catalogue/<string:categorySlug>/items')
def showMenuItemsInACategory(categorySlug):
    try:
        category = session.query(Category).filter_by(
            slug=categorySlug
        ).options(joinedload(Category.menu_items)).one()
        if category in emptyValues:
            """
                This is necessary because while using 'sqlite'
                'NoResultFound' is not thrown by the orm for some reason.
            """
            raise NoResultFound
    except NoResultFound:
        abort(404)

    return render_template(
        'category.html',
        category=category,
        numberOfItems=len(category.menu_items)
    )


@app.route('/catalogue/<string:categorySlug>', methods=['GET', 'POST'])
@requires_auth
def addMenuItemToACategory(categorySlug):
    try:
        category = session.query(Category).filter_by(
            slug=categorySlug
        ).one()
        if category in emptyValues:
            """
                This is necessary because while using 'sqlite'
                'NoResultFound' is not thrown by the orm for some reason.
            """
            raise NoResultFound
    except NoResultFound:
        abort(404)

    if login_session['user_id'] != category.user_id:
        abort(403)

    if request.method == 'GET':
        return render_template(
            'addMenuItem.html',
            category=category
        )
    else:
        formValues = {
            key: value.strip(" \t\n\r") for key, value in request.form.items()
        }
        name = formValues.get('name', None)
        slug = formValues.get('slug', None)

        if (name in emptyValues) or (slug in emptyValues):
            abort(400)

        menuItem = MenuItem(
            name=name,
            slug=slug,
            category_id=category.id,
            description=formValues.get('description', None)
        )

        session.add(menuItem)
        session.commit()
        flash('Menu Item: %s was added' % menuItem.name)

        return redirect(url_for(
            'showMenuItemsInACategory',
            categorySlug=categorySlug
        ))


@app.route('/catalogue/<string:categorySlug>/<string:menuSlug>')
def showMenuItem(categorySlug, menuSlug):
    try:
        menuItem = getMenuItem(categorySlug, menuSlug)
    except NoResultFound:
        abort(404)

    return render_template(
        'menuItem.html',
        menuItem=menuItem,
        categorySlug=categorySlug
    )


@app.route(
    '/catalogue/<string:categorySlug>/<string:menuSlug>/edit',
    methods=['GET', 'POST', 'PUT']
)
@requires_auth
def editMenuItem(categorySlug, menuSlug):
    try:
        menuItem = getMenuItem(categorySlug, menuSlug)
    except NoResultFound:
        abort(404)

    if login_session['user_id'] != menuItem.category.user_id:
        abort(403)

    if request.method == 'GET':
        return render_template(
            'editMenuItem.html',
            menuItem=menuItem,
            categorySlug=menuItem.category.slug
        )
    elif (
        (request.method == 'PUT') or
        (request.form.get('_method', None) == 'PUT')
    ):
        formValues = {
            key: value.strip(" \t\n\r") for key, value in request.form.items()
        }
        name = formValues.get('name', None)
        slug = formValues.get('slug', None)

        if (name in emptyValues) or (slug in emptyValues):
            abort(400)

        menuItem.name = name
        menuItem.slug = slug
        menuItem.description = formValues.get('description', None)
        session.add(menuItem)
        session.commit()
        flash('Menu Item: %s was edited' % menuItem.name)
    else:
        abort(405)

    return redirect(url_for(
        'showMenuItem',
        categorySlug=categorySlug,
        menuSlug=menuSlug
    ))


@app.route(
    '/catalogue/<string:categorySlug>/<string:menuSlug>/delete',
    methods=['GET', 'POST', 'DELETE']
)
@requires_auth
def deleteMenuItem(categorySlug, menuSlug):
    try:
        menuItem = getMenuItem(categorySlug, menuSlug)
    except NoResultFound:
        abort(404)

    if login_session['user_id'] != menuItem.category.user_id:
        abort(403)

    if request.method == 'GET':
        return render_template(
            'deleteMenuItem.html',
            menuItem=menuItem,
            categorySlug=menuItem.category.slug
        )
    elif (
        (request.method == 'DELETE') or
        (request.form.get('_method', None) == 'DELETE')
    ):
        session.delete(menuItem)
        session.commit()
        flash('Menu Item: %s was deleted' % menuItem.name)
    else:
        abort(405)

    return redirect(url_for(
        'showMenuItemsInACategory',
        categorySlug=categorySlug
    ))


@app.route('/login', methods=['GET'])
def login():
    if 'categories' not in login_session:
        categories = session.query(Category).order_by(Category.name).all()
        login_session['categories'] = [c.serialize for c in categories]
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32)
    )
    login_session['state'] = state

    return render_template(
        'login.html',
        STATE=state,
        GOOGLE_CLIENT_ID=config.GOOGLE_CLIENT_ID,
        FB_APP_ID=config.FB_APP_ID,
        FB_VERSION=config.FB_VERSION,
        APP_PORT=config.APP_PORT
    )


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data.decode('utf-8')
    print("access token received %s " % access_token)

    app_id = config.FB_APP_ID
    app_secret = config.FB_APP_SECRET

    url = 'https://graph.facebook.com/oauth/access_token'
    url += '?grant_type=fb_exchange_token'
    url += "&client_id={}&client_secret={}&fb_exchange_token={}".format(
        app_id, app_secret, access_token
    )

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    result = json.loads(result)
    token = result['access_token']

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/{}/me".format(config.FB_VERSION)

    url = userinfo_url + '?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = userinfo_url + '/picture'
    url += '?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/{}/permissions?access_token={}'.format(
        facebook_id, access_token
    )

    h = httplib2.Http()
    h.request(url, 'DELETE')[1]
    return "You have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = OAuth2WebServerFlow(
            client_id=config.GOOGLE_CLIENT_ID,
            client_secret=config.GOOGLE_CLIENT_SECRET,
            scope='',
            redirect_uri='postmessage'
        )
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),
            401
        )
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != config.GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'),
            401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        login_session['access_token']
    )
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
        )
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/logout', methods=['POST'])
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in")

    return redirect(url_for('home'))


# JSON API Routes

@app.route('/catalogue.json')
def getAllItemsInCatalogue():
    try:
        categories = session.query(Category).options(
            joinedload(Category.menu_items)
        ).order_by(desc(Category.created_at)).all()

        if categories in emptyValues:
            raise NoResultFound
    except NoResultFound:
        response = {
            'message': 'No Categories found in the system.'
        }
        return jsonify(response), 400
    response = []
    for category in categories:
        menuItems = [m.serialize for m in category.menu_items]
        category = category.serialize
        category['menu_items'] = menuItems
        response.append(category)

    return jsonify(categories=response)


@app.route('/catalogue.json/<string:categorySlug>')
def getCategoryJSON(categorySlug):
    try:
        category = session.query(Category).filter_by(
            slug=categorySlug
        ).options(
            joinedload(Category.menu_items)
        ).one()

        if category in emptyValues:
            raise NoResultFound
    except NoResultFound:
        response = {
            'message': "No Category %s found in the system." % categorySlug
        }

        return jsonify(response), 400

    menuItems = [m.serialize for m in category.menu_items]
    response = category.serialize
    response['menu_items'] = menuItems

    return jsonify(category=response)


@app.route('/catalogue.json/<string:categorySlug>/<string:menuSlug>')
def showMenuItemJSON(categorySlug, menuSlug):
    try:
        menuItem = getMenuItem(categorySlug, menuSlug)
    except NoResultFound:
        response = {
            'message': 'No result found.'
        }

        return jsonify(response), 404

    return jsonify(menu_item=menuItem.serialize)


# Helper Functions


def createUser(login_session):
    newUser = User(
        name=login_session.get('username'),
        email=login_session.get('email'),
        picture=login_session.get('picture')
    )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()

    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        if user in emptyValues:
            raise NoResultFound

        return user.id
    except NoResultFound:
        return None


def getMenuItem(categorySlug, menuSlug):
    menuItem = session.query(MenuItem).filter_by(
        slug=menuSlug
    ).options(joinedload(MenuItem.category)).one()

    if menuItem in emptyValues or menuItem.category.slug != categorySlug:
        raise NoResultFound

    return menuItem


if __name__ == '__main__':
    app.secret_key = config.APP_SECRET_KEY
    app.debug = True
    app.run(host=config.APP_HOST, port=config.APP_PORT)
