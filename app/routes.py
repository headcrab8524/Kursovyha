# -*- coding: utf-8 -*-
from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect
from app import db
from app.forms import *
from app.forms import MakeGameForm
from flask_login import current_user, login_user
from app.models import *
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime
from flask import url_for
from flask_login import login_required
from flask_paginate import *


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, Sex=form.sex.data,
                    Dateregistration=datetime.utcnow(),
                    Birth_Date=form.birthdate.data, Ava=form.avatar.data.read(), Country=form.country.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>/<group_id>')
def addgroup(username, group_id):
    user = User.query.filter_by(username=username).first_or_404()
    user.id = group_id
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/game', methods=['GET','POST'])
@login_required
def game():
    form = MakeGameForm()
    if form.validate_on_submit():
        game = Game(name=form.gamename.data, Picture=form.picture.data.read())
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('game.html', title='Game', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title="Profile", user=user)


@app.route('/profile_photo/<id>')
def profile_photo(id):
    user = User.query.get(id)
    return user.Ava


@app.route('/game_photo/<id>')
def game_photo(id):
    game = Game.query.get(id)
    return game.Picture


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


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Welcome to SpyMods")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/makenewmod', methods=['GET', 'POST'])
def makenewmod():
    form = MakeNewModForm()
    if form.validate_on_submit():
        mod = Mod(gamename=form.gamename.data, materialname=form.materialname.data, materialtext=form.materialtext.data,
                    image=form.image.data.read(), language=form.language.data, mainlink=form.mainlink.data,
                  maintext=form.maintext.data, sublink=form.sublink.data, subtext=form.subtext.data, tubelink=form.tubelink.data,
                  tags=form.tags.data, adddate=form.adddate.data)
        db.session.add(mod)
        db.session.commit()
        flash('Поздравляем, вы создали новый мод!')
        return redirect(url_for('index'))
    return render_template('makenewmod.html', title='Создание мода', form=form)


@app.route('/gamelist')
def gamelist():
    page = request.args.get('page', type=int, default=1)
    games = Game.query.paginate(page=page, per_page=10, error_out=False)
    return render_template("gamelist.html", games=games, title="Список игр")

@app.route('/faq')
def faq():
    return render_template("faq.html", title="FAQ")
