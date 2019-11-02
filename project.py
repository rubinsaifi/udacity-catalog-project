#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Sport, MenuItem, User

# Session Import
from flask import session as login_session
import random
import string

# OAuth Libs
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Loading secret json file

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///sportitemwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# login route
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return 'Current session state - %s' % state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps(
                'Invalid state parameter'
            ), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # got auth code
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps(
                'Failed to upgrade authorization code.'
            ), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that access token is valid
    access_token = credentials.access_token
    print(access_token)
    url = (
      'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    )
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    if result.get('error') is not None:
        response = make_response(
            json.dumps(
                'Token Validation error: %s' % result['error']
            ), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify access token used to intended user
    gid = credentials.id_token['sub']

    if result['user_id'] != gid:
        response = make_response(
            json.dumps(
                'Token does not match with user ID'
            ), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for the app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps(
                'Client ID token mismatch with App ID'
            ), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gid = login_session.get('gid')
    if stored_access_token is not None and gid == stored_gid:
        response = make_response(
            json.dumps(
                'Current User is already connected'
            ), 200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store acceess token in login_session
    login_session['access_token'] = credentials.access_token
    login_session['gid'] = gid

    # Get user information
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'atl': 'json'}
    answer = requests.get(userinfo_url, params=params)

    print('Token: %s' % credentials.access_token)
    data = answer.json()
    print(json.dumps(data))

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Add user information to db
    print('Adding User to local DB')
    try:
        user_id = getUserID(login_session['email'])
        if not user_id:
            user_id = createUser(login_session)
        login_session['user_id'] = user_id
    except Exception as e:
        print("Exception %s" % str(e))

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    output += '<img src="' + login_session['picture'] + '" '
    output += 'style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;'
    flash('You are now logged in as %s' % login_session['username'])

    return output


@app.route('/logout')
def logout():
    if 'username' in login_session:
        gdisconnect()
        # del login_session['gid']
        # del login_session['access_token']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        # del login_session['user_id']
        flash("You have been successfully logged out!")
        return redirect(url_for('showSports'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('showSports'))

# disconnect
@app.route('/gdisconnect', methods=['GET'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps(
                'Current user not connected'
            ), 401
        )
        return response
    # Revoke access token
    print('Token: %s' % access_token)
    print('User: %s' % login_session['username'])

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    _result_ = h.request(url, 'GET')
    result_resp = json.loads(_result_[1].decode('utf-8'))
    result = _result_[0]

    print(result_resp)
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gid']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        response = make_response(
            json.dumps(
                'Successfully disconnected'
            ), 200
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # Something wrong with disconnect
        if result['status'] == '400' and result_resp['error_description'] == 'Token expired or revoked':
            response = make_response(
                json.dumps(
                    'Token already expired or revoked'
                ), 200
            )
        else:
            response = make_response(
                json.dumps(
                    'Failed to revoke token for given user'
                ), 400
            )
        response.headers['Content-Type'] = 'application/json'
        return response


# Local user permission system
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None

# end of local permission system

# JSON APIs to view Sport Information
@app.route('/sport/<int:sport_id>/menu/JSON')
def sportMenuJSON(sport_id):
    items = session.query(MenuItem).filter_by(sport_id=sport_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/sport/<int:sport_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(sport_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/sport/JSON')
def sportsJSON():
    sports = session.query(Sport).all()
    return jsonify(sports=[r.serialize for r in sports])


@app.route('/sport/catalog.json')
def showCatalog():
    items = session.query(MenuItem).order_by(MenuItem.id.desc())
    return jsonify(catalog=[i.serialize for i in items])


# HTML Routes

# Show all Sport menu
@app.route('/')
@app.route('/sport/')
def showSports():
    sport = session.query(Sport).order_by(asc(Sport.name))
    items = session.query(MenuItem).order_by(desc(MenuItem.id))
    return render_template('landing.html', sport=sport, items=items)


# Create a new sport
@app.route('/sport/new/', methods=['GET', 'POST'])
def newSport():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newSport = Sport(
            name=request.form['name'],
            user_id=login_session['user_id']
        )
        session.add(newSport)
        flash('New Restaurant %s Successfully Created' % newSport.name)
        session.commit()
        return redirect(url_for('showSports'))
    else:
        return render_template('newSport.html')


# Show a sport menu
@app.route('/sport/<int:sport_id>/')
@app.route('/sport/<int:sport_id>/menu/')
def showMenu(sport_id):
    sport = session.query(Sport).filter_by(id=sport_id).one()
    items = session.query(MenuItem).filter_by(sport_id=sport_id).all()
    return render_template('menu.html', items=items, sport=sport)


@app.route('/sport/item')
def showItem():
    items = session.query(MenuItem).order_by(MenuItem.id.desc())
    return render_template('menuitem.html', items=items)


# Edit a Support
@app.route('/sport/<int:sport_id>/edit/', methods=['GET', 'POST'])
def editSport(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedSport = session.query(Sport).filter_by(id=sport_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedSport.name = request.form['name']
            flash('Sport Successfully Edited %s' % editedSport.name)
            return redirect(url_for('showSports'))
    else:
        return render_template('editSport.html', sport=editedSport)


# Delete a Sport
@app.route('/sport/<int:sport_id>/delete/', methods=['GET', 'POST'])
def deleteSport(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    sportToDelete = session.query(Sport).filter_by(id=sport_id).one()
    if request.method == 'POST':
        session.delete(sportToDelete)
        flash('%s Successfully Deleted' % sportToDelete.name)
        session.commit()
        return redirect(url_for('showSports', sport_id=sport_id))
    else:
        return render_template('deleteSport.html', sport=sportToDelete)


# Create a new menu item
@app.route('/sport/<int:sport_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(sport_id):
    if 'username' not in login_session:
        return redirect('/login')
    sport = session.query(Sport).filter_by(id=sport_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            sport_id=sport_id
        )
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', sport_id=sport_id))
    else:
        return render_template('newmenuitem.html', sport_id=sport_id)


# Edit a menu item
@app.route(
  '/sport/<int:sport_id>/menu/<int:menu_id>/edit',
  methods=['GET', 'POST']
)
def editMenuItem(sport_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # sport = session.query(Sport).filter_by(id=sport_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        # if request.form['course']:
        #    editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', sport_id=sport_id))
    else:
        return render_template(
            'editmenuitem.html',
            sport_id=sport_id,
            menu_id=menu_id,
            item=editedItem
        )


# Delete a menu item
@app.route(
  '/sport/<int:sport_id>/menu/<int:menu_id>/delete',
  methods=['GET', 'POST']
)
def deleteMenuItem(sport_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    # sport = session.query(Sport).filter_by(id = sport_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', sport_id=sport_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'Qa#f}Ww|]+6FuYc_web[#yV_nSte|_4Lu"kyGg'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
