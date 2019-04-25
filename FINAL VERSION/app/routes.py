from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, Fb_Register_Form, EatForm, InviteForm
from app.models import User, Meal
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import urllib3
import facebook
import requests
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import json
import urllib
import ast

@app.route('/')

@app.route('/index')
@login_required
def index():
    database_meals = Meal.query.filter_by(user_id=current_user.id).all()
    meals=[]
    for meal in database_meals:
        attributes=["body","timestamp"]
        body= meal.body
        timestamp= meal.timestamp
        values=[body,timestamp]
        m=dict(zip(attributes, values))
        meals.append(m)
    return render_template('index.html', title='Home', meals=meals)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, name=form.name.data, location=form.location.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    authorization_url=authorize(client_id,client_secret)
    print(authorization_url)
    return render_template('register.html', title='Register', form=form, auth_url=authorization_url)

@app.route('/fb_register', methods=['GET', 'POST'])
def fb_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Fb_Register_Form()
    if form.validate_on_submit():
        email=form.email.data
        print(email)
        info=extract(email)
        id=info['id']
        name=info['name']
        location='Boston'
        friends=str(info['friends'])
        user = User(username=form.username.data, email=email, id=id, name=name, location=location, friends=friends)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('fb_register.html', title='Fb Register', form=form)

@app.route("/eat",methods=['GET', 'POST'])
def eat():
    if current_user.is_authenticated:
        form = EatForm()
        if form.validate_on_submit():
            term=form.food.data
            location= current_user.location
            next_page = url_for('result', term=term ,location=location)
            return redirect(next_page)
    else:
        return redirect(url_for('index'))
    return render_template('eat.html', title='Eat', form=form)

@app.route("/result/<term>/<location>",methods=['GET', 'POST'])
def result(term,location):
    if current_user.is_authenticated:
        url_params = {'term': term,'location': location,'limit': 50,'offset': 0}
        restos=yelp_call(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params).get('businesses')
        names=[]
        links=[]
        for r in restos:
            name= r['name']
            names.append(name)
            link=r['url']
            links.append(link)
        iterator=[i for i in range(len(names))]
        user=current_user
        friends_id=ast.literal_eval(user.friends)
        friends=[User.query.filter_by(id=friend_id).first() for friend_id in friends_id]
        form=InviteForm()
        form.friends.choices = [(i,friends[i].name) for i in range(len(friends))]
        form.food.choices =[(i,names[i]) for i in range(len(names))]
        if form.validate_on_submit():
            name= friends[form.friends.data].name
            chosen_food =names[form.food.data]
            message= "invited " + name+ " to eat at " + chosen_food
            post = Meal(body= message, author=user)
            db.session.add(post)
            db.session.commit()
            flash('Invite sent')
            return redirect('/index')
        return render_template('record.html',names=names, links=links, index=iterator, form= form)
    else:
        return redirect(url_for('index'))


#Yelp API call
API_KEY= ""
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

def yelp_call(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

# Facebook Oauth and API call 
client_id = ''
client_secret = ''

def authorize(client_id,client_secret):
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'http://localhost:5000/fb_register'     # Should match Site URL
    fb = OAuth2Session(client_id, redirect_uri=redirect_uri)
    fb= facebook_compliance_fix(fb)
    authorization_url, state = fb.authorization_url(authorization_base_url)
    return authorization_url

def get_fb_token(client_id,client_secret):

    url = 'https://graph.facebook.com/oauth/access_token'       
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, params=payload)
    app_token=response.json()['access_token']
    return app_token
def extract(user_email):
    app_token=get_fb_token(client_id,client_secret)
    graph = facebook.GraphAPI(access_token=app_token, version = 3.1)
    users = 'https://graph.facebook.com/v3.1/app/accounts/test-users?access_token='+app_token
    users = requests.get(users).json()
    attributes=['id','email','name','location','friends']
    for u in range(len(users['data'])):
        user_token=users['data'][u]['access_token']
        call_email="https://graph.facebook.com/v2.11/me?fields=email&access_token="+user_token
        call_me="https://graph.facebook.com/v2.11/me?fields=name&access_token="+user_token
        call_location="https://graph.facebook.com/v2.11/me?fields=location&access_token="+user_token
        call_friends="https://graph.facebook.com/v2.11/me?fields=friends&access_token="+user_token
        email =requests.get(call_email).json()['email']
        if user_email==email:
            id =requests.get(call_me).json()['id']
            name=requests.get(call_me).json()['name']
            location=requests.get(call_location).json()
            raw_friends=requests.get(call_friends).json()
            raw_friends=raw_friends['friends']['data']
            friends=[]
            for f in raw_friends:
                friends.append(f['id'])
            values=[id,email,name, location, friends]
            user=dict(zip(attributes, values))
            print(user)
    return user


