# -*- coding: utf-8 -*-
from flask import render_template, jsonify, make_response
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
from sqlalchemy import or_, and_, func
import shlex


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
    elif form.errors:
        return jsonify(form.errors), 400
    else:
        if current_user.is_anonymous:
            login_form = LoginForm()
            return render_template('register.html', title='Register', form=form, login_form=login_form)
        
        return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>/<group_id>')
def addgroup(username, group_id):
    user = User.query.filter_by(username=username).first_or_404()
    user.IdGroup = group_id
    db.session.add(user)
    db.session.commit()
    if current_user.is_anonymous:
        login_form = LoginForm()
        return redirect(url_for('user', username=username, login_form=login_form))
    return redirect(url_for('user', username=username))


@app.route('/game', methods=['GET', 'POST'])
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
    if current_user.is_anonymous:
        login_form = LoginForm()
        return render_template('user.html', title="Profile", user=user, login_form=login_form)
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
            return jsonify({'username': ['Неправильное имя пользователя или пароль.']}), 400
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return jsonify(form.errors), 400


@app.route('/')
@app.route('/index')
def index():
    login_form = LoginForm()
    mods_count = Mod.query.count()
    return render_template("index.html", login_form=login_form, mods_count=mods_count)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/makenewmod', methods=['GET', 'POST'])
def makenewmod():
    form = MakeNewModForm()
    if form.validate_on_submit():
        mod = Mod(GameId=form.gamename.data, name=form.materialname.data, Description=form.materialtext.data,
                  Picture=form.image.data.read(), DescriptionCard=form.desctex.data, Language=form.language.data,
                  GameTagId=form.tags.data, DateCreation=form.adddate.data, AuthorId=current_user.id)
        db.session.add(mod)
        db.session.commit()
        if form.tubelink.data:
            mod_video=ModVideo(Link=form.tubelink.data, Modid=mod.id)
            db.session.add(mod_video)
        mod_link = ModLink(Link=form.mainlink.data, Modid=mod.id, LinkName=form.maintext.data)
        db.session.add(mod_link)
        if form.sublink.data:
            mod_link = ModLink(Link=form.sublink.data, Modid=mod.id, LinkName=form.subtext.data)
            db.session.add(mod_link)
        db.session.commit()
        flash('Поздравляем, вы создали новый мод!')
        return redirect(url_for('index'))
    elif form.errors:
        return jsonify(form.errors), 400
    return render_template('makenewmod.html', title='Создание мода', form=form)


@app.route('/gamelist')
def gamelist():
    search = request.args.get('searchGame')
    if search:
        search_words = [word.lower() for word in search.split()]
        games = Game.query.filter(and_(
            *[func.lower(Game.name).contains(word) for word in search_words]
        ))
    else:
        games = Game.query
    
    page = request.args.get('page', type=int, default=1)
    games = games.order_by(Game.name).paginate(page=page, per_page=10, error_out=False)

    if current_user.is_anonymous:
        login_form = LoginForm()
        return render_template("gamelist.html", games=games, title="Список игр", login_form=login_form)
    
    return render_template("gamelist.html", games=games, title="Список игр")


@app.route('/faq')
def faq():
    if current_user.is_anonymous:
        login_form = LoginForm()
        return render_template("faq.html", title="FAQ", login_form=login_form)
    
    return render_template("faq.html", title="FAQ")


@app.route('/mods/')
@app.route('/mods/<game_id>')
def mods(game_id=None, search=None):
    kwargs = { 'mods': [] }

    search = request.args.get('search')
    # game_id = request.args.get('game_id', type=int)

    if game_id:
        # поиск по названию игры
        game = Game.query.get(game_id)
        mods = Mod.query.filter_by(GameId=game_id)
        kwargs.update({ 'game': game })
    elif search:
        # поиск по запросу
        search_words = [word.lower() for word in search.split()]
        mods = Mod.query.filter(and_(
            *[func.lower(Mod.name).contains(word) for word in search_words]
        ))
    else:
        mods = Mod.query
    
    tags_in_filter = []
    if mods:
        tags = GameTags.query.all()
        tags_count = []
        for tag in tags:
            mods_with_tag = [mod for mod in mods if mod.GameTagId == tag.id]
            if mods_with_tag:
                tags_count.append((tag, len(mods_with_tag)))

        kwargs.update({ 'tags_count': tags_count })
    
        # фильтрация по тегам
        if request.cookies.get('tags_filter'):
            tags_in_filter = request.cookies.get('tags_filter').split()
        
        # добавление нового фильтра
        tag_to_set = request.args.get('set')
        if tag_to_set and tag_to_set not in tags_in_filter:
            tags_in_filter.append(tag_to_set)
        
        # удаление фильтра
        tag_to_reset = request.args.get('reset')
        if tag_to_reset:
            if tag_to_reset == 'all':
                tags_in_filter = []
            elif tag_to_reset in tags_in_filter:
                tags_in_filter.remove(tag_to_reset)

        # применение фильтров
        mods = mods.filter(or_(*[Mod.GameTagId == tag_id for tag_id in tags_in_filter]))
            
        page = request.args.get('page', type=int, default=1)
        mods = mods.order_by(Mod.name).paginate(page=page, per_page=15, error_out=False)
    kwargs.update({'mods': mods})
    kwargs.update({'tags_filter': tags_in_filter})

    if current_user.is_anonymous:
        login_form = LoginForm()
        kwargs.update({'login_form': login_form})

    # сохранение тегов, по которым идёт фильтрация, в куки
    response = make_response(render_template('modlist.html', **kwargs))
    response.set_cookie('tags_filter', ' '.join(tags_in_filter))

    return response


@app.route('/mod_photo/<mod_id>')
def mod_photo(mod_id):
    mod = Mod.query.get(mod_id)
    return mod.Picture or redirect('/static/img/logo.svg')


@app.route('/mod/<mod_id>')
def mod(mod_id):
    mod = Mod.query.get(mod_id)

    if current_user.is_anonymous:
        login_form = LoginForm()
        return render_template("mod.html", mod=mod, login_form=login_form)
    views = ModViews.query.filter(
        and_(ModViews.Modid == mod.id, ModViews.AuthorId == current_user.id)
    )
    if not views.count():
        new_view = ModViews(Modid=mod.id, AuthorId=current_user.id)
        db.session.add(new_view)
        db.session.commit()

    comment_form = CommentForm()
    
    return render_template("mod.html", mod=mod, comment_form=comment_form)


@app.route('/mod_link/<link_id>')
def mod_link(link_id):
    link = ModLink.query.get(link_id)
    if link:
        if current_user.is_authenticated:
            mod = link.mod
            downloads = ModDownload.query.filter(
                and_(ModDownload.Modid == mod.id, ModDownload.AuthorId == current_user.id)
            )
            if not downloads.count():
                new_download = ModDownload(Modid=mod.id, AuthorId=current_user.id)
                db.session.add(new_download)
                db.session.commit()
        return redirect(link.Link)
    else:
        return redirect(url_for('index')), 404


@app.route('/comment/<mod_id>', methods=['post'])
@login_required
def comment(mod_id):
    form = CommentForm()
    if form.validate_on_submit() and form.comment.data:
        comment = ModComment(Message=form.comment.data, Modid=mod_id,
                             MessageAuthorId=current_user.id,
                             )
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('mod', mod_id=mod_id))
